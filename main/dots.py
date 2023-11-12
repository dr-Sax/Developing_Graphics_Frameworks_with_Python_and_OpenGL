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
HEIGHT = 1350
Z = 12  # Sets camera distance away from xy plane
NUM_POINTS = 50


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
        self.pace = 0
        self.angle = 0

        # self.angled_grating(self.angle)
        # self.angled_grating(15 * np.pi / 180)
        self.renderer.render(self.scene, self.camera)


    def angled_grating(self, angle):
        for r in np.arange(0, Z / 3, 0.2):
            x1 = r * np.cos(angle) - Z / 2 * np.sin(angle)
            y1 = r * np.sin(angle) + Z / 2 * np.cos(angle)
            x2 = r * np.cos(angle) + Z / 2 * np.sin(angle)
            y2 = r * np.sin(angle) - Z / 2 * np.cos(angle)

            x11 = r * np.cos(angle + np.pi) - Z / 2 * np.sin(angle + np.pi)
            y11 = r * np.sin(angle + np.pi) + Z / 2 * np.cos(angle + np.pi)
            x22 = r * np.cos(angle + np.pi) + Z / 2 * np.sin(angle + np.pi)
            y22 = r * np.sin(angle + np.pi) - Z / 2 * np.cos(angle + np.pi)

            x1_ls = np.linspace(x1, x2, NUM_POINTS)
            x2_ls = np.linspace(x11, x22, NUM_POINTS)
            y1_ls = np.linspace(y1, y2, NUM_POINTS)
            y2_ls = np.linspace(y11, y22, NUM_POINTS)

            for i in range(0, len(x1_ls)):
                p1 = PolygonGeometry(
                    sides = 5,
                    radius = 0.01,
                    x = x1_ls[i],
                    y = y1_ls[i],
                )

                p2 = PolygonGeometry(
                    sides = 5,
                    radius = 0.01,
                    x = x2_ls[i],
                    y = y2_ls[i],
                )
                material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
                self.point_container.append(Mesh(p1, material))
                self.point_container.append(Mesh(p2, material))
                self.scene.add(self.point_container[-1])
                self.scene.add(self.point_container[-2])

    def angled_grating2(self, angle):
        for r in np.arange(0, Z / 3, 0.2):
            x1 = r * np.cos(angle) - Z / 2 * np.sin(angle)
            y1 = r * np.sin(angle) + Z / 2 * np.cos(angle)
            x2 = r * np.cos(angle) + Z / 2 * np.sin(angle)
            y2 = r * np.sin(angle) - Z / 2 * np.cos(angle)

            x11 = r * np.cos(angle + np.pi) - Z / 2 * np.sin(angle + np.pi)
            y11 = r * np.sin(angle + np.pi) + Z / 2 * np.cos(angle + np.pi)
            x22 = r * np.cos(angle + np.pi) + Z / 2 * np.sin(angle + np.pi)
            y22 = r * np.sin(angle + np.pi) - Z / 2 * np.cos(angle + np.pi)

            x1_ls = np.linspace(x1, x2, NUM_POINTS)
            x2_ls = np.linspace(x11, x22, NUM_POINTS)
            y1_ls = np.linspace(y1, y2, NUM_POINTS)
            y2_ls = np.linspace(y11, y22, NUM_POINTS)

            for i in range(0, len(x1_ls)):
                p1 = PolygonGeometry(
                    sides = 5,
                    radius = 0.01,
                    x = x1_ls[i],
                    y = y1_ls[i],
                )

                p2 = PolygonGeometry(
                    sides = 5,
                    radius = 0.01,
                    x = x2_ls[i],
                    y = y2_ls[i],
                )
        
                material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
                self.point_container2.append(Mesh(p1, material))
                self.point_container2.append(Mesh(p2, material))
                self.scene.add(self.point_container2[-1])
                self.scene.add(self.point_container2[-2])

    def remove_grating(self):
        for i in range(0, len(self.point_container)):
            self.scene.remove(self.point_container[i])
        self.point_container = []

    def remove_grating2(self):
        for i in range(0, len(self.point_container2)):
            self.scene.remove(self.point_container2[i])
        self.point_container2 = []
    

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
        pygame.image.save(screen_surf, f"../dot_overlap/{round(angle, 4)}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        if self.pace == 0:
            self.angled_grating(0) 
            self.angled_grating2(self.angle / 2 + 120 / 180 * np.pi) 
            self.angle += np.pi / 200
            
        elif self.pace % 3 == 0:
            self.remove_grating()
            self.remove_grating2()
            self.angled_grating(0) 
            self.angled_grating2(self.angle / 2 + 120 / 180 * np.pi) 
            self.angle += np.pi / 200
            
        self.renderer.render(self.scene, self.camera)
        self.screen_recorder(angle = 180 / np.pi * (self.angle / 2 + 120 / 180 * np.pi))
        self.pace += 1



t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


