from operator import add, sub
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from math import sin, cos, tan, cosh, exp, pi
from OpenGL.GL import *
from material.surfaceMaterial import SurfaceMaterial
from geometry.polygonGeometry import PolygonGeometry
import numpy as np
import pygame
from time import sleep

WIDTH = 1080
HEIGHT = 1350
Z = 12  # Sets camera distance away from xy plane

K = [
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
]

i = [
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 1]
]

n = [
    [1, 1, 1, 1, 0], 
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1]
]

d = [
    [0, 0, 0, 1, 1], 
    [0, 0, 0, 1, 1], 
    [0, 1, 1, 1, 1], 
    [1, 1, 0, 1, 1], 
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1]
]

o = [
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0]
]

f = [
    [0, 0, 1, 1], 
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
]

c = [
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0]
]

s = [
    [0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0]
]

v = [
    [0, 1, 1, 0], 
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1]
]

e = [
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0]
]

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

        self.point_container = []
        self.point_container2 = []
        self.letter_list = [K, i, n, d, o, f, c, o, n, s, i, s, v, e, n, v]
        self.letter_sp   = [4500, 4000, 3700, 3300, 2700, 2600, 7503, 7550, 7650, 7820, 8000, 8200, 8500, 8800, 9200, 9700]
        self.point_list = []
        self.pace = 0
        self.angle = 0
        self.inf_sign()

        self.renderer.render(self.scene, self.camera)

    def inf_sign(self, theta0 = 0, thetaf = 2 * pi):

        for theta in np.linspace(self.angle, 2 * pi + self.angle, 150):
            A = 3
            r = A * np.sqrt(np.cos(2*theta))
            if theta % 2 * pi < pi:
                cir_r = 8 * sin(self.angle) + 0.01
            else:
                cir_r = 8 * cos(self.angle) + 0.01
            p1 = PolygonGeometry(
                sides = 100,
                radius = cir_r,
                x = r * np.cos(theta),
                y = r * np.sin(theta),
            )

            
            material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
            self.point_container.append(Mesh(p1, material))
            self.scene.add(self.point_container[-1])

    def letter(self, l, x0 = 0, y0 = 0):
        for y in range(0, len(l)):
            for x in range(0, len(l[y])):
                A = 3
                s = 0.05
                if l[y][x] == 1:
                    p1 = PolygonGeometry(
                        sides = 50,
                        radius = 0.01 * sin(self.angle),
                        x = x0 + s * x,
                        y = y0 - s * y,
                    )

                
                    material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
                    self.point_container.append(Mesh(p1, material))
                    self.scene.add(self.point_container[-1])

    def letter_sign(self):
        self.point_list = []
        for theta in np.linspace(np.pi / 2 + self.angle, np.pi + self.angle, 5000):
            A = 3
            r = A * np.sqrt(np.cos(2 * theta))
            x = r * np.cos(theta),
            y = r * np.sin(theta),
            self.point_list.append([x, y])
                
        for theta in np.linspace(3 * np.pi / 2 + self.angle, 2 * np.pi + self.angle, 5000):
            A = 3
            r = A * np.sqrt(np.cos(2 * theta))
            x = r * np.cos(theta),
            y = r * np.sin(theta),
            self.point_list.append([x, y])

        scale = int(2000 / 16)

        for i in range(0, len(self.letter_list)):
            
            try:
                self.letter(
                    self.letter_list[i], 
                    x0 = self.point_list[self.letter_sp[i]][0][0], 
                    y0 = self.point_list[self.letter_sp[i]][1][0]
                    )
            except:
                self.letter(self.letter_list[i])

    

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
        pygame.image.save(screen_surf, f"../dot_overlap/{round(angle, 4)}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        pass
        if self.pace % 30 == 0 and self.angle == 0:
            self.inf_sign()
            self.angle += np.pi / 100
            self.renderer.render(self.scene, self.camera)
        else:
            self.remove_grating()
            self.inf_sign()
            self.angle += np.pi / 500
            self.renderer.render(self.scene, self.camera)
        # #self.screen_recorder(angle = 180 / np.pi * (self.angle / 2 + 120 / 180 * np.pi))
        self.pace += 1



t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
        
        
        
        