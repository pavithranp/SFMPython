/*

quad.cc - Simple Quad program
*/

#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include <stdlib.h>
#include <iostream>
using namespace std;
void quad()
{
glBegin(GL_QUADS);
glVertex2f( 0.0f, 1.0f); // Top Left
glVertex2f( 1.0f, 1.0f); // Top Right
glVertex2f( 1.0f, 0.0f); // Bottom Right
glVertex2f( 0.0f, 0.0f); // Bottom Left
glEnd();
}

void draw()
{
// Make background colour black
glClearColor( 0, 0, 0, 0 );
glClear ( GL_COLOR_BUFFER_BIT );

    // Push the matrix stack - more on this later
    glPushMatrix();

    // Set drawing colour to blue
    glColor3f( 0, 0, 1 );

    // Move the shape to middle of the window
    // More on this later
    glTranslatef(-0.5, -0.5, 0.0);

    // Call our Quad Method
    quad();

    // Pop the Matrix
    glPopMatrix();

    // display it 
    glutSwapBuffers();
}

// Keyboard method to allow ESC key to quit
void keyboard(unsigned char key,int x,int y)
{
    
if(key==27)
std::cout<<"exiting"; exit(0);
}

int main(int argc, char **argv)
{

	glutInit( & argc, argv );
	// Double Buffered RGB display
glutInitDisplayMode( GLUT_RGB | GLUT_DOUBLE);
// Set window size
glutInitWindowSize( 500,500 );
glutCreateWindow("Test");
// Declare the display and keyboard functions
glutDisplayFunc(draw);
glutKeyboardFunc(keyboard);
// Start the Main Loop
glutMainLoop();
}
