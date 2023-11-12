# https://github.com/jbum/Whitney-Music-Box-Examples/blob/master/processing/digital_harmony_examples/whitney_columnbc/whitney_columnbc.pde

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.sphereGeometry import SphereGeometry
from geometry.polygonGeometry import PolygonGeometry
from math import sin, cos, pi
from OpenGL.GL import *
from material.material import Material
import numpy as np
import pygame
from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceMaterial import SurfaceMaterial

WIDTH = 2560
HEIGHT = 1400
Z = 20  # Sets camera distance away from xy plane
O = 10  # Outer Circle Radius
CIRCLE_CNT = 30
SQUARE_CNT = 10

# render a basic scene
class Test(Base):

    def initialize(self):

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])

        # Define the Materiality of each circle on the screen
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

        self.circle_container = []
        self.circle_container2 = []
        self.c1_x = 10
        self.c2_x = -10
        self.timer_container = np.arange(0, 10, 1)
        self.pace = 0
        self.frame = 0

        # Creating initial circle list
        for i in range(0, CIRCLE_CNT):
            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = O * i / CIRCLE_CNT
                )
            
            color_ratio = i / CIRCLE_CNT
            material = self.material_gen(r = color_ratio, g = color_ratio, b = color_ratio)
            self.circle_container.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container[i])
        
        # Creating initial circle list
        for i in range(0, CIRCLE_CNT):
            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = O * i / CIRCLE_CNT
                )
            
            color_ratio = i / CIRCLE_CNT
            material = self.material_gen(r = color_ratio, g = color_ratio, b = color_ratio)
            self.circle_container2.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container2[i])


        self.renderer.render(self.scene, self.camera) 


    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP):
        material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': True,
                'lineWidth': 1,
                'drawStyle': draw_style
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [r, g, b]
        )
        return material
    
    def circle_updater(self, circ_ls, x_off = 0, y_off = 0, radii = np.linspace(0, O, CIRCLE_CNT)):

        self.remove_shape_cluster(circ_ls)

        # Creating initial circle list
        for i in range(0, CIRCLE_CNT):
            self.geometry = PolygonGeometry(
            sides = 100, 
            radius = radii[i],
            x = x_off,
            y = y_off
            )
            color_ratio = 1.0
            material = self.material_gen(r = color_ratio, g = color_ratio, b = color_ratio)
            circ_ls[i] = Mesh(self.geometry, material)
            self.scene.add(circ_ls[i])

        self.renderer.render(self.scene, self.camera) 
        

    
    def remove_shape_cluster(self, container):
        for i in range(0, len(container)):
            self.scene.remove(container[i])
    
    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../moire_circles/{self.frame}.jpg")

    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self): 
        if self.pace == 100:
            self.pace = 0
        else:
            if self.pace % 5 == 1:
                self.circle_updater(circ_ls = self.circle_container, x_off = self.c1_x)
                self.circle_updater(circ_ls = self.circle_container2, x_off = self.c2_x)
                if self.c1_x < -10:
                    self.c1_x = 10
                    self.c2_x = -10
                else:
                    self.c1_x -= 0.5
                    self.c2_x += 0.5
            
            self.pace += 1
        
        self.screen_recorder()
        self.frame += 1

        
       
        

        
        
        

        
# instantiate this class and run the program


Test(screenSize = [WIDTH, HEIGHT]).run()
