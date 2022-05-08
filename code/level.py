import pygame
from settings import *
from title import Title
from player import Player
from debug import debug

class Level:
    def __init__(self):

        #Pega o display surface
        self.display_surface = pygame.display.get_surface()
        
        #Configuração do grupo de sprites
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        #Configuração da sprite
        self.create_map()
    
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Title((x,y), [self.visible_sprites,self.obstacles_sprites])
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites])

    def run(self):
        #Atualiza e desenha o jogo
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)