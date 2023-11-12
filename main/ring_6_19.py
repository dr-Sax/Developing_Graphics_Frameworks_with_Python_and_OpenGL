# Internal Packages
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from material.surfaceMaterial import SurfaceMaterial
from geometry.polygonGeometry import PolygonGeometry

from operator import add, sub
from math import sin, cos, tan, cosh, exp, pi
from OpenGL.GL import *
import numpy as np
import pygame
from time import sleep
import cv2

# Constants:
WIDTH = 1080
HEIGHT = 1080
Z = 10  # Sets camera distance away from xy plane
SIZE = Z / 3
RADIUS = 1/15
IMAGE = cv2.imread('hand_outline.png')
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

# render a basic scene
class Test(Base):

    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = WIDTH / HEIGHT)
        self.camera.setPosition([0, 0, Z])
        self.renderer.render(self.scene, self.camera)
        
        self.iter0 = 0
        self.iter = self.iter0
        self.angle = self.iter0 * pi / 1000
        self.time = 0

        self.line_container = []
        self.point_container = []
        self.point_container2 = []
        self.point_container3 = []
        
        self.cnts = self.contour_from_image(image = IMAGE)

              
    def contour_from_image(self, image = IMAGE):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 120, 255, 1)
        cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]  
        return cnts

    # from: https://medium.com/analytics-vidhya/tutorial-how-to-scale-and-rotate-contours-in-opencv-using-python-f48be59c35a2
    def scale_contour(self, cnt, scale = 1):
        M = cv2.moments(cnt)
        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        except:
            cx = 0
            cy = 0

        cnt_norm = cnt - [cx, cy]
        cnt_scaled = cnt_norm * scale
        cnt_scaled = cnt_scaled + [cx, cy]
        cnt_scaled = cnt_scaled.astype(np.int32)

        return cnt_scaled
    
    def cart2pol(self, x, y):
        theta = np.arctan2(y, x)
        rho = np.hypot(x, y)
        return theta, rho


    def pol2cart(self, theta, rho):
        x = rho * np.cos(theta)
        y = rho * np.sin(theta)
        return x, y


    def rotate_contour(self, cnt, angle):
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cnt_norm = cnt - [cx, cy]
        
        coordinates = cnt_norm[:, 0, :]
        xs, ys = coordinates[:, 0], coordinates[:, 1]
        thetas, rhos = self.cart2pol(xs, ys)
        
        thetas = np.rad2deg(thetas)
        thetas = (thetas + angle) % 360
        thetas = np.deg2rad(thetas)
        
        xs, ys = self.pol2cart(thetas, rhos)
        
        cnt_norm[:, 0, 0] = xs
        cnt_norm[:, 0, 1] = ys

        cnt_rotated = cnt_norm + [cx, cy]
        cnt_rotated = cnt_rotated.astype(np.int32)

        return cnt_rotated
    
    def set_cnts(self, scale):
        for i in range(0, len(self.cnts[0])):
            self.cnts[0][i] = self.scale_contour(self.cnts[0][i], scale = scale)

    def remove_hex1(self):
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
    
    def screen_recorder(self, file_name):
        screen = pygame.display.get_surface()
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        screen_surf = pygame.image.fromstring(buffer, size, "RGBA")
        screen_surf = pygame.transform.flip(screen_surf, True, True)
        pygame.image.save(screen_surf, f"../twin_snakes/{file_name}.jpg")

    def ring_pts(self, r0, phi, color, a, n, t, poly_radius):
        n_dots = int(np.pi * r0 / poly_radius)
        namp = n
        for theta in np.linspace(0, 2 * np.pi, n_dots, endpoint=False):
            n = namp
            x0 = (r0 + a * np.sin(n * (theta + t))) * np.cos(theta)
            y0 = (r0 + a * np.sin(n * (theta + t)))* np.sin(theta)
            p1 = PolygonGeometry(
                sides = 20,
                radius = poly_radius,
                x = x0,
                y = y0,
                theta1 = phi,
                theta2 = 2 * np.pi + phi
            )

            material = self.material_gen(r = color[0], g = color[1], b = color[2])
            self.point_container.append(Mesh(p1, material))
            self.scene.add(self.point_container[-1])


                

    def ring(self, r0, phi, color, pr, a, n, t):
        self.ring_pts(r0, phi, color, a, n, t, poly_radius = pr)
        
        

    ## main loop ##  (At 60 fps, this runs once every 0.017 secs.)

    def update(self):
        nmax = 5
        nmin = 2
        namp = 1 / 2 * (nmax - nmin)

        pr = 0.3
        
        a = 5
        r0 = 4.98
        
        if self.time == 0:
            self.ring(r0 = r0, phi = 0, color = [0.0, abs(1.0*cos(1/2*self.time)), abs(1.0*sin(1/2*self.time))], pr = pr, a = a, n = 1/2, t = -self.time)
            self.ring(r0 = r0, phi = 0, color = [0.0, abs(1.0*cos(1/2*self.time)), abs(1.0*sin(1/2*self.time))], pr = pr, a = a, n = 1/2, t = self.time)
            self.renderer.render(self.scene, self.camera)
            #self.screen_recorder(self.iter)
        else:
            self.remove_hex1()
            self.remove_hex1()
            self.ring(r0 = r0, phi = 0, color = [0.0, abs(1.0*cos(1/2*self.time)), abs(1.0*sin(1/2*self.time))], pr = pr, a = a, n = 1/2, t = -self.time)
            self.ring(r0 = r0, phi = 0, color = [0.0, abs(1.0*cos(1/2*self.time)), abs(1.0*sin(1/2*self.time))], pr = pr, a = a, n = 1/2, t = self.time)
            self.renderer.render(self.scene, self.camera)
            #self.screen_recorder(self.iter)

        self.time += pi/21000000000
        self.iter +=1


t = Test(screenSize = [WIDTH, HEIGHT])
t.run()
    


