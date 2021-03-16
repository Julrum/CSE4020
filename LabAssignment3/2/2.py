import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.array([[1.,0.,0.],
                       [0.,1.,0.],
                       [0.,0.,1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
  global gComposedM
  if key==glfw.KEY_W:
    w = np.array([[1.,0.,0.],
                  [0.,0.9,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = w @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = w @ gComposedM
  if key==glfw.KEY_E:
    e = np.array([[1.,0.,0.],
                  [0.,1.1,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = e @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = e @ gComposedM
  if key==glfw.KEY_S:
    th = np.radians(10)
    s = np.array([[np.cos(th), -np.sin(th),0.],
                  [np.sin(th), np.cos(th),0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = s @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = s @ gComposedM
  if key==glfw.KEY_D:
    th = np.radians(-10)
    d = np.array([[np.cos(th), -np.sin(th),0.],
                  [np.sin(th), np.cos(th),0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = d @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = d @ gComposedM
  if key==glfw.KEY_X:
    x = np.array([[1.,0.,0.1],
                  [0.,1.,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = x @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = x @ gComposedM
  if key==glfw.KEY_C:
    c = np.array([[1.,0.,-0.1],
                  [0.,1.,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = c @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = c @ gComposedM
  if key==glfw.KEY_R:
    r = np.array([[-1.,0.,0.],
                  [0.,-1.,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = r @ gComposedM
    elif action==glfw.REPEAT:
      gComposedM = r @ gComposedM
  if key==glfw.KEY_1:
    o = np.array([[1.,0.,0.],
                  [0.,1.,0.],
                  [0.,0.,1.]])
    if action==glfw.PRESS:
      gComposedM = o
    elif action==glfw.REPEAT:
      gComposedM = o

def main():
    global gComposedM
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029670", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        th = np.radians(60)
        R = np.array([[np.cos(th), -np.sin(th),0.],
                      [np.sin(th), np.cos(th),0.],
                      [0.,        0.,         1,]])

        T = np.array([[1.,0.,.4],
                      [0.,1.,.1],
                      [0.,0.,1.]])

        # render(R)
        # render(T)
        render(gComposedM)
        # render(R @ T)


        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

