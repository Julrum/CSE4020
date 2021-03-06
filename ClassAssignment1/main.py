import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

isPerspective = True
gXAng = -35.
gYAng = 45.
gXTrans = gYTrans = 0.
gZTrans = 5.
cx = cy = 0.
lAx = lAy = lTx = lTy = 0.
leftButton = rightButton = False

def drawXGrid():
  glBegin(GL_LINES)
  glVertex3f(-10., 0., 0.)
  glVertex3f(10., 0., 0.)
  glEnd()
  
def drawYGrid():
  glBegin(GL_LINES)
  glVertex3f(0., 0., -10.)
  glVertex3f(0., 0., 10.)
  glEnd()

def drawGridArray():
  for i in range(-10, 11):
    for j in range(-10, 11):
      glPushMatrix()
      glTranslatef(i, 0, 0)
      drawYGrid()
      glTranslatef(-i, 0, j)
      drawXGrid()
      glPopMatrix()

def drawFrame():
  glBegin(GL_LINES)
  glColor3ub(255, 0, 0)
  glVertex3f( 0.,0.,0.)
  glVertex3f(10.,0.,0.)
  glColor3ub(0, 255, 0)
  glVertex3f(0.,0.,0.)
  glVertex3f(0.,10.,0.)
  glColor3ub(0, 0, 255)
  glVertex3f(0.,0.,0)
  glVertex3f(0.,0.,10.)
  glEnd()

def render():
  global isPerspective ,gXAng, gYAng, gXTrans, gYTrans, gZTrans
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

  glLoadIdentity()

  if isPerspective:
    gluPerspective(120, 1, 1, 100)
  else:
    glOrtho(-gZTrans,gZTrans, -gZTrans,gZTrans, -100,100)

  glTranslatef(gXTrans, gYTrans, -gZTrans)
  glRotatef(-gXAng, 1, 0, 0)
  glRotatef(-gYAng, 0, 1, 0)
  drawFrame()
  glColor3ub(255, 255, 255)

  drawGridArray()

def cursor_callback(window, xpos, ypos):
  global gXAng, gYAng, cx, cy, lAx, lAy, lTx, lTy, leftButton, rightButton, gXTrans, gYTrans
  if leftButton==False and rightButton==False:
    cx = xpos
    cy = ypos
  elif leftButton:
    dx = cx - xpos
    dy = cy - ypos
    gYAng = lAx + dx
    gXAng = lAy + dy
  elif rightButton:
    dx = cx - xpos
    dy = cy - ypos
    gXTrans = lTx - dx*0.0416
    gYTrans = lTy + dy*0.0416
  
def button_callback(window, button, action, mod):
  global gXAng, gYAng, gXTrans, gYTrans, leftButton, rightButton, lAx, lAy, lTx, lTy
  if button==glfw.MOUSE_BUTTON_LEFT:
    lAx = gYAng
    lAy = gXAng
    if action==glfw.PRESS:
      leftButton=True
    elif action==glfw.RELEASE:
      leftButton=False
  if button==glfw.MOUSE_BUTTON_RIGHT:
    lTx = gXTrans
    lTy = gYTrans
    if action==glfw.PRESS:
      rightButton=True
    elif action==glfw.RELEASE:
      rightButton=False

def scroll_callback(window, xoffset, yoffset):
  global gZTrans
  gZTrans += yoffset

def key_callback(window, key, scancode, action, mods):
  global isPerspective
  if action==glfw.PRESS or action==glfw.REPEAT:
    if key==glfw.KEY_V:
      if isPerspective:
        isPerspective=False
      else:
        isPerspective=True

def main():
  if not glfw.init():
    return
  window = glfw.create_window(960,960,'Viewer', None,None)
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

