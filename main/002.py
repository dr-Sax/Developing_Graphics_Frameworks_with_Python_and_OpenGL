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
from geometry.rectangleGeometry import RectangleGeometry
import numpy as np
import pygame
from time import sleep

WIDTH = 1080 * 2
HEIGHT = 1350
Z = 10  # Sets camera distance away from xy plane
NUM_LINES = 50


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


        self.line_container = []
        self.line_container2 = []
        self.line_container3 = []
        self.pace = 0
        self.angle = 0

         
        
        # r = RectangleGeometry(12, 12)
        # material = self.material_gen(r = 1.0, g = 1.0, b = 1.0, draw_style = GL_TRIANGLE_FAN, wireframe = False)
        # r_mesh = Mesh(r, material)
        # self.scene.add(r_mesh)

        #self.angled_grating(np.pi / 6)

        self.renderer.render(self.scene, self.camera)

        # sleep(3)   
        # self.remove_grating(self.line_container)
        # self.renderer.render(self.scene, self.camera)

    def angled_grating(self, angle):
            for r in np.arange(0, Z / 2, 0.2):
                x1 = r * np.cos(angle) + Z / 2 * np.sin(angle)
                y1 = r * np.sin(angle) + Z / 2 * np.cos(angle)
                x2 = r * np.cos(angle) - Z / 2 * np.sin(angle)
                y2 = r * np.sin(angle) - Z / 2 * np.cos(angle)

                x11 = r * np.cos(angle + np.pi) + Z / 2 * np.sin(angle + np.pi)
                y11 = r * np.sin(angle + np.pi) + Z / 2 * np.cos(angle + np.pi)
                x22 = r * np.cos(angle + np.pi) - Z / 2 * np.sin(angle + np.pi)
                y22 = r * np.sin(angle + np.pi) - Z / 2 * np.cos(angle + np.pi)

                l1 = LineGeometry(
                    x1 = x1,
                    x2 = x2,
                    y1 = y1,
                    y2 = y2
                )

                l2 = LineGeometry(
                    x1 = x11,
                    x2 = x22,
                    y1 = y11,
                    y2 = y22
                )
            
                material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
                self.line_container.append(Mesh(l1, material))
                self.line_container.append(Mesh(l2, material))
                self.scene.add(self.line_container[-1])
                self.scene.add(self.line_container[-2])

    def remove_grating(self):
        for i in range(0, len(self.line_container)):
            self.scene.remove(self.line_container[i])
        self.line_container = []


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
    
    def screen_recorder(self):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        pygame.image.save(screen_surf, f"../hilbert_color/{self.order}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        if self.pace == 0:
            self.angled_grating(self.angle) 
            self.angle += np.pi / 100
            self.pace += 1
        elif self.pace % 1 == 0:
            self.remove_grating()
            self.angled_grating(self.angle) 
            self.angle += np.pi / 100
            self.pace += 1
        else:
            self.pace += 1

        self.renderer.render(self.scene, self.camera)
        pass

t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


