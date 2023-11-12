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
SIZE = Z / 3
RADIUS = 1/4


# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.line_container = []
        self.iter = 0


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
        self.angle = 0
        self.renderer.render(self.scene, self.camera)

    def hex_orbit(self, xc, yc, phi, r1, r2):
        h1 = PolygonGeometry(
            sides = 6,
            radius = r1,
            x = xc,
            y = yc,
            theta1 = 0,
            theta2 = 2 * np.pi
        )
        h2 = PolygonGeometry(
            sides = 6,
            radius = r2,
            x = xc + (r1 / 2) + r2 * np.sin(phi - 5 * np.pi / 6),
            y = yc + (-r1 * np.sqrt(3) / 2) + r2 * np.cos(phi - 5 * np.pi / 6),
            
            theta1 = phi,
            theta2 = 2 * np.pi + phi
        )

        material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
        self.point_container.append(Mesh(h1, material))
        self.scene.add(self.point_container[-1])
        self.point_container.append(Mesh(h2, material))
        self.scene.add(self.point_container[-1])
        
    def remove_hex(self):
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
        pygame.image.save(screen_surf, f"../hexagons/{angle}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        if self.angle == 0:
            self.hex_orbit(0, 0, 0, 2, 2)

        else:
            self.remove_hex()
            self.hex_orbit(0, 0, self.angle, 2, 2)

        self.angle += pi/200
        
        self.renderer.render(self.scene, self.camera)
        
        



t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


