import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)

def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

# euler[0]: zang
# euler[1]: yang
# euler[2]: xang
def ZYXEulerToRotMat(euler):
    zang, yang, xang = euler
    Rx = np.array([[1,0,0],
                   [0, np.cos(xang), -np.sin(xang)],
                   [0, np.sin(xang), np.cos(xang)]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang)],
                   [0,1,0],
                   [-np.sin(yang), 0, np.cos(yang)]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0],
                   [np.sin(zang), np.cos(zang), 0],
                   [0,0,1]])
    return Rx @ Ry @ Rz

def exp(rv):
    t = l2norm(rv)
    u = normalized(rv)
    R = np.array([[np.cos(t) + u[0]*u[0]*(1-np.cos(t)), u[0]*u[1]*(1-np.cos(t))-u[2]*np.sin(t), u[0]*u[2]*(1-np.cos(t))+u[1]*np.sin(t)],
                  [u[1]*u[0]*(1-np.cos(t))+u[2]*np.sin(t), np.cos(t)+u[1]*u[1]*(1-np.cos(t)), u[1]*u[2]*(1-np.cos(t))-u[0]*np.sin(t)],
                  [u[2]*u[0]*(1-np.cos(t))-u[1]*np.sin(t), u[2]*u[1]*(1-np.cos(t))+u[0]*np.sin(t), np.cos(t)+u[2]*u[2]*(1-np.cos(t))]])
    return R

def log(R):
    t = np.arccos((R[0][0]+R[1][1]+R[2][2]-1)/2)
    rv = np.array([(R[2][1]-R[1][2])/np.sin(t)/2, (R[0][2]-R[2][0])/np.sin(t)/2, (R[1][0]-R[0][1])/np.sin(t)/2])
    return t * rv

def slerp(R1, R2, t):
    return R1 @ exp(t*log(R1.T@R2))

def drawObject(R1, R2):
      J1 = R1
    
      glPushMatrix()
      glMultMatrixf(J1.T)
      glPushMatrix()
      glTranslatef(0.5,0,0)
      glScalef(0.5, 0.05, 0.05)
      drawCube_glDrawElements()
      glPopMatrix()
      glPopMatrix()

      T1 = np.identity(4)
      T1[0][3] = 1.

      J2 = R1 @ T1 @ R2

      glPushMatrix()
      glMultMatrixf(J2.T)
      glPushMatrix()
      glTranslatef(0.5,0,0)
      glScalef(0.5, 0.05, 0.05)
      drawCube_glDrawElements()
      glPopMatrix()
      glPopMatrix()

def render(ang):
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    euler1_1 = np.array([np.radians(20), np.radians(30), np.radians(30)])
    R1_1 = ZYXEulerToRotMat(euler1_1)

    euler2_1 = np.array([np.radians(15), np.radians(30), np.radians(25)])
    R2_1 = ZYXEulerToRotMat(euler2_1)

    euler1_2 = np.array([np.radians(45), np.radians(60), np.radians(40)])
    R1_2 = ZYXEulerToRotMat(euler1_2)

    euler2_2 = np.array([np.radians(25), np.radians(40), np.radians(40)])
    R2_2 = ZYXEulerToRotMat(euler2_2)

    euler1_3 = np.array([np.radians(60), np.radians(70), np.radians(50)])
    R1_3 = ZYXEulerToRotMat(euler1_3)

    euler2_3 = np.array([np.radians(40), np.radians(60), np.radians(50)])
    R2_3 = ZYXEulerToRotMat(euler2_3)

    euler1_4 = np.array([np.radians(80), np.radians(85), np.radians(70)])
    R1_4 = ZYXEulerToRotMat(euler1_4)

    euler2_4 = np.array([np.radians(55), np.radians(80), np.radians(65)])
    R2_4 = ZYXEulerToRotMat(euler2_4)
    M1 = np.identity(4)
    M2 = np.identity(4)
    ang
    if 0<= ang < 20:
      t = (ang % 20)/20
      M1[:3,:3] = slerp(R1_1, R1_2, t)
      M2[:3,:3] = slerp(R2_1, R2_2, t)
      drawObject(M1, M2)
    elif 20 <= ang < 40:
      t = (ang % 20)/20
      M1[:3,:3] = slerp(R1_2, R1_3, t)
      M2[:3,:3] = slerp(R2_2, R2_3, t)
      drawObject(M1, M2)
    elif 40 <= ang <= 60:
      t = (ang % 20)/21
      M1[:3,:3] = slerp(R1_3, R1_4, t)
      M2[:3,:3] = slerp(R2_3, R2_4, t)
      drawObject(M1, M2)

    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    M1[:3,:3] = R1_1
    M2[:3,:3] = R2_1
    drawObject(M1, M2)

    objectColor = (1.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    M1[:3,:3] = R1_2
    M2[:3,:3] = R2_2
    drawObject(M1, M2)

    objectColor = (0.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    M1[:3,:3] = R1_3
    M2[:3,:3] = R2_3
    drawObject(M1, M2)
    glDisable(GL_LIGHTING)

    objectColor = (0.,0.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    M1[:3,:3] = R1_4
    M2[:3,:3] = R2_4
    drawObject(M1, M2)


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2017029670', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    
    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 61
        render(ang)
        count += 1

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

