from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from OpenGL.GL import *
from geometry.geometry import Geometry
from numpy import arange
from material.pointMaterial import PointMaterial
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
        self.frame = 4440
        self.dot_container = []

        self.renderer.render(self.scene, self.camera)
    
    def lpf(self, mat, lim):
        for i in range(0, len(mat)):
            for j in range(0, len(mat[i])):
                if abs(mat[i][j]) < lim:
                    mat[i][j] = 0
        return mat

    def pattern(self):
        

        for x in arange(-5, 5, 0.1):
                for y in arange(-5, 5, 0.1):
                    geometry = Geometry()
                    posData = []

                    posData.append([x, y, 0])
                    geometry.addAttribute('vec3', 'vertexPosition', posData)
                    geometry.countVertices()
                    
                    r1 = 0.5 * cos(2 * pi * f1 * (x)) + 0.5
                    r2 = 0.5 * cos(2 * pi * f2 * (x * cos(theta2) + y * sin(theta2))) + 0.5


                    pointMaterial = PointMaterial(
                        {
                            'baseColor': [r1 * r2, r1 * r2, r1 * r2],
                            'pointSize': 5,
                        }, 

                        lineColor = [1.0, 1.0, 1.0]
                    )


                    pointMesh = Mesh(geometry, pointMaterial)
                    self.dot_container.append(pointMesh)
                    self.scene.add(pointMesh)

    def pattern_2(self, l):

        if l > 4440:
            for dot in self.dot_container:
                self.scene.remove(dot)
            self.dot_container = []

        x = np.arange(-5, 5, 0.1)
        X, Y = np.meshgrid(x, x)

        r1 = 0.5 * np.cos(2 * np.pi * f1 * X) + 0.5
        r2 = 0.5 * np.cos(2 * np.pi * f2 * (X * np.cos(theta2) + Y * np.sin(theta2))) + 0.5
        

        iffts = ifftshift(r1)
        ft = fft2(iffts)
        ftts_r1 = fftshift(ft)

        iffts = ifftshift(r2)
        ft = fft2(iffts)
        ftts_r2 = fftshift(ft)

        ftts_r2 = self.lpf(ftts_r2, 1200)  # low pass filter to remove artifacts

        ftts_r3 = abs(ifft2(convolve2d(ftts_r1, ftts_r2, 'same')))
        ftts_r3 = self.lpf(ftts_r3, l)


        y = -5
        x = -5
        step = 0.1
        for r in range(0, len(r1)):
            x = -5
        
            for col in range(0, len(r1[r])):
                f_r1 = ftts_r3[r][col]
                
                geometry = Geometry()
                posData = []
                posData.append([x, y, 0])
                geometry.addAttribute('vec3', 'vertexPosition', posData)
                geometry.countVertices()

                pointMaterial = PointMaterial(
                        {
                            'baseColor': [f_r1, f_r1, f_r1],
                            'pointSize': 5,
                        }, 

                        lineColor = [1.0, 1.0, 1.0]
                    )


                pointMesh = Mesh(geometry, pointMaterial)
                self.dot_container.append(pointMesh)
                self.scene.add(pointMesh)

                x = x + step
            
            y = y + step

    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../cosinusoidal_gratings/{self.frame}.jpg")

    def update(self):

        self.pattern_2(self.frame)
        self.renderer.render(self.scene, self.camera)
        self.screen_recorder()
        self.frame += 10   
        

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()



