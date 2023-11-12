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
NUM_POINTS = 70
SIZE = Z / 3
RADIUS = 1


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
        self.pace = 0
        self.angle = 0
        self.renderer.render(self.scene, self.camera)

    
    def angled_grating(self, n = 1/2):
        for i in np.linspace(-Z / 2, Z / 2, int(n * Z / RADIUS)):
            for j in np.linspace(-Z / 2, Z / 2, int(n * Z / RADIUS)):
                p1 = PolygonGeometry(
                    sides = 6,
                    radius = RADIUS,
                    x = i,
                    y = j,
                )

                material = self.material_gen(r = 1.0, g = 1.0, b = 1.0)
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
        pygame.image.save(screen_surf, f"../hexagons/{angle}.jpg")
    
    
    # 180 bpm = 3 beats per second... a beat every .33333 secs
    def update(self):
        if self.pace == 0:
            self.angled_grating() 
            
        elif self.iter % 64 == 0:
            self.remove_grating()
            self.angled_grating(n = self.pace) 
            
            self.renderer.render(self.scene, self.camera)
            self.screen_recorder(angle = self.iter)
        self.pace += np.pi / 2000
        self.iter += 1
        



t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


