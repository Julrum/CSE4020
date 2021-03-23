import glfw
from OpenGL.GL import *
import numpy as np

glList = []

def render():
  global glList
  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  # draw cooridnates
  glBegin(GL_LINES)
  glColor3ub(255, 0, 0)
  glVertex2fv(np.array([0.,0.]))
  glVertex2fv(np.array([1.,0.]))
  glColor3ub(0, 255, 0)
  glVertex2fv(np.array([0.,0.]))
  glVertex2fv(np.array([0.,1.]))
  glEnd()

  glColor3ub(255, 255, 255)
  
  for op in glList:
    if op == 'Q':
      glTranslatef(-0.1, 0, 0)
    elif op == 'E':
      glTranslatef(0.1, 0, 0)
    elif op == 'A':
      glRotatef(10, 0, 0, 1)
    elif op == 'D':
      glRotatef(-10, 0, 0, 1)

  drawTriangle()

def drawTriangle():
  glBegin(GL_TRIANGLES)
  glVertex2fv(np.array([.0,.5]))
  glVertex2fv(np.array([.0,.0]))
  glVertex2fv(np.array([.5,.0]))
  glEnd()

def key_callback(window, key, scancode, action, mods):
  global glList
  if action==glfw.PRESS or action==glfw.REPEAT:
    if key==glfw.KEY_Q:
      glList.insert(0, 'Q')
    elif key==glfw.KEY_E:
      glList.insert(0, 'E')
    elif key==glfw.KEY_A:
      glList.insert(0, 'A')
    elif key==glfw.KEY_D:
      glList.insert(0, 'D')
    elif key==glfw.KEY_1:
      glList = []

def main():
  if not glfw.init():
    return
  window = glfw.create_window(480,480, '2017029670', None,None)
  if not window:
    glfw.terminate()
    return
  glfw.make_context_current(window)
  glfw.set_key_callback(window, key_callback)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    render()
    glfw.swap_buffers(window)

  glfw.terminate()

if __name__ == "__main__":
  main()
