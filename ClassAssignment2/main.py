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

gPath = None
sunPath = None
moonPath = None
earthPath = None
astronautPath = None

polygonMode = GL_LINE
isForced = False

gVertexArraySeparate = None
gVertexArraySeparateForced = None

isHierarchical = False

vertexArray = np.array([[]])
normalArray = np.array([[]])
faceArray = np.array([[[]]])
indexArray = np.array([[]])

numOf3 = 0
numOf4 = 0
numOfM = 0
numV = []

num = 0

sunArray = None
sunArrayForced = None
moonArray = None
moonArrayForced = None
earthArray = None
earthArrayForced = None
astronautArray = None
astronautArrayForced = None

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

def moonRender():
  global num, moonArray, moonArrayForced
  if num!=4:
    obj_loader('./moon.obj')
    moonArray, moonArrayForced = createVertexArraySeparate()
    num+=1
  draw_glDrawArrays(moonArray, moonArrayForced)

def sunRender():
  global num, sunArray, sunArrayForced
  if num!=4:
    obj_loader('./sun.obj')
    sunArray, sunArrayForced = createVertexArraySeparate()
    num+=1
  draw_glDrawArrays(sunArray, sunArrayForced)

def earthRender():
  global num, earthArray, earthArrayForced
  if num!=4:
    obj_loader('./earth.obj')
    earthArray, earthArrayForced = createVertexArraySeparate()
    num+=1
  draw_glDrawArrays(earthArray, earthArrayForced)

def astronautRender():
  global num, astronautArray, astronautArrayForced
  if num!=4:
    obj_loader('./astronaut.obj')
    astronautArray, astronautArrayForced = createVertexArraySeparate()
    num+=1
  draw_glDrawArrays(astronautArray, astronautArrayForced)
  

def obj_loader(path):
  global gPath, vertexArray, normalArray, faceArray, indexArray, gVertexArraySeparate, gVertexArraySeparateForced, numOf3, numOf4, numOfM, numV, isHierarchical
  numOf3 = numOf4 = numOfM = 0
  if path=='None':
    isHierarchical = False
    f = open(gPath, 'r')
  else:
    f = open(path, 'r')
  lines = f.readlines()

  vertexArray = np.array([[0.,0.,0.]])
  normalArray = np.array([[0.,0.,0.]])
  faceArray = np.array([[[0,0,0],[0,0,0],[0,0,0]]])
  indexArray = np.array([[0,0,0]])

  for line in lines:
    if line.startswith('#'):
      continue
    data = line.split(' ')
    
    if data[0] == 'v':
      v = np.array([[float(data[1]), float(data[2]), float(data[3])]])
      vertexArray = np.append(vertexArray, v, axis=0)
      numV.append([])
    elif data[0] == 'vn':
      vn = np.array([[float(data[1]), float(data[2]), float(data[3])]])
      normalArray = np.append(normalArray, vn, axis=0)
    elif data[0] == 'f':
      if data[len(data)-1] == '\n':
        data = np.delete(data, len(data)-1, 0)
      f1 = data[1].split('/')
      for i in range(len(f1)):
        if f1[i] == '':
          f1[i] = -1
        if len(f1) < 3:
          f1.append(-1)
      f2 = data[2].split('/')
      for i in range(len(f2)):
        if f2[i] == '':
          f2[i] = -1
        if len(f2) < 3:
          f2.append(-1)
      f3 = data[3].split('/')
      for i in range(len(f3)):
        if f3[i] == '':
          f3[i] = -1
        if len(f3) < 3:
          f3.append(-1)
      
      face = np.array([[[int(f1[0])-1, int(f1[1]), int(f1[2])],
                        [int(f2[0])-1, int(f2[1]), int(f2[2])],
                        [int(f3[0])-1, int(f3[1]), int(f3[2])]]])
      faceArray = np.append(faceArray, face, axis=0)
      numV[int(f1[0])-1].append(len(indexArray)-1)
      numV[int(f2[0])-1].append(len(indexArray)-1)
      numV[int(f3[0])-1].append(len(indexArray)-1)
      index = np.array([[int(f1[0])-1, int(f2[0])-1, int(f3[0])-1]])
      indexArray = np.append(indexArray, index, axis=0)

      if len(data) == 4:
        numOf3 += 1
      elif len(data) == 5:
        numOf4 += 1
      elif len(data) > 5:
        numOfM += 1
    else:
      continue

  faceArray = np.delete(faceArray, 0, 0)
  indexArray = np.delete(indexArray, 0, 0)
  vertexArray = np.delete(vertexArray, 0, 0)
  normalArray = np.delete(normalArray, 0, 0)

  print()
  if(isHierarchical):
    print("File name:", path)
  else:
    print("File name:", gPath)
  print("Total number of faces:", len(faceArray))
  print("Number of faces with 3 vertices:", numOf3)
  print("Number of faces with 4 vertices:", numOf4)
  print("Number of faces with more than 4 vertices:", numOfM)


def createVertexArraySeparate():
  global gPath, vertexArray, normalArray, faceArray, indexArray, gVertexArraySeparate, gVertexArraySeparateForced, numOf3, numOf4, numOfM, numV
  global isForced
  varr1 = np.array([[0,0,0]], 'float32')
  nvArray = np.array([[0,0,0]], 'float32')
  vnvArray = np.array([[0,0,0]], 'float32')

  for i in range(len(faceArray)):
    v0 = vertexArray[faceArray[i][0][0]]
    v1 = vertexArray[faceArray[i][1][0]]
    v2 = vertexArray[faceArray[i][2][0]]
    vec1 = v1 - v0
    vec2 = v2 - v0
    n = np.cross(vec1, vec2)
    nv = np.array([n], 'float32')
    nvArray = np.append(nvArray, nv, axis = 0)
    
    if (faceArray[i][0][2] != -1):
      n0 = np.array([normalArray[faceArray[i][0][2]-1]], 'float32')
      n1 = np.array([normalArray[faceArray[i][1][2]-1]], 'float32')
      n2 = np.array([normalArray[faceArray[i][2][2]-1]], 'float32')
    else:
      n0 = np.array([n], 'float32')
      n1 = np.array([n], 'float32')
      n2 = np.array([n], 'float32')

    v0 = vertexArray[faceArray[i][0][0]]
    v1 = vertexArray[faceArray[i][1][0]]
    v2 = vertexArray[faceArray[i][2][0]]

    varr1 = np.append(varr1, n0, axis=0)
    varr1 = np.append(varr1, np.array([v0], 'float32'), axis=0)
    varr1 = np.append(varr1, n1, axis=0)
    varr1 = np.append(varr1, np.array([v1], 'float32'), axis=0)
    varr1 = np.append(varr1, n2, axis=0)
    varr1 = np.append(varr1, np.array([v2], 'float32'), axis=0)
  
  nvArray = np.delete(nvArray, 0, 0)
  varr1 = np.delete(varr1, 0, 0)
  varr2 = np.array(varr1)

  for i in range(len(vertexArray)):
    sum = np.array([0, 0, 0], 'float32')
    for j in numV[i]:
      sum += nvArray[j]
    sum /= len(numV[i])
    sum = np.array([sum])
    vnvArray = np.append(vnvArray, sum, axis=0)

  vnvArray = np.delete(vnvArray, 0, 0)
  for i in range(len(faceArray)):
    varr2[i*6+0] = vnvArray[faceArray[i][0][0]]
    varr2[i*6+2] = vnvArray[faceArray[i][1][0]]
    varr2[i*6+4] = vnvArray[faceArray[i][2][0]]
  return varr1, varr2

def draw_glDrawArrays(a, b):
  global isForced, isHierarchical
  if isForced:
    varr = b
  else:
    varr = a

  glPolygonMode(GL_FRONT_AND_BACK, polygonMode)
  glEnableClientState(GL_VERTEX_ARRAY)
  glEnableClientState(GL_NORMAL_ARRAY)
  glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
  glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
  glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawTriangle_glDrawArrays():
  global gVertexArraySeparate, gVertexArraySeparateForced, isForced, isHierarchical
  if isForced:
    varr = gVertexArraySeparateForced
  else:
    varr = gVertexArraySeparate

  glPolygonMode(GL_FRONT_AND_BACK, polygonMode)
  glEnableClientState(GL_VERTEX_ARRAY)
  glEnableClientState(GL_NORMAL_ARRAY)
  glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
  glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
  glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def render():
  global isPerspective ,gXAng, gYAng, gXTrans, gYTrans, gZTrans, gPath, isHierarchical

  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  glEnable(GL_DEPTH_TEST)
  glMatrixMode(GL_PROJECTION)
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

  glMatrixMode(GL_MODELVIEW)
  drawGridArray()

  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_LIGHT1)

  glEnable(GL_RESCALE_NORMAL)

  lightpos = (10., 10., 10., 1.)
  lightColor = (1.,0.,0.,1.)
  ambientLightColor = (.1,.1,.1,1.)
  glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
  glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
  glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
  glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

  lightpos = (-10., -10., -10., 0.)
  lightColor = (0.,0.,1.,1.)
  ambientLightColor = (.1,.1,.1,1.)
  glLightfv(GL_LIGHT1, GL_POSITION, lightpos)
  glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
  glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
  glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)

  objectColor = (1.,1.,1.,1.)
  specularObjectColor = (1.,1.,1.,1.)
  glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
  glMaterialfv(GL_FRONT, GL_SHININESS, 10)
  glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

  if(isHierarchical):
    t = glfw.get_time()
    glPushMatrix()
    glTranslatef(0, 15, 0)
    sunRender()

    glPushMatrix()
    glTranslatef(30*np.sin(t), 0, 30*np.cos(t))
    earthRender()

    glPushMatrix()
    glTranslatef(3*np.sin(3*t), 0, 3*np.cos(3*t))
    moonRender()
    
    glPushMatrix()
    glTranslatef(1.2*np.sin(5*t), 0, 1.2*np.cos(5*t))
    glScalef(0.05, 0.05, 0.05)
    astronautRender()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
  else:
    if gPath == None:
      glDisable(GL_LIGHTING)
      return
    drawTriangle_glDrawArrays()
  glDisable(GL_LIGHTING)

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
  global isPerspective, polygonMode, isForced, isHierarchical
  if action==glfw.PRESS or action==glfw.REPEAT:
    if key==glfw.KEY_V:
      if isPerspective:
        isPerspective=False
      else:
        isPerspective=True
    elif key==glfw.KEY_Z:
      if polygonMode == GL_LINE:
        polygonMode = GL_FILL
      else:
        polygonMode = GL_LINE
    elif key==glfw.KEY_S:
      if isForced:
        isForced = False
      else:
        isForced = True
    elif key==glfw.KEY_H:
      if isHierarchical:
        isHierarchical = False
      else:
        isHierarchical = True


def drop_callback(window, paths):
  global gPath, gVertexArraySeparate, gVertexArraySeparateForced
  gPath = paths[0]
  isHierarchical = False
  obj_loader('None')
  gVertexArraySeparate, gVertexArraySeparateForced = createVertexArraySeparate()


def main():
  global gVertexArraySeparate

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
  glfw.set_drop_callback(window, drop_callback)

  glfw.swap_interval(1)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    render()
    glfw.swap_buffers(window)

  glfw.terminate()

if __name__ == "__main__":
  main()

