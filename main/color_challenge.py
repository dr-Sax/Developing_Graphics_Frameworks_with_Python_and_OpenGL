from operator import add, sub
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from math import sin, cos, tan, cosh, exp, pi
from OpenGL.GL import *
from material.surfaceMaterial import SurfaceMaterial
from geometry.lineGeometry import LineGeometry
from geometry.polygonGeometry import PolygonGeometry
from geometry.rectangleGeometry import RectangleGeometry
import numpy as np
import pygame
from time import sleep

WIDTH = 1080
HEIGHT = 1080
Z = 10  # Sets camera distance away from xy plane
NUM_POINTS = 30
SIZE = Z / 3


# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.line_container = []


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

        self.point_container = []
        self.point_container2 = []
        self.point_container3 = []
        self.pace = 0
        self.angle = 0
        self.phi = 0
        self.renderer.render(self.scene, self.camera)

    
    def angled_grating(self, offset):
        for r in np.arange(0.1, Z / 3, 0.1):
            for theta in np.linspace(0, 2 * np.pi, abs(int(50 * r*sin(2*np.pi * r /(Z/3) + offset)))):
                p1 = PolygonGeometry(
                    sides = 20,
                    radius = np.exp(-r),
                    x = r * np.cos(theta),
                    y = r * np.sin(theta),
                )
                m1 = self.material_gen(r = theta*cos(r), g = np.random.rand(1), b = np.random.rand(1)) # blue green
                m2 = self.material_gen(r = theta*cos(r), g = np.random.rand(1), b = theta*cos(r))   # green
                m3 = self.material_gen(r = np.random.rand(1), g = theta*cos(r), b = np.random.rand(1) ) # purple
                m4 = self.material_gen(r = np.random.rand(1), g = np.random.rand(1), b = np.random.rand(1) ) # random
                x = r * np.cos(theta + self.phi)
                y = r * np.sin(theta + self.phi)

                if x > 0 and y > 0:  # Q1
                    material = m1
                elif x < 0 and y > 0:# Q2
                    material = m2
                elif x < 0 and x < 0:# Q3
                    material = m3
                elif x > 0 and y < 0:# Q4
                    material = m4
                else:
                    material = m4

                
                self.point_container.append(Mesh(p1, material))
                self.scene.add(self.point_container[-1])                

    def remove_grating(self):
        for i in range(0, len(self.point_container)):
            self.scene.remove(self.point_container[i])
        self.point_container = []
    
    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP, wireframe = True):
        material = SurfaceMaterial(
            {
                'useVertexColors': False,
                'wireframe': wireframe,
                'lineWidth': 3,
                'drawStyle': draw_style
            },  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES,
            lineColor = [r, g, b]
        )
        return material
    
    def screen_recorder(self, angle):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../froot_loops/{self.pace}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        pass
        if self.pace == 0:
            self.angled_grating(self.angle) 
            self.angle += pi/200
            self.phi += pi/200
            
        elif self.pace % 1 == 0:
            self.remove_grating()
            self.angled_grating(self.angle) 
            self.angle += pi/200
            self.phi += pi/200
            
        self.renderer.render(self.scene, self.camera)
        self.screen_recorder(angle = self.pace)
        self.pace += 1




t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


