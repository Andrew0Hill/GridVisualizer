import pygame
import OpenGL

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initial display size
DISPLAY_SIZE = [1000,750]

# Previous mouse position, used for computing the deltax and deltay for mouse drag movement.
prev_mouse_x = 0
prev_mouse_y = 0

# Offset amount. Sent to the gluOrtho2D command to translate the map in space.
offset_amt_x = 0
offset_amt_y = 0

# Boolean flag to signal if the mouse is moving or not.
dragging = False
def display():
	# Discovered Vertex 
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glColor3f(0.5,0.5,1.0)

	glBegin(GL_POINTS)
	glVertex2i(25,25)
	glEnd()
	
def setupScreen():
	global offset_amt_x
	global offset_amt_y
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPointSize(50)
	gluOrtho2D(0.0+offset_amt_x,DISPLAY_SIZE[0]+offset_amt_x,0.0+offset_amt_y,DISPLAY_SIZE[1]+offset_amt_y)
	
def handleEvents():
	global dragging
	global offset_amt_x
	global offset_amt_y
	global prev_mouse_x
	global prev_mouse_y
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		# Keep track of where the mouse moves, so that we can move around the map.
		elif event.type == pygame.MOUSEMOTION:			
			if dragging:
				offset_amt_x -= event.pos[0] - prev_mouse_x
				offset_amt_y += event.pos[1] - prev_mouse_y
				prev_mouse_x = event.pos[0]
				prev_mouse_y = event.pos[1]
				setupScreen()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				dragging = True
				prev_mouse_x = event.pos[0]
				prev_mouse_y = event.pos[1]
			elif event.button == 4:
				DISPLAY_SIZE[0] *= 2
				DISPLAY_SIZE[1] *= 2
				offset_amt_x = 0
				offset_amt_y = 0
				setupScreen()
			elif event.button == 5:
				DISPLAY_SIZE[0] /= 2
				DISPLAY_SIZE[1] /= 2
				offset_amt_x = 0
				offset_amt_y = 0
				setupScreen()
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				dragging = False
def main():
	pygame.init()

	pygame.display.set_mode(DISPLAY_SIZE,DOUBLEBUF|OPENGL)
	glClearColor(0,0,0,0)
	setupScreen()
	while True:
		handleEvents()
		display()
		pygame.display.flip()
		pygame.time.wait(10)


main()