from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from geometry.sphereGeometry import SphereGeometry
from geometry.cylinderGeometry import CylinderGeometry
from geometry.pyramidGeometry import PyramidGeometry
from material.surfaceMaterial import SurfaceMaterial
from OpenGL.GL import *

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800 / 600)
        self.camera.setPosition([0, 0, 2])

        geometry = PyramidGeometry(heightSegments = 10000)
        material = SurfaceMaterial(
            {
                'useVertexColors': True,
                'wireframe': True,
                'drawStyle': GL_LINE_LOOP}  ## LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        )
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotateY(0.0514)
        self.mesh.rotateX(0.0337)
        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()
