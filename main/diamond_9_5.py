from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *
from core.shapes import circle, triangle, pentagon
from math import pi, sqrt

# render 2 shapes
class Test(Base):

    def initialize(self):
        print('Initializing program...')
        ### initialize program ###

        # vertex shader code 
        vsCode = """
        in vec3 position;
        void main()
        {
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """

        # fragment shader code
        fsCode = """
        out vec4 FragColor;
        void main()
        {
            FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        glLineWidth(3)

        ### setup vertex array object - circle ###
        self.vao_c1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c1)
        c1 = circle.Circle(0, 2 * pi, 1, 10000)
        positionData_c1 = c1.circle_array()
        self.vertexCount_c1 = len(positionData_c1)
        positionAttribute_c1 = Attribute("vec3", positionData_c1)
        positionAttribute_c1.associateVariable(self.programRef, "position")

        ### setup vertex array object - pentagon ###
        self.vao_p1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_p1)
        p1 = pentagon.Pentagon()
        positionData_p1 = p1.diamond_coords()
        self.vertexCount_p1 = len(positionData_p1)
        positionAttribute_p1 = Attribute("vec3", positionData_p1)
        positionAttribute_p1.associateVariable(self.programRef, "position")

        ### setup vertex array object - pentagon ###
        self.vao_t1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t1)
        positionData_t1 = [positionData_p1[1], positionData_p1[3], positionData_p1[4]]
        self.vertexCount_t1 = len(positionData_t1)
        positionAttribute_t1 = Attribute("vec3", positionData_t1)
        positionAttribute_t1.associateVariable(self.programRef, "position")

        ### setup vertex array object - pentagon ###
        self.vao_t2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t2)
        positionData_t2 = [positionData_p1[1], positionData_p1[4], positionData_p1[2]]
        self.vertexCount_t2 = len(positionData_t2)
        positionAttribute_t2 = Attribute("vec3", positionData_t2)
        positionAttribute_t2.associateVariable(self.programRef, "position")

        ### setup vertex array object - pentagon ###
        self.vao_t3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t3)
        positionData_t3 = [positionData_p1[0], positionData_p1[2], positionData_p1[3]]
        self.vertexCount_t3 = len(positionData_t3)
        positionAttribute_t3 = Attribute("vec3", positionData_t3)
        positionAttribute_t3.associateVariable(self.programRef, "position")

    
    def update(self):

        # select program to use when rendering
        glUseProgram(self.programRef)

        # draw the circle
        glBindVertexArray(self.vao_c1)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_c1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw the pentagon
        glBindVertexArray(self.vao_p1)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_p1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 1
        glBindVertexArray(self.vao_t1)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 2
        glBindVertexArray(self.vao_t2)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t2)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw triangle 3
        glBindVertexArray(self.vao_t3)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t3)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES
        
# instantiate this class and run the program
Test(screenSize=[1000, 1000]).run()