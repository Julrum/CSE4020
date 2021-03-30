import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gXAng = 0.
gYAng = 0.
gXTrans = 0.
gYTrans = 0.
gZTrans = 0.
cx = 0.
cy = 0.
lAx = 0.
lAy = 0.
lTx = 0.
lTy = 0.
leftButton = 0
rightButton = 0

def drawGrid():
  glBegin(GL_LINES)
  glVertex3f( 0., 0., 0.)
  glVertex3f(20., 0., 0.)
  glVertex3f( 0., 0., 0.)
  glVertex3f( 0., 0.,20.)
  glEnd()
  
def drawGridArray():
  for i in range(-20, 20):
    for j in range(-20, 20):
      glPushMatrix()
      glTranslatef(i,0, j)
      drawGrid()
      glPopMatrix()

def drawFrame():
  glBegin(GL_LINES)
  glColor3ub(255, 0, 0)
  glVertex3f( 0.,0.,0.)
  glVertex3f(20.,0.,0.)
  glColor3ub(0, 255, 0)
  glVertex3f(0.,0.,0.)
  glVertex3f(0.,20.,0.)
  glColor3ub(0, 0, 255)
  glVertex3f(0.,0.,0)
  glVertex3f(0.,0.,20.)
  glEnd()

def render():
  global gXAng, gYAng, gXTrans, gYTrans, gZTrans
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

  glLoadIdentity()

  # test other parameter values
  glOrtho(-10,10, -10,10, -10,10)

  glRotatef(gXAng, 1, 0, 0)
  glRotatef(gYAng, 0, 1, 0)
  glTranslatef(gXTrans, gYTrans, gZTrans)
  drawFrame()
  glColor3ub(255, 255, 255)

  drawGridArray()

def cursor_callback(window, xpos, ypos):
  global gXAng, gYAng, cx, cy, lAx, lAy, lTx, lTy, leftButton, rightButton, gXTrans, gYTrans
  if leftButton == 0 and rightButton == 0:
    cx = xpos
    cy = ypos
  elif leftButton == 1:
    dx = cx - xpos
    dy = cy - ypos
    gYAng = lAx + dx
    gXAng = lAy + dy
  elif rightButton == 1:
    dx = cx - xpos
    dy = cy - ypos
    gXTrans = lTx + dx*0.0416
    gYTrans = lTy + dy*0.0416
  
def button_callback(window, button, action, mod):
  global gXAng, gYAng, gXTrans, gYTrans, leftButton, rightButton, lAx, lAy, lTx, lTy, dx, dy
  if button==glfw.MOUSE_BUTTON_LEFT:
    if action==glfw.PRESS:
      leftButton = 1
    elif action==glfw.RELEASE:
      leftButton = 0
      lAx = gYAng
      lAy = gXAng
  if button==glfw.MOUSE_BUTTON_RIGHT:
    if action==glfw.PRESS:
      rightButton = 1
    elif action==glfw.RELEASE:
      rightButton = 0
      lTx = gXTrans
      lTy = gYTrans

def scroll_callback(window, xoffset, yoffset):
  global gXTrans, gYTrans, gZTrans
  gZTrans += yoffset
  print('mouse wheel scroll: %f, %f, %f'%(gXTrans, gYTrans, gZTrans))

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
    render()
    glfw.swap_buffers(window)

  glfw.terminate()

if __name__ == "__main__":
  main()

