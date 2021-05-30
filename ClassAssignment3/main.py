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
gCount = 0
gModel = None
isAnimate = False

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

class Joint:
  def __init__(self):
    self.parent = None
    self.children = []
    self.offset = []
    self.channels = []
    self.frames = []
    self.index = [0, 0]

class Model:
  def __init__(self):
    self.root = None
    self.stack = []
    self.channel_count = 0
    self.jointName = []
    self.motions = []
    self.frametime = 0.
    self.frames = 0

def bvh_loader(path):
  global gModel
  f = open(path)
  lines = f.readlines()

  parent = None
  current = None
  isMotion = False
  model = Model()

  for line in lines[1:len(lines)]:
    parts = line.split()
  
    if parts[0] in ["ROOT", "JOINT", "End"]:
      if current:
        parent = current

      current = Joint()
      model.jointName.append(parts[1])

      if len(model.stack) == 0:
        model.root = current
      model.stack.append(current)
      current.parent = parent
      if current.parent:
        current.parent.children.append(current)
      
    elif parts[0] == "{":
      pass

    elif parts[0] == "}":
      current = current.parent
      if current:
        parent = current.parent
        
    elif parts[0] == "OFFSET":
      offset = []
      for i in range(1, len(parts)):
        offset.append(float(parts[i]))
      current.offset = offset
  
    elif parts[0] == "CHANNELS":
      current.channels = parts[2:len(parts)]
      current.index[0] = model.channel_count
      current.index[1] = model.channel_count + len(current.channels)
      model.channel_count += len(current.channels)

    elif parts[0] == "MOTION":
      isMotion = True
  
    elif parts[0] == "Frames:":
      model.frames = int(parts[1])
  
    elif parts[0] == "Frame":
      model.frametime = float(parts[2])
  
    elif isMotion:
      channelData(model.root, [float(val) for val in parts])
      vals = []
      for val in parts:
        vals.append(float(val))
      model.motions.append(vals)
      
  fullName = ""
  for name in model.jointName:
    fullName += name
    if name == model.jointName[-1]:
      continue
    fullName += ", "

  print("File name: ", gPath)
  print("Number of frames: ", str(model.frames))
  print("FPS (which is 1/FrameTime): ", str(1/model.frametime))
  print("Number of joints (including root): ", str(len(model.jointName)))
  print("List of all joint names:", fullName)
  print()
  return model

def channelData(joint, value):
  joint.frames.append(value[:len(joint.channels)])
  value = value[len(joint.channels):]
  for child in joint.children:
    value = channelData(child, value)
  return value  

def drawModel(joint, count, drawable):
  global isAnimate, gModel
	
  position = [0, 0, 0]
  R = np.identity(4)
  offset = np.array([float(joint.offset[0]*0.05),
                     float(joint.offset[1]*0.05),
                     float(joint.offset[2])*0.05])

  if isAnimate:
    for i in range(0, len(joint.channels)):
      channel = joint.channels[i]
      info = gModel.motions[count][joint.index[0] + i]
      

      if channel.upper() == "XPOSITION":
        position[0] = info*0.05
      elif channel.upper() == "YPOSITION":
        position[1] = info*0.05
      elif channel.upper() == "ZPOSITION":
        position[2] = info*0.05

      tmp = np.identity(4)
      if channel.upper() == "XROTATION":
        tmp = np.array([[1, 0, 0, 0],
                        [0, np.cos(np.radians(info)), -np.sin(np.radians(info)), 0],
                        [0, np.sin(np.radians(info)), np.cos(np.radians(info)), 0],
                        [0, 0, 0, 1]])
        R = np.dot(R, tmp)
      elif channel.upper() == "YROTATION":
        tmp = np.array([[np.cos(np.radians(info)), 0, np.sin(np.radians(info)), 0],
                        [0, 1, 0, 0],
                        [-np.sin(np.radians(info)), 0, np.cos(np.radians(info)), 0],
                        [0, 0, 0, 1]])
        R = np.dot(R, tmp)
      elif channel.upper() == "ZROTATION":
        tmp = np.array([[np.cos(np.radians(info)), -np.sin(np.radians(info)), 0, 0],
                        [np.sin(np.radians(info)), np.cos(np.radians(info)), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        R = np.dot(R, tmp)
  glPushMatrix()
  glTranslatef(position[0], position[1], position[2])
  if drawable:
    glBegin(GL_LINES)
    glVertex3fv(np.array([0, 0, 0]))
    glVertex3fv(np.array(offset))
    glEnd()

  glTranslatef(joint.offset[0]*0.05, joint.offset[1]*0.05, joint.offset[2]*0.05)
  glMultMatrixf(R.T)

  for child in joint.children:
    drawModel(child, count, True)
  glPopMatrix()

def render(gCount):
  global isPerspective ,gXAng, gYAng, gXTrans, gYTrans, gZTrans, gPath, gModel

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

  if gModel:
    glPushMatrix()
    if gCount == gModel.frames:
      gCount = 0
    drawModel(gModel.root, gCount % gModel.frames, False)
    glPopMatrix()

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
  global isPerspective, gCount, isAnimate
  if action==glfw.PRESS or action==glfw.REPEAT:
    if key==glfw.KEY_V:
      if isPerspective:
        isPerspective=False
      else:
        isPerspective=True
    if key==glfw.KEY_SPACE:
      if isAnimate:
        gCount = 0
        isAnimate=False
      else:
        isAnimate=True

def drop_callback(window, paths):
  global gPath, gCount, isAnimate, gModel
  gPath = paths[0]
  gCount = 0
  isAnimate = False
  gModel = bvh_loader(gPath)

def main():
  global isAnimate, gCount

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
    render(gCount)
    glfw.swap_buffers(window)
    if isAnimate:
      gCount += 1

  glfw.terminate()

if __name__ == "__main__":
  main()

