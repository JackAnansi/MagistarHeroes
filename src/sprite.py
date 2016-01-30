'''
Created on Jan 25, 2016

@author: Dan
'''

import pygame
from enum import Enum

class GravityType(Enum):
    Normal = 1
    ZeroG = 0
    Reversed = -1
    
class Weight(Enum):
    Light = 4
    Medium = 6
    Heavy = 8
    
class Sprite(object):
    '''
    Sprites are things that exist on the screen. Some move, some don't.
    '''

    def __init__(self, image, position, object_container, weight=Weight.Medium, gravity=GravityType.Normal):
        '''
        Constructor
        '''
        self.name = image
        self.load_image(image)
        self.alive = True                   # Does this exist?
        self.rect = pygame.Rect(position, 
                                (self.image.get_rect().width, self.image.get_rect().height))
        self.position = position            # tuple
        self.velocity = (0, 0)              # tuple
        self.acceleration = (0.0, 0.0)      # tuple
        self.grounded = False               # Can you jump?
        self.gravity = gravity              # What is gravity at the moment
        self.weight = weight                # How much gravity affects you
        
        # This is a weakref to the parent container of objects
        self.object_container = object_container
        
    def load_image(self, image):
        try:
            self.image = pygame.image.load('../img/' + image + '.png').convert_alpha()
        except pygame.error as message:
            print("oops!")
            raise SystemExit(message)
    
    def isAlive(self):
        return self.alive
    
    def update(self, clock):
        if clock.get_fps() == 0:
            fps = 1 / 60
        else:
            fps = (1 / clock.get_fps())
        ''' Gravity '''
        if self.gravity == GravityType.Normal:
            gravity_accel = (0, (1000 + (4 * self.weight.value)))
        elif self.gravity == GravityType.Reversed:
            gravity_accel = (0, (-1000 - (4 * self.weight.value)))
        else:
            gravity_accel = (0, 0)
        
        #print("Gravity acceleration:")
        #print(gravity_accel)
        
        # Movement acceleration
        # Handle friction (lower acceleration to 0)
        temp = self.acceleration
        self.acceleration = (temp[0] * 0.2, self.acceleration[1])
        me_velocity = tuple(fps * _ for _ in self.acceleration)
        #print("Me acceleration:")
        #print(self.acceleration)
        
        gravity_velocity = tuple(fps * _ for _ in gravity_accel)
        
        #print("Gravity velocity:")
        #print(gravity_velocity)
        ''' Gravity ends '''
        
        # Find new velocity
        self.velocity = tuple([vel + grav for vel, grav in zip(self.velocity, gravity_velocity)])
        self.velocity = tuple([vel + move for vel, move in zip(self.velocity, me_velocity)])
        
        # Check for ground
        if self.isGrounded():
            if self.velocity[1] > 0:
                self.velocity = (self.velocity[0] * 0.80, 0) # Friction
            self.acceleration = (self.acceleration[0], 0)

        velocity_step = tuple(fps * _ for _ in self.velocity)
        
        # Collision detection
        self.detect_collisions()
        
        # Find new position
        self.rect.x = self.rect.x + velocity_step[0]
        self.rect.y = self.rect.y + velocity_step[1]
    
    def isGrounded(self):
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            return True
        else:
            return False
            
    def get_max_speed(self):
        return ((1 / self.weight.value) + 100)
    
    def detect_collisions(self):
        for name, thingy in self.object_container.items():
                if name != self.name:
                    if self.rect.colliderect(thingy.rect):
                        pass
        
            
class ShortLivedSprite(Sprite):
    def __init__(self, lifetime, image, position, object_container, 
                 weight=Weight.Medium, gravity=GravityType.Normal):
        super().__init__(image, position, object_container, 
                         weight=Weight.Medium, gravity=GravityType.Normal)
        
        self.initial_lifetime = lifetime
        self.lifetime = lifetime
        
    def update(self, clock):
        if self.lifetime > 0:
            Sprite.update(self, clock)
            if clock.get_fps() == 0:
                fps = 1 / 60
            else:
                fps = (1 / clock.get_fps())
            self.lifetime = self.lifetime - fps
            self.linear_fade()
        else:
            self.alive = False
            
    def linear_fade(self):
        fade_amt = (self.lifetime / self.initial_lifetime) * 255
        print(fade_amt)
        self.image.set_alpha(fade_amt)