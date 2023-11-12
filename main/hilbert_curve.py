from operator import add, sub
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from math import sin, cos, tan, cosh, exp
from OpenGL.GL import *
from material.surfaceMaterial import SurfaceMaterial
from geometry.lineGeometry import LineGeometry

import pygame

WIDTH = 900
HEIGHT = 900
Z = 10  # Sets camera distance away from xy plane

def hilbert_x(order = 1):
    if order == 1:
        return [1, 1, 3, 3]
    elif order % 2 == 0: # even orders do not drop the last point in the subshape
        n = int(2 ** order)
        x_p = hilbert_x(order - 1)
        y_p = hilbert_y(order - 1)
        s1 = y_p
        s2 = x_p[1:]
        s3 = list(map(add, x_p[:-1], [n for i in range(0, len(x_p))][:-1]))
        s4 = list(map(sub, [n * 2 for i in range(0, len(x_p))], y_p))
        return s1 + s2 + s3 + s4
    elif order % 2 == 1 and order != 1:  # odd orders
        n = int(2 ** order)
        x_p = hilbert_x(order - 1)
        y_p = hilbert_y(order - 1)
        s1 = y_p[:-1]
        s2 = x_p[:-1]
        s3 = list(map(add, x_p[1:], [n for i in range(0, len(x_p))][1:]))
        s4 = list(map(sub, [2 * n for i in range(0, len(x_p))][1:], y_p[1:]))
        return s1 + s2 + s3 + s4

def hilbert_y(order = 1):
    if order == 1:
        return [1, 3, 3, 1]
    elif order % 2 == 0: # even orders do not drop the last point in the subshape
        n = int(2 ** order)
        x_p = hilbert_x(order - 1)
        y_p = hilbert_y(order - 1)
        s1 = x_p
        s2 = list(map(add, [n for i in range(0, len(y_p))][1:], y_p[1:]))
        s3 = list(map(add, [n for i in range(0, len(y_p))][:-1], y_p[:-1]))
        s4 = list(map(sub, [n for i in range(0, len(y_p))], x_p))
        return s1 + s2 + s3 + s4
    elif order % 2 == 1 and order != 1:  # odd orders
        n = int(2 ** order)
        x_p = hilbert_x(order - 1)
        y_p = hilbert_y(order - 1)
        s1 = x_p[:-1]
        s2 = list(map(add, [n for i in range(0, len(y_p))][:-1], y_p[:-1]))
        s3 = list(map(add, y_p[1:], [n for i in range(0, len(y_p))][1:]))
        s4 = list(map(sub, [n for i in range(0, len(x_p))][1:], x_p[1:]))
        return s1 + s2 + s3 + s4
        
x_coords = []
y_coords = []
for i in range(1, 10):
    x_coords.append(hilbert_x(i))
    y_coords.append(hilbert_y(i))

# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.line_container = []
        self.pace = 0
        self.order = 1

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


        self.renderer.render(self.scene, self.camera) 


    def material_gen(self, r, g, b, draw_style = GL_LINE_STRIP):
        material = SurfaceMaterial(
            {
                'useVertexColors': True,
                'wireframe': True,
                'lineWidth': 1,
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

        if self.pace % 100 == 0:
            for l in self.line_container:
                self.scene.remove(l)

            self.line_container = []

            for i in range(0, len(x_coords[self.order - 1]) - 1):
                x1 = (Z / 4 * x_coords[self.order - 1][i] / (2 ** (self.order - 1)) - Z / 2)
                x2 = (Z / 4 * x_coords[self.order - 1][i + 1] / (2 ** (self.order - 1)) - Z / 2)
                y1 = (Z / 4 * y_coords[self.order - 1][i] / (2 ** (self.order - 1)) - Z / 2)
                y2 = (Z / 4 * y_coords[self.order - 1][i + 1] / (2 ** (self.order - 1)) - Z / 2)
                self.geometry = LineGeometry(
                    x1 = x1,
                    x2 = x2,
                    y1 = y1,
                    y2 = y2
                )
            
                material = self.material_gen(r = abs(x1), g = abs(x2), b = abs(y1))
                self.line_container.append(Mesh(self.geometry, material))
                self.scene.add(self.line_container[i])

            self.screen_recorder()
            
            self.order += 1
            

        
        self.pace += 1
        self.renderer.render(self.scene, self.camera) 

Test(screenSize = [WIDTH, HEIGHT]).run()
    


