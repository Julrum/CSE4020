import glfw
import numpy as np
from OpenGL.GL import *

radians = np.linspace(0, 2*np.pi, 13)
currentInput = 3

def render():
  global currentInput
  glClear(GL_COLOR_BUFFER_BIT)
  glLoadIdentity()
  glBegin(GL_LINE_LOOP)
  for radian in radians:
    glVertex2fv((np.cos(radian), np.sin(radian)))
  glEnd()

  glBegin(GL_LINES)
  glVertex2f(0.0,0.0)
  glVertex2fv((np.cos(radians[currentInput]), np.sin(radians[currentInput])))
  glEnd()

def key_callback(window, key, scancode, action, mods):
  global currentInput
  if key==glfw.KEY_0:
    if action==glfw.PRESS:
      currentInput = 5
  if key==glfw.KEY_1:
    if action==glfw.PRESS:
      currentInput = 2
  if key==glfw.KEY_2:
    if action==glfw.PRESS:
      currentInput = 1
  if key==glfw.KEY_3:
    if action==glfw.PRESS:
      currentInput = 0
  if key==glfw.KEY_4:
    if action==glfw.PRESS:
      currentInput = 11
  if key==glfw.KEY_5:
    if action==glfw.PRESS:
      currentInput = 10
  if key==glfw.KEY_6:
    if action==glfw.PRESS:
      currentInput = 9
  if key==glfw.KEY_7:
    if action==glfw.PRESS:
      currentInput = 8
  if key==glfw.KEY_8:
    if action==glfw.PRESS:
      currentInput = 7
  if key==glfw.KEY_9:
    if action==glfw.PRESS:
      currentInput = 6
  if key==glfw.KEY_Q:
    if action==glfw.PRESS:
      currentInput = 4
  if key==glfw.KEY_W:
    if action==glfw.PRESS:
      currentInput = 3

def main():
  # Initialize the library
  if not glfw.init():
    return
  # Create a windowed mode window and its OpenGL context
  window = glfw.create_window(480, 480, "2017029670", None, None)
  if not window:
    glfw.terminate()
    return

  glfw.set_key_callback(window, key_callback)

  # Make the window's context current
  glfw.make_context_current(window)

  # Loop until the user closes the window
  while not glfw.window_should_close(window):
    # Poll for and process events
    glfw.poll_events()

    # Render here, e.g. using pyOpenGL
    render()

    # Swap front and back buffers
    glfw.swap_buffers(window)

  glfw.terminate()

if __name__ == "__main__":
  main()
