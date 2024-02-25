import sys
from os import walk

import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        
        # image
        self.import_assets()
        
        self.frame_index = 0
        self.state = 'down'
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 250
        
        # collision
        self.collision_sprites = collision_sprites
    
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    
                    # if move right
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx
                    # if move left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.rect.colliderect(self.rect):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    
                    # if move down
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery
                    # if move up
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery
    
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
        self.rect.centerx = round(self.pos.x)
        self.collision(direction='horizontal')
        
        # vertical movement + collisions
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
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
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
