from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from OpenGL.GL import *
from geometry.geometry import Geometry
from numpy import arange
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial
from geometry.lineGeometry import LineGeometry
from math import cos, sin, pi
from scipy.fft import fft2, ifft2, ifftshift, fftshift
from scipy.signal import convolve2d
import numpy as np
import pygame

f1 = 1
f2 = 1
theta1 = 0
theta2 = pi / 12

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800 / 600)
        self.camera.setPosition([0, 0, 10])
        self.frame = 0
        
        self.renderer.render(self.scene, self.camera)
    

    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../cosinusoidal_gratings/{self.frame}.jpg")

    def update(self):
        pass
        # self.pattern_2(self.frame)
        # self.renderer.render(self.scene, self.camera)
        # self.screen_recorder()
        # self.frame += 10   
        

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()



