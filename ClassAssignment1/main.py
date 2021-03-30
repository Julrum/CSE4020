import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gXAng = 0.
gYAng = 0.
gZAng = 0.
cx = 0.
cy = 0
lx = 0
ly = 0.
leftButton = 0
rightButton = 0

# draw a cube of side 1, centered at the origin.
def drawGrid(M):
  glBegin(GL_LINES)
  glVertex3fv(M @ np.array([ 0., 0., 0.]))
  glVertex3fv(M @ np.array([20., 0., 0.]))
  glVertex3fv(M @ np.array([ 0., 0., 0.]))
  glVertex3fv(M @ np.array([ 0., 0.,20.]))
  glEnd()
  glRotatef(45, 0, 0, 1);
  glRotatef(90, 0, 1, 0);
  glTranslatef(-1, -1, 0);

def drawGridArray(M):
  for i in range(-20, 20):
    for j in range(-20, 20):
      glPushMatrix()
      glTranslatef(i,0, j)
      drawGrid(M)
      glPopMatrix()

def drawFrame(M):
  glBegin(GL_LINES)
  glColor3ub(255, 0, 0)
  glVertex3fv(M @ np.array([ 0.,0.,0.]))
  glVertex3fv(M @ np.array([20.,0.,0.]))
  glColor3ub(0, 255, 0)
  glVertex3fv(M @ np.array([0.,0.,0.]))
  glVertex3fv(M @ np.array([0.,20.,0.]))
  glColor3ub(0, 0, 255)
  glVertex3fv(M @ np.array([0.,0.,0]))
  glVertex3fv(M @ np.array([0.,0.,20.]))
  glEnd()

def render(M):
  global gXAng, gYAng, gZAng
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

  glLoadIdentity()

  # test other parameter values
  glOrtho(-10,10, -10,10, -10,10)

  # gluLookAt(1*np.sin(gCamAng),gCamHeight,1*np.cos(gCamAng), 0,0,0, 0,1,0)
  
  glRotatef(gXAng, 1, 0, 0)
  glRotatef(gYAng, 0, 1, 0)
  glRotatef(gZAng, 0, 0, 1)
  glTranslatef(0, 0, 0)
  drawFrame(M)
  glColor3ub(255, 255, 255)

  # drawGrid()

  # test 

  drawGridArray(M)

def cursor_callback(window, xpos, ypos):
  global gXAng, gYAng, cx, cy, lx, ly, leftButton, rightButton
  if leftButton == 0:
    cx = xpos
    cy = ypos
    print('x: %d, y: %d'%(cx, cy))
  elif leftButton == 1:
    dx = cx - xpos
    dy = cy - ypos
    print('dx: %d dy: %d'%(dx, dy))
    gYAng = dx
    gXAng = dy
  
def button_callback(window, button, action, mod):
  global gXAng, gYAng, leftButton, rightButton
  if button==glfw.MOUSE_BUTTON_LEFT:
    if action==glfw.PRESS:
      leftButton = 1
      print('press left btn: (%d, %d)'%glfw.get_cursor_pos(window))
    elif action==glfw.RELEASE:
      print('release left btn: (%d, %d)'%glfw.get_cursor_pos(window))
      leftButton = 0
  if button==glfw.MOUSE_BUTTON_RIGHT:
    if action==glfw.PRESS:
      rightButton = 1
      print('press left btn: (%d, %d)'%glfw.get_cursor_pos(window))
    elif action==glfw.RELEASE:
      print('release left btn: (%d, %d)'%glfw.get_cursor_pos(window))
      rightButton = 0

def scroll_callback(window, xoffset, yoffset):
  print('mouse wheel scroll: %d, %d'%(xoffset, yoffset))

def key_callback(window, key, scancode, action, mods):
  global gXAng, gYAng, gZAng
  if action==glfw.PRESS or action==glfw.REPEAT:
    if key==glfw.KEY_1:
      gXAng += 10
    elif key==glfw.KEY_3:
      gZAng += 10
    elif key==glfw.KEY_2:
      gYAng += 10
    elif key==glfw.KEY_W:
      gYAng = 0
      gXAng = 0
      gZAng = 0

def main():
  if not glfw.init():
    return
  window = glfw.create_window(480,480,'title', None,None)
  if not window:
    glfw.terminate()
    return
  glfw.make_context_current(window)
  glfw.set_key_callback(window, key_callback)
  glfw.set_cursor_pos_callback(window, cursor_callback)
  glfw.set_mouse_button_callback(window, button_callback)
  glfw.set_scroll_callback(window, scroll_callback)


  while not glfw.window_should_close(window):
    glfw.poll_events()
    # gluLookAt(1*np.sin(gCamAng),gCamHeight,1*np.cos(gCamAng), 0,0,0, 0,1,0)
    render(np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]))
    glRotatef(45, 0, 0, 1)
    glRotatef(90, 0, 1, 0)
    glTranslatef(-1, -1, 0)
    glfw.swap_buffers(window)

  glfw.terminate()

if __name__ == "__main__":
  main()

