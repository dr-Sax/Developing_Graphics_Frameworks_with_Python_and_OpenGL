from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from OpenGL.GL import *
from core.shapes import circle, triangle
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
            FragColor = vec4(1.0, 1.0, 1.0, 1.0);
        }
        """

        # send code to GPU and compile; store program reference
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        ### render settings (optional) ###
        glLineWidth(1)

        ### setup vertex array object - circle ###
        self.vao_c1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c1)
        c1 = circle.Circle(0, 2 * pi, 1, 10000)
        positionData_c1 = c1.circle_array()
        self.vertexCount_c1 = len(positionData_c1)
        positionAttribute_c1 = Attribute("vec3", positionData_c1)
        positionAttribute_c1.associateVariable(self.programRef, "position")

        ### setup vertex array object - triangle ###
        self.vao_t1 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t1)
        t1 = triangle.Triangle(0, 0, sqrt(3))
        positionData_t1 = t1.equilateral_triangle_array()
        self.vertexCount_t1 = len(positionData_t1)
        positionAttribute_t1 = Attribute("vec3", positionData_t1)
        positionAttribute_t1.associateVariable(self.programRef, "position")

        ### setup vertex array object - circle ###
        self.vao_c2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c2)
        c2 = circle.Circle(0, 2 * pi, 1 / 2, 10000)
        positionData_c2 = c2.circle_array()
        self.vertexCount_c2 = len(positionData_c2)
        positionAttribute_c2 = Attribute("vec3", positionData_c2)
        positionAttribute_c2.associateVariable(self.programRef, "position")

        ### setup vertex array object - triangle ###
        self.vao_t2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t2)
        t2 = triangle.Triangle(0, 0, 1 / 2 * sqrt(3))
        positionData_t2 = t2.equilateral_triangle_array()
        self.vertexCount_t2 = len(positionData_t2)
        positionAttribute_t2 = Attribute("vec3", positionData_t2)
        positionAttribute_t2.associateVariable(self.programRef, "position")

        ### setup vertex array object - circle ###
        self.vao_c3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c3)
        c3 = circle.Circle(0, 2 * pi, 1 / 4, 10000)
        positionData_c3 = c3.circle_array()
        self.vertexCount_c3 = len(positionData_c2)
        positionAttribute_c3 = Attribute("vec3", positionData_c3)
        positionAttribute_c3.associateVariable(self.programRef, "position")

        ### setup vertex array object - triangle ###
        self.vao_t3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_t3)
        t3 = triangle.Triangle(0, 0, 1 / 4 * sqrt(3))
        positionData_t3 = t3.equilateral_triangle_array()
        self.vertexCount_t3 = len(positionData_t3)
        positionAttribute_t3 = Attribute("vec3", positionData_t3)
        positionAttribute_t3.associateVariable(self.programRef, "position")

        ### setup vertex array object - circle ###
        self.vao_c4 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_c4)
        c4 = circle.Circle(0, 2 * pi, 1 / 8, 10000)
        positionData_c4 = c4.circle_array()
        self.vertexCount_c4 = len(positionData_c2)
        positionAttribute_c4 = Attribute("vec3", positionData_c4)
        positionAttribute_c4.associateVariable(self.programRef, "position")
        
    
    def update(self):

        # select program to use when rendering
        glUseProgram(self.programRef)

        # draw the circle
        glBindVertexArray(self.vao_c1)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_c1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES
        
        # draw the triangle
        glBindVertexArray(self.vao_t1)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t1)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

                # draw the circle
        glBindVertexArray(self.vao_c2)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_c2)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        # draw the triangle
        glBindVertexArray(self.vao_t2)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t2)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        glBindVertexArray(self.vao_c3)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_c3)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES
        # draw the triangle
        glBindVertexArray(self.vao_t3)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_t3)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES

        glBindVertexArray(self.vao_c4)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount_c4)  # LINE_STRIP, LINES, LINE_LOOP, TRIANGLE_FAN, TRIANGLES
        

# instantiate this class and run the program
Test(screenSize=[1000, 1000]).run()