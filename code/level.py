import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self):

        #Pega o display surface
        self.display_surface = pygame.display.get_surface()
        
        #Configuração do grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #Configuração da sprite
        self.create_map()
    
    def create_map(self):
        layout = {
            'boundary': import_csv_layout('../Zeldinha-Souls/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../Zeldinha-Souls/map/map_Grass.csv'),
            'object': import_csv_layout('../Zeldinha-Souls/map/map_LargeObjects.csv'),
        }
        graphics = {
            'grass': import_folder('../Zeldinha-Souls/graphics/grass'),
            'objects': import_folder('../Zeldinha-Souls/graphics/objects')
        }

        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites], 'object', surf)
                            
        self.player = Player((2000,1430),[self.visible_sprites],self.obstacles_sprites)

    def run(self):
        #Atualiza e desenha o jogo
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # Configuração Geral
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Criando o chão
        self.floor_surf = pygame.image.load('../Zeldinha-Souls/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):

        # pegando o deslocamento
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth

        # desenhando o chão 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)