import pygame
import OpenGL
import rospy


from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from nav_msgs.msg import GridCells
from geometry_msgs.msg import Point
# Initial display size
DISPLAY_SIZE = [1000,750]

# Scalar value for zoom per scroll wheel click
DEFAULT_ZOOM = 2

# Scalar value for default point size
DEFAULT_POINT_SIZE = 5

# Scalar value for grid square size
HALF_GRID_SIZE = 2.5

# Previous mouse position, used for computing the deltax and deltay for mouse drag movement.
prev_mouse_x = 0
prev_mouse_y = 0

# Offset amount. Sent to the gluOrtho2D command to translate the map in space.
offset_amt_x = 0
offset_amt_y = 0

# Boolean flag to signal if the mouse is moving or not.
dragging = False
def display():
	# Clear the screen
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	# Set first color
	glColor3f(0.5,0.5,1.0)

	# Draw each point
	glBegin(GL_POINTS)
	
	
	glVertex2f(HALF_GRID_SIZE,HALF_GRID_SIZE)
	glEnd()

# Callback for Occupancy Grid topic
def oc_update():
	print("Activity on occupancy grid topic")
# Callback for Occupancy Grid Update topic.
def ocu_update():
	print("Activity on occupancy grid update topic")
# Zooms out screen by scaling factor 'inc'
def zoomOut(inc):
	global DEFAULT_POINT_SIZE
	global DEFAULT_ZOOM
	global HALF_GRID_SIZE
	DISPLAY_SIZE[0] /= inc
	DISPLAY_SIZE[1] /= inc
	DEFAULT_POINT_SIZE /= inc
	HALF_GRID_SIZE /= 2*inc
	offset_amt_x = 0
	offset_amt_y = 0
	setupScreen()

# Zooms in screen by scaling factor 'inc'
def zoomIn(inc):
	global DEFAULT_POINT_SIZE
	global DEFAULT_ZOOM
	global HALF_GRID_SIZE
	DISPLAY_SIZE[0] *= DEFAULT_ZOOM
	DISPLAY_SIZE[1] *= DEFAULT_ZOOM
	DEFAULT_POINT_SIZE *= DEFAULT_ZOOM
	HALF_GRID_SIZE *= 4
	offset_amt_x = 0
	offset_amt_y = 0
	setupScreen()

# Sets up the screen for drawing.
# Uses Orthographic 2D projection.
def setupScreen():
	global offset_amt_x
	global offset_amt_y
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glPointSize(DEFAULT_POINT_SIZE)
	gluOrtho2D(0.0+offset_amt_x,DISPLAY_SIZE[0]+offset_amt_x,0.0+offset_amt_y,DISPLAY_SIZE[1]+offset_amt_y)

# Main event handler for pygame (keyboard/mouse) events
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
			# Zooms in with scroll wheel. calls setupScreen()
			elif event.button == 4:
				zoomIn(DEFAULT_ZOOM)
			# Zooms out with scroll wheel. calls setupScreen()
			elif event.button == 5:
				zoomOut(DEFAULT_ZOOM)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				dragging = False
def main():
	pygame.init()

	pygame.display.set_mode(DISPLAY_SIZE,DOUBLEBUF|OPENGL)
	glClearColor(0,0,0,0)
	setupScreen()
	# Initialize the node with the name 'cmap_listener'
	#rospy.init_node('cmap_listener')

	# Subscribe to /move_base/global_costmap/costmap and 
	# /move_base/global_costmap/costmap_update
	#rospy.Subscriber("/move_base/global_costmap/costmap",100,oc_update)
	#rospy.Subscriber("/move_base/global_costmap/costmap_update",100,ocu_update)


	while True:
		handleEvents()
		display()
		pygame.display.flip()
		pygame.time.wait(10)


main()
