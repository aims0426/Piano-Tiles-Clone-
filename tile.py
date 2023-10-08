import pygame
pygame.init()
SCREEN=WIDTH, HEIGHT = 300,500
t_wid= WIDTH//4
t_height= HEIGHT//4
BLACK= (0,0,0)
BLUE=(30,144,255)
class TILE(pygame.sprite.Sprite):#sprite.Sprite is an inbuilt class in python
    #TILE will inherit all the properties from class sprite
    def __init__(self,x, y, window):
        #__init__ is used to initialise attributes of the objects
        #self is used to represent the objects of the class 
        #x,y,-position to create tile
        super(TILE,self).__init__()#class name and first variable
        #if we inherit some class in pygame we should initilaise that class
        self.window=window#making copy of the window in this class
        self.x,self.y =x,y
        self.color= BLACK
        self.surface= pygame.Surface((t_wid,t_height),pygame.SRCALPHA)
        #to create a transparent image
        self.rect= self.surface.get_rect()#TO GET A RECTANGLE
        self.rect.x= x #setting tile position
        self.rect.y= y
    def update(self,speed):
        self.rect.y+= speed
        if self.rect.y >= HEIGHT:
            self.kill()
        pygame.draw.rect(self.surface, self.color,(0,0, t_wid, t_height))
        #filling the tile with black color; passing width and height
        self.window.blit(self.surface, self.rect)#this statement should be last
