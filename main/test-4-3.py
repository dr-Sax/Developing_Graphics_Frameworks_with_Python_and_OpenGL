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
from geometry.geometry import Geometry
from math import sin
from numpy import arange
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial

# render a basic scene
class Test(Base):

    def initialize(self):
        print('Initializing program...')

        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio = 800 / 600)
        self.camera.setPosition([0, 0, 10])

        geometry = Geometry()
        posData = []
        for x in arange(-3.2, 3.2, 0.3):
            posData.append([x, sin(x), 0])
        geometry.addAttribute('vec3', 'vertexPosition', posData)
        geometry.countVertices()

        pointMaterial = PointMaterial(
            {
                'baseColor': [1, 1, 0],
                'pointSize': 10,
            },
            lineColor=[1.0,1.0, 1.0]
        )
        pointMesh = Mesh(geometry, pointMaterial)
        
        lineMaterial = LineMaterial(
            {
                'baseColor': [1, 0, 1],
                'lineWidth': 4                
            }
        )
        lineMesh = Mesh(geometry, lineMaterial)

        self.scene.add(pointMesh)
        self.scene.add(lineMesh)

        self.renderer.render(self.scene, self.camera)

# instantiate this class and run the program
Test(screenSize = [800, 600]).run()

