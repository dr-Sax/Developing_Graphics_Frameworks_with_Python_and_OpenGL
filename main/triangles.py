# https://github.com/jbum/Whitney-Music-Box-Examples/blob/master/processing/digital_harmony_examples/whitney_columnbc/whitney_columnbc.pde

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.polygonGeometry import PolygonGeometry
from math import sin, cos, pi
from OpenGL.GL import *
from material.material import Material
from material.surfaceMaterial import SurfaceMaterial
import pygame
import numpy as np

Z = 30  # Sets camera distance away from xy plane

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
                'lineWidth': 5,
                'drawStyle': GL_LINE_LOOP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [1.0, 1.0, 1.0]
        )

        self.material2 = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 5,
                'drawStyle': GL_LINE_LOOP
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [1.0, 0.0, 0.0]
        )

        self.mesh_list = []
        self.mesh_list2 = []

        for i in np.arange(0.5, 7, 0.5):
            self.geometry = PolygonGeometry(sides = 5, radius = i)
            self.temp_mesh = Mesh(self.geometry, self.material)
            self.temp_mesh.translate(x = 12, y = 0, z = 0)
            self.temp_mesh.rotateZ(30*pi/180)
            self.mesh_list.append(self.temp_mesh)
            self.scene.add(self.temp_mesh)

        # for i in np.arange(0.5, 7, 0.5):
        #     self.geometry = PolygonGeometry(sides = 3, radius = i)
        #     self.temp_mesh = Mesh(self.geometry, self.material2)
        #     self.temp_mesh.translate(x = -5, y = 0, z = 0)
        #     self.temp_mesh.rotateZ(30*pi/180)
        #     self.mesh_list2.append(self.temp_mesh)
        #     self.scene.add(self.temp_mesh)
        
        self.renderer.render(self.scene, self.camera) 

        self.timer = 0




    def update(self):  

        ftime = self.timer 
        
        for i in range(0, len(self.mesh_list)):   
            rate = (i + 1) / len(self.mesh_list)
            x = 12 * cos(ftime * rate)
            y = 12 * sin(ftime * rate)         

            self.temp_mesh = Mesh(self.geometry, self.material)

            self.temp_mesh.translate(x = x, y = y, z = 0)
            x_pos_i = self.mesh_list[i].getPosition()[0]
            y_pos_i = self.mesh_list[i].getPosition()[1]
            self.mesh_list[i].translate(
                x = self.temp_mesh.getPosition()[0] - x_pos_i, 
                y = self.temp_mesh.getPosition()[1] - y_pos_i, 
                z = 0
                )   

        # for i in range(0, len(self.mesh_list2)):   
        #     rate = (i + 1) / len(self.mesh_list2)
        #     x = -5 * cos(-ftime * rate)
        #     y = -5 * sin(-ftime * rate)         

        #     self.temp_mesh = Mesh(self.geometry, self.material2)

        #     self.temp_mesh.translate(x = x, y = y, z = 0)
        #     x_pos_i = self.mesh_list2[i].getPosition()[0]
        #     y_pos_i = self.mesh_list2[i].getPosition()[1]
        #     self.mesh_list2[i].translate(
        #         x = self.temp_mesh.getPosition()[0] - x_pos_i, 
        #         y = self.temp_mesh.getPosition()[1] - y_pos_i, 
        #         z = 0
        #         )   

        



        self.renderer.render(self.scene, self.camera) 
        # screen = pygame.display.get_surface()
        # size = screen.get_size()
        # buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        # screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        # pygame.image.save(screen_surf, f"../spiral/{ftime}.jpg")

        self.timer = self.timer + 0.017  # number of secs that pass after each update
        


# instantiate this class and run the program
Test(screenSize = [900, 900]).run()
