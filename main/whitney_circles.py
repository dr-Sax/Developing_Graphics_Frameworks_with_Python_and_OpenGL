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
CIRCLE_CNT = 10
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
        self.square_container = []
        self.timer_container = np.arange(0, 10, 1)
        self.pace = 0

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

        # # Creating initial square list
        # for i in range(0, SQUARE_CNT):

        #     square_side_length = i / SQUARE_CNT * O * pi

        #     self.geometry = RectangleGeometry(
        #         width = square_side_length,
        #         height = square_side_length
        #         )
            
        #     color_ratio = i / SQUARE_CNT
        #     material = self.material_gen(r = color_ratio, g = color_ratio, b = color_ratio, draw_style = GL_LINE_LOOP)
        #     self.square_container.append(Mesh(self.geometry, material))
        #     self.scene.add(self.square_container[i])

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
    
    def circle_updater(self, x_off = 0, y_off = 0, radii = [x for x in range(CIRCLE_CNT)]):

        self.remove_shape_cluster(self.circle_container)

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
            self.circle_container[i] = Mesh(self.geometry, material)
            self.scene.add(self.circle_container[i])

        self.renderer.render(self.scene, self.camera) 

    def square_updater(self):

        self.remove_shape_cluster(self.square_container)

        for i in range(0, SQUARE_CNT):
            

            square_side_length = i / SQUARE_CNT * O * pi

            self.geometry = RectangleGeometry(
                width = square_side_length,
                height = square_side_length
            )
            material = self.material_gen(r = np.random.random(), g = np.random.random(), b = np.random.random(), draw_style = GL_LINE_LOOP)
            self.square_container[i] = Mesh(self.geometry, material)
            self.scene.add(self.square_container[i])

        self.renderer.render(self.scene, self.camera) 
    
    def remove_shape_cluster(self, container):
        for i in range(0, len(container)):
            self.scene.remove(container[i])
    
    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../spiral/{ftime}.jpg")

    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self): 
        if self.pace == 10:
            self.circle_updater()
            self.pace = 0
        else:
            self.pace += 1
        
       
        

        
        
        

        
# instantiate this class and run the program


Test(screenSize = [WIDTH, HEIGHT]).run()
