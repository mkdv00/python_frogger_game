import sys
from os import walk

import pygame
from pygame import Rect, Surface


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        
        # image
        self.import_assets()
        
        self.frame_index = 0
        self.state = 'down'
        self.image: Surface = self.animations[self.state][self.frame_index]
        self.rect: Rect = self.image.get_rect(center=pos)
        
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 250
        
        # collision
        self.collision_sprites = collision_sprites
        self.hitbox: Rect = self.rect.inflate(0, -self.rect.height / 2)
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    
                    # if move right
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    # if move left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    
                    # if move down
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    # if move up
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
    
    def import_assets(self):
        self.animations = {}
        for index, folder in enumerate(walk('graphics/player')):
            if index == 0:
                for folder_name in folder[1]:
                    self.animations[folder_name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(file=path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)
    
    def move(self, dt):
        if self.direction.magnitude():
            self.direction = self.direction.normalize()
            
        # horizontal movement + collisions
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision(direction='horizontal')
        
        # vertical movement + collisions
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision(direction='vertical')
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.state = 'right'
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.state = 'left'
            self.direction.x = -1
        else:
            self.direction.x = 0

        # vertical movement
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.state = 'down'
            self.direction.y = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.state = 'up'
            self.direction.y = -1
        else:
            self.direction.y = 0
    
    def animate(self, dt):
        current_animation = self.animations[self.state]
        
        if self.direction.magnitude():
            self.frame_index += 8 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        
        self.image = current_animation[int(self.frame_index)]
    
    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = self.hitbox.left
        
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.left = self.hitbox.left
        
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()
