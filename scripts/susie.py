import pygame
import math
import os

base_path = os.path.dirname(__file__)
character_path = os.path.join(base_path, "..", "assets", "susie_sprite.png")

class Susie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.spritesheet = pygame.image.load(character_path).convert_alpha()


        FRAME_WIDTH = 328
        FRAME_HEIGHT = 368

        self.animations = {
            "idle":  self.get_frames(0, 6, FRAME_WIDTH, FRAME_HEIGHT),
            "disapointed": self.get_frames(6, 1, FRAME_WIDTH, FRAME_HEIGHT),
            "reaction1":  self.get_frames(7, 1, FRAME_WIDTH, FRAME_HEIGHT),
            "reaction2":    self.get_frames(8, 2, FRAME_WIDTH, FRAME_HEIGHT),
            "reaction3":    self.get_frames(10, 2, FRAME_WIDTH, FRAME_HEIGHT),
            "reaction4":    self.get_frames(12, 2, FRAME_WIDTH, FRAME_HEIGHT),
            "reaction5":    self.get_frames(14, 2, FRAME_WIDTH, FRAME_HEIGHT),
        }

        # Animation state
        self.dir_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 0.05  # frames per update tick
        self.image = self.animations[self.dir_animation][0]
        self.rect = self.image.get_rect(x=20, y=100)


        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

    def get_frames(self, start_col, num_frames, frame_width, frame_height):
        frames = []
        for i in range(num_frames):
            current_col = start_col + i
            
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

            start_x = current_col * frame_width
            start_y = 0 
            
            frame.blit(self.spritesheet, (0, 0), (start_x, start_y, frame_width, frame_height))
            frames.append(frame)
        return frames
    
    def change_reaction(self, reaction, actual_time):
        if self.dir_animation != reaction:
            self.dir_animation = reaction
            self.frame_index = 0
        
        self.reaction_expiry = actual_time + 1000
    
    def update(self, actual_time):
            
        if self.dir_animation != "idle" and actual_time >= self.reaction_expiry:
            self.dir_animation = "idle"
            self.frame_index = 0
            
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.dir_animation]):
            self.frame_index = 0
            
        self.image = self.animations[self.dir_animation][int(self.frame_index)]

    def update_loose(self):
            
        self.dir_animation = "reaction4"
            
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.dir_animation]):
            self.frame_index = 0
            
        self.image = self.animations[self.dir_animation][int(self.frame_index)]