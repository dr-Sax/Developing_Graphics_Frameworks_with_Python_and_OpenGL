# https://github.com/jbum/Whitney-Music-Box-Examples/blob/master/processing/digital_harmony_examples/whitney_columnbc/whitney_columnbc.pde

#D92530
#60277E
#2445A2
#77CE89
#F5FC7C
#F5FC7C

color_order = [
    [0.851,0.145,0.188],
    [0.376,0.153,0.494],
    [0.141,0.271,0.635],
    [0.467,0.808,0.537],
    [0.961,0.988,0.486],
    [0.961,0.988,0.486]
]




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

WIDTH = 8.5 * 100
HEIGHT = 13.5 * 100
Z = 20  # Sets camera distance away from xy plane
O = 10  # Outer Circle Radius
CIRCLE_CNT = 24
R = (Z + 2) / (2 * CIRCLE_CNT) - 0.04


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
        self.circle_container_right = []

        # Creating left circle list
        for i in range(0, CIRCLE_CNT):
            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = (i + 1) * R,
                x = - Z * WIDTH / HEIGHT / 2,
                theta1 = - pi / 2 - .09,
                theta2 = pi / 2
                )
            
            r = color_order[i % 6][0]
            g = color_order[i % 6][1]
            b = color_order[i % 6][2]
            material = self.material_gen(r = r, g = g, b = b)
            self.circle_container.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container[i])

         # Creating right circle list
        for i in range(0, CIRCLE_CNT):
            self.geometry = PolygonGeometry(
                sides = 100, 
                radius = R * (i + 1),
                x =  Z * WIDTH / HEIGHT / 2,
                theta1 = pi / 2 - 0.09, 
                theta2 = 3 *  pi / 2
                )
            
            r = color_order[i % 6][0]
            g = color_order[i % 6][1]
            b = color_order[i % 6][2]
            material = self.material_gen(r = r, g = g, b = b)
            self.circle_container_right.append(Mesh(self.geometry, material))
            self.scene.add(self.circle_container_right[i])

        # Outer Rectangle:
        #0.914,0.961,0.396
        rect = RectangleGeometry(width = Z * WIDTH / HEIGHT + 1, height = Z + 2)
        material = self.material_gen(r = 0.914, g = 0.961, b = 0.396, draw_style = GL_LINE_LOOP)
        self.scene.add(Mesh(rect, material))
        


        self.renderer.render(self.scene, self.camera) 


    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP_ADJACENCY):
        material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': False,
                'lineWidth': 5,
                'drawStyle': draw_style
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [r, g, b]
        )
        return material        

    def update(self): 
        pass


Test(screenSize = [WIDTH, HEIGHT]).run()
