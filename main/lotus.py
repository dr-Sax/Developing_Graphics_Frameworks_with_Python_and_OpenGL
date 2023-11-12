# https://github.com/jbum/Whitney-Music-Box-Examples/blob/master/processing/digital_harmony_examples/whitney_columnbc/whitney_columnbc.pde

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.lineGeometry import LineGeometry
from math import sin, cos, pi
from OpenGL.GL import *
from material.material import Material
from material.surfaceMaterial import SurfaceMaterial
import pygame
import numpy as np
from time import sleep

Z = 20  # Sets camera distance away from xy plane

# render a basic scene
class Test(Base):

    def initialize(self):

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 1)
        self.camera.setPosition([0, 0, Z])
        

        vsCode = '''
            in vec3 vertexPosition;
            out vec3 position;
            uniform mat4 modelMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 projectionMatrix;
            void main()
            {
                vec4 pos = vec4(vertexPosition, 1.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
                position = vertexPosition;
            }
        '''

        self.material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_LOOP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [1.0, 1.0, 1.0]
        )

        self.mesh_list = []
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../lotus/{0}.jpg")
        

        
        self.renderer.render(self.scene, self.camera) 

        self.i = 1
        self.timer = 0



    def update(self):  
        if self.timer % 10 == 0:
            x1 = 10 * cos(self.i/20*2*pi)
            y1 = 10 * sin(self.i/20*2*pi)
            for j in np.arange(0, 20):
                x2 = 10 * cos(j/20*2*pi)
                y2 = 10 * sin(j/20*2*pi)
                self.geometry = LineGeometry(x1 = x1, y1 = y1, x2 = x2, y2 = y2)
                self.temp_mesh = Mesh(self.geometry, self.material)

                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)
                
            self.renderer.render(self.scene, self.camera) 
            
            # screen = pygame.display.get_surface()
            # size = screen.get_size()
            # buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
            # screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
            # pygame.image.save(screen_surf, f"../lotus/{self.i}.jpg")

            self.i = self.i + 1
            

        self.timer = self.timer + 1
            


        


# instantiate this class and run the program
Test(screenSize = [1300, 1300]).run()
