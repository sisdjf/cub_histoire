import pygame as pg
from settings import *


class ObjectRenderer: 
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
    
    def draw(self):
        self.draw_background()
        self.render_game_object()

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        pg.draw.rect(self.screen, FLOOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_object(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key = lambda t: t[0], reverse = True) 
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)    

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1 : self.get_texture('resources/textures/mur_medieval1.jpg'),
            2 : self.get_texture('resources/textures/mur1.png'),
            3 : self.get_texture('resources/textures/mur2.png'),
            4 : self.get_texture('resources/textures/mur3.png'),
            5 : self.get_texture('resources/textures/mur4.png'),
            6 : self.get_texture('resources/textures/mur5.png'),

        }