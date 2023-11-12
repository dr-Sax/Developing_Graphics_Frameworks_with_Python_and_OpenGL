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
from geometry.ellipsoidGeometry import EllipsoidGeometry
from geometry.polygonGeometry import PolygonGeometry
from time import sleep

Z = 20  # Sets camera distance away from xy plane
O = 10
I = 8 / 14 * O
S = I / 2
SS = 1.5 / 14 * O
SSS = 6 / 14 * SS

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
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [1.0, 1.0, 1.0]
        )

        self.material_yellow = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [0.867, 0.839, 0.325]
        )

        self.material_dark_blue = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [0.224,0.31,0.592]
        )

        self.material_dark_green = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [0.169, 0.435, 0.345]
        )

        self.material_red = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': GL_LINE_STRIP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [0.949,0.251,0.188]
        )

        self.mesh_list = []
        # screen = pygame.display.get_surface()
        # size = screen.get_size()
        # buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        # screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        # pygame.image.save(screen_surf, f"../lotus/{0}.jpg")



        # Outer Circle:
        self.geometry = PolygonGeometry(sides = 100, radius = O)
        self.temp_mesh = Mesh(self.geometry, self.material)
        self.mesh_list.append(self.temp_mesh)
        self.scene.add(self.temp_mesh)


        theta = [
            [pi/2 + pi/6, pi + pi/3],
            [pi, 3 * pi / 2 + pi/6],
            [pi + pi / 3, 2 * pi], 
            [pi + 2 * pi / 3, 2 * pi + pi / 3],
            [0, pi/2 + pi/6],
            [pi/3, pi],
        ]

        # Six Crossed Circles:
        for scale in np.arange(SS/S, 1.0, 0.007):
            for i in range(0, 6):
                x = I * cos(i / 6 * 2 * pi)
                y = I * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S * scale, x = x, y = y)
                self.temp_mesh = Mesh(self.geometry, self.material_dark_blue)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Six Inner Circles:
        for scale in np.arange(SSS/SS, 1.0, 0.02):
            for i in range(0, 6):
                x = I * cos(i / 6 * 2 * pi)
                y = I * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = SS * scale, x = x, y = y)
                self.temp_mesh = Mesh(self.geometry, self.material_dark_green)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Six Inner-Inner Circles:
        for scale in np.arange(0, 1.0, 0.05):
            for i in range(0, 6):
                x = I * cos(i / 6 * 2 * pi)
                y = I * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = SSS * scale, x = x, y = y)
                self.temp_mesh = Mesh(self.geometry, self.material_red)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Inner Cusps:  
        for scale in np.arange(0.6, 0.8, 0.01):
            for i in range(0, 6):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x, y = y, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Inner Cusps:  
        for scale in np.arange(0.2, 0.3, 0.01):
            for i in range(0, 6):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x, y = y, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Inner Cusps:  
        for scale in np.arange(0, 0.1, 0.01):
            for i in range(0, 6):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S * scale, x = x + 0, y = y + 0, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(3, 5):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x + 10, y = y + 5.7, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(1, 3):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x, y = y - 11.5, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(2, 4):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x + 10, y = y - 5.7, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)
        
        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(0, 2):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x - 10, y = y - 5.7, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)
        
        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(4, 6):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x , y = y + 11.5, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)

        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(5, 6):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x - 10 , y = y + 5.7, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)
        
        # Outer Cusps:  
        for scale in np.arange(0.9, 1, 0.01):
            for i in range(0, 1):
                x = I * scale * cos(i / 6 * 2 * pi)
                y = I * scale * sin(i / 6 * 2 * pi)
                self.geometry = PolygonGeometry(sides = 100, radius = S*scale, x = x - 10, y = y + 5.7, theta1 = theta[i][0], theta2 = theta[i][1])
                self.temp_mesh = Mesh(self.geometry, self.material_yellow)
                self.mesh_list.append(self.temp_mesh)
                self.scene.add(self.temp_mesh)


        self.mesh_list1 = []
        self.geometry = PolygonGeometry(sides = 100, radius = O)
        self.temp_mesh = Mesh(self.geometry, self.material)
        self.mesh_list1.append(self.temp_mesh)
        self.scene.add(self.temp_mesh)

        self.mesh_list2 = []
        self.geometry = PolygonGeometry(sides = 100, radius = O * 0.5)
        self.temp_mesh = Mesh(self.geometry, self.material)
        self.mesh_list2.append(self.temp_mesh)
        self.scene.add(self.temp_mesh)

        self.mesh_list3 = []
        self.geometry = PolygonGeometry(sides = 100, radius = O * 0.75)
        self.temp_mesh = Mesh(self.geometry, self.material)
        self.mesh_list3.append(self.temp_mesh)
        self.scene.add(self.temp_mesh)


        self.renderer.render(self.scene, self.camera) 
        self.counter1 = 0
        self.counter2 = 50
        self.counter3 = 75

        self.i = 0
        



    def update(self):  
        if self.counter1 % 1 == 0:

            # f1
            self.scene.remove(self.mesh_list1[-1])
            self.geometry = PolygonGeometry(sides = 100, radius = O * self.counter1 / 75)
            self.temp_mesh = Mesh(self.geometry, self.material)
            self.mesh_list1.append(self.temp_mesh)
            self.scene.add(self.temp_mesh)

            #f2
            self.scene.remove(self.mesh_list2[-1])
            self.geometry = PolygonGeometry(sides = 100, radius = O * self.counter2 / 75)
            self.temp_mesh = Mesh(self.geometry, self.material)
            self.mesh_list2.append(self.temp_mesh)
            self.scene.add(self.temp_mesh)

            #f3
            self.scene.remove(self.mesh_list3[-1])
            self.geometry = PolygonGeometry(sides = 100, radius = O * self.counter3 / 75)
            self.temp_mesh = Mesh(self.geometry, self.material)
            self.mesh_list3.append(self.temp_mesh)
            self.scene.add(self.temp_mesh)

        
        if self.counter1 == 100:
            self.counter1 = 0
        else:
            self.counter1 += 1
        
        if self.counter2 == 100:
            self.counter2 = 0
        else:
            self.counter2 += 1

        if self.counter3 == 100:
            self.counter3 = 0
        else:
            self.counter3 += 1

        self.renderer.render(self.scene, self.camera) 
            
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../mandala_21/{self.i}.jpg")
        
        self.i += 1

            


        


# instantiate this class and run the program
Test(screenSize = [1300, 1300]).run()
