# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 12:33:07 2020

@author: Faria Soroni
"""

import cv2
import numpy as np
cap = cv2.VideoCapture(0)
while(1):
  
  _, frameinv = cap.read()    

  frame = cv2.flip( frameinv, 1)


  cv2.imshow('Frame', hsv)

  k = cv2.waitKey(10) & 0xFF
  if k == 27:
      break
cap.release()
#cv2.destroyAllWindows()
def nothing(x):
  pass

kernel = np.zeros((300,512,3), np.uint8)
name = 'Calibrate'
cv2.namedWindow(name)

cv2.createTrackbar('Hue', name, 0, 255, nothing)
cv2.createTrackbar('Sat', name, 0, 255, nothing)
cv2.createTrackbar('Val', name, 0, 255, nothing)

switch = '0 : OFF \n 1 : ON'

cv2.createTrackbar(switch, name,0,1,nothing)

while(1):
  cv2.imshow(name,kernel)
  k = cv2.waitKey(1) & 0xFF
  if k == 27:
      break

  hue = cv2.getTrackbarPos('Hue', name)
  sat = cv2.getTrackbarPos('Sat', name)
  val = cv2.getTrackbarPos('Val', name)
  s = cv2.getTrackbarPos(switch,name)

  if s == 0:
      kernel[:] = 0
  else:
      kernel[:] = [hue,sat,val]

def makeMask(hsv_frame, color_Range):

    mask = cv2.inRange( hsv_frame, color_Range[0], color_Range[1])
eroded = cv2.erode( mask, kernel, iterations=1)
dilated = cv2.dilate( eroded, kernel, iterations=1)

      return dialated

def drawCentroid(vid, color_area, mask, showCentroid):

    contour, _ = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
l=len(contour)
area = np.zeros(l)

for i in range(l):
  if cv2.contourArea(contour[i])>color_area[0] and cv2.contourArea(contour[i]):
            area[i] = cv2.contourArea(contour[i])
  else:
    area[i] = 0
    a = sorted(area, reverse = True)

for i in range(l):
  for j in range(1):
    if area[i] == a[j]:
      swap( contour, i, j)
if l > 0 :		
  M = cv2.moments(contour[0])

  if M['m00'] != 0:
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    center = (cx,cy)

    if showCentroid:
      cv2.circle( vid, center, 5, (0,0,255), -1)
        
    return center
else:
  
  return (-1,-1)
  
  def setCursorPos( yc, pyp):

      yp = np.zeros(2)

if abs(yc[0]-pyp[0])<5 and abs(yc[1]-pyp[1])<5:
  yp[0] = yc[0] + .7*(pyp[0]-yc[0]) 
  yp[1] = yc[1] + .7*(pyp[1]-yc[1])
else:
  yp[0] = yc[0] + .1*(pyp[0]-yc[0])
  yp[1] = yc[1] + .1*(pyp[1]-yc[1])

return yp

def chooseAction(yp, rc, bc):
    out = np.array(['move', 'false'])
if rc[0]!=-1 and bc[0]!=-1:
  
  if distance(yp,rc)<50 and distance(yp,bc)<50 and distance(rc,bc)<50 :
    out[0] = 'drag'
    out[1] = 'true'
    return out
  elif distance(rc,bc)<40: 
    out[0] = 'right'
    return out
  elif distance(yp,rc)<40:	
    out[0] = 'left'
    return out
  elif distance(yp,rc)>40 and rc[1]-bc[1]>120:
    out[0] = 'down'
    return out	
  elif bc[1]-rc[1]>110:
    out[0] = 'up'
    return out
  else:
    return out
else:
  out[0] = -1
  return out
  
  def performAction( yp, rc, bc, action, drag, perform):
      if perform:
       cursor[0] = 4*(yp[0]-110)
  cursor[1] = 4*(yp[1]-120)
  if action == 'move':
    if yp[0]>110 and yp[0]<590 and yp[1]>120 and yp[1]<390:
      pyautogui.moveTo(cursor[0],cursor[1])
    elif yp[0]<110 and yp[1]>120 and yp[1]<390:
      pyautogui.moveTo( 8 , cursor[1])
    elif yp[0]>590 and yp[1]>120 and yp[1]<390:
      pyautogui.moveTo(1912, cursor[1])
    elif yp[0]>110 and yp[0]<590 and yp[1]<120:
      pyautogui.moveTo(cursor[0] , 8)
    elif yp[0]>110 and yp[0]<590 and yp[1]>390:
      pyautogui.moveTo(cursor[0] , 1072)
    elif yp[0]<110 and yp[1]<120:
      pyautogui.moveTo(8, 8)
    elif yp[0]<110 and yp[1]>390:
      pyautogui.moveTo(8, 1072)
    elif yp[0]>590 and yp[1]>390:
      pyautogui.moveTo(1912, 1072)
    else:
      pyautogui.moveTo(1912, 8)
  elif action == 'left':
    pyautogui.click(button = 'left')
  elif action == 'right':
    pyautogui.click(button = 'right')
    time.sleep(0.3)	
  elif action == 'up':
    pyautogui.scroll(5)
#			time.sleep(0.3)
  elif action == 'down':
    pyautogui.scroll(-5)			
#			time.sleep(0.3)
  elif action == 'drag' and drag == 'true':
    global y_pos
    drag = 'false'
    pyautogui.mouseDown()
  
    while(1):
      k = cv2.waitKey(10) & 0xFF
      changeStatus(k)
      _, frameinv = cap.read()
      frame = cv2.flip( frameinv, 1)
      hsv = cv2.cvtColor( frame, cv2.COLOR_BGR2HSV)
      b_mask = makeMask( hsv, blue_range)
      r_mask = makeMask( hsv, red_range)
      y_mask = makeMask( hsv, yellow_range)
      py_pos = y_pos 
      b_cen = drawCentroid( frame, b_area, b_mask, showCentroid)
      r_cen = drawCentroid( frame, r_area, r_mask, showCentroid)	
      y_cen = drawCentroid( frame, y_area, y_mask, showCentroid)
    
      if 	py_pos[0]!=-1 and y_cen[0]!=-1:
        y_pos = setCursorPos(y_cen, py_pos)
      performAction(y_pos, r_cen, b_cen, 'move', drag, perform)
      cv2.imshow('Frame', frame)
      if distance(y_pos,r_cen)>60 or distance(y_pos,b_cen)>60 or distance(r_cen,b_cen)>60:
        break
    pyautogui.mouseUp()
          
cv2.destroyAllWindows()