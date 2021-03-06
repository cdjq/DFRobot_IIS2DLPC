# -*- coding:utf-8 -*-
"""
   @file tap.py
   @brief Single click and double click detection
   @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
   @licence     The MIT License (MIT)
   @author [fengli](li.feng@dfrobot.com)
   @version  V1.0
   @date  2021-01-16
   @get from https://www.dfrobot.com
   @https://github.com/DFRobot/DFRobot_IIS2DLPC
"""

import sys
sys.path.append("../..") # set system path to top

from DFRobot_IIS2DLPC import *
import time

#如果你想要用SPI驱动此模块，打开下面两行的注释并通过SPI连接好模块和树莓派
RASPBERRY_PIN_CS =  27              #Chip selection pin when SPI is selected
acce = DFRobot_IIS2DLPC_SPI(RASPBERRY_PIN_CS)


#如果你想要应IIC驱动此模块，打开下面三行的注释，并通过I2C连接好模块和树莓树莓派
I2C_MODE         = 0x01             #default use I2C1
ADDRESS_0        = 0x19             #I2C address
#acce = DFRobot_IIS2DLPC_I2C(I2C_MODE ,ADDRESS_0)

acce.begin()
print("chip id :")
print(acce.get_ID())
acce.soft_reset()
'''
    @brief Set the measurement range
    @param range:Range(g)
                 RANGE_2G     #/**<±2g>*/
                 RANGE_4G     #/**<±4g>*/
                 RANGE_8G     #/**<±8g>*/
                 RANGE_16G    #/**< ±16g>*/
'''
acce.set_range(acce.RANGE_2G)
acce.set_power_mode(acce.CONT_LOWPWRLOWNOISE_12BIT)
acce.set_data_rate(acce.ODR_800HZ)


#Enable click detection in the X direction
acce.enable_tap_detection_on_z(True)
#Enable click detection in Y direction
acce.enable_tap_detection_on_y(True)
#Enable click detection in the Z direction
acce.enable_tap_detection_on_x(True)
#The threshold setting in the X direction is similar to the sensitivity of detection, the larger the value, the less sensitive (0~31)
acce.set_tap_threshold_on_x(0.5)
#The threshold setting in the Y direction is similar to the sensitivity of detection, the larger the value, the less sensitive (0~31)
acce.set_tap_threshold_on_y(0.5)
#The threshold setting in the Z direction is similar to the sensitivity of detection, the larger the value, the less sensitive (0~31)
acce.set_tap_threshold_on_z(0.5)
'''
  双击的两次点击之间的间隔时间：
  @param th 1 LSB = 32 * 1/ODR(0~15)
  @n ODR:Data acquisition frequency
  @n example
  |                           High-pass filter cut-off frequency configuration                             |
  |--------------------------------------------------------------------------------------------------------|
  |                |    ft [Hz]      |        ft [Hz]       |       ft [Hz]        |        ft [Hz]        |
  |   dur          |Data rate = 25 Hz|   Data rate = 100 Hz |  Data rate = 400 Hz  |   Data rate = 800 Hz  |
  |--------------------------------------------------------------------------------------------------------|
  |  n             |n*(1s/25)= n*40ms|  n*(1s/100)= n*10ms  |  n*(1s/400)= 2.5*nms |  n*(1s/800)= n*1.25ms |
  |--------------------------------------------------------------------------------------------------------|
'''
acce.set_tap_dur(3)

'''
  Set the click detection mode:
      ONLY_SINGLE   //检测单击
      BOTH_SINGLE_DOUBLE //检测单击和双击
'''
acce.set_tap_mode(acce.BOTH_SINGLE_DOUBLE)

'''
Set the interrupt source of the int1 pin:
        DOUBLE_TAP = 0x08 #/**< Double-tap recognition is routed to INT1 pad>*/
        FF_EVENT = 0x10 #/**< Free-fall recognition is routed to INT1 pad>*/
        WAKEUP_EVENT = 0x20 #/**<Wakeup recognition is routed to INT1 pad>*/
        SINGLE_TAP = 0x40  #/**<Single-tap recognition is routed to INT1 pad.>*/
        TNT_16D  = 0x80  #/**<6D recognition is routed to INT1 pad>*/

'''
acce.set_int1_route(acce.DOUBLE_TAP)
time.sleep(0.1)

while True:
    #Get the acceleration in the three directions of xyz
    #time.sleep(0.3)
    tap = False
    event = acce.tap_detect()
    direction = acce.get_tap_direction()
    if event == acce.SINGLE_CLICK:
      print ("Tap Detected :")
      tap = True
    elif event == acce.DOUBLE_CLICK:
      print ("Double Tap Detected :")
      tap = True
    if tap == True:
      if direction == acce.DIR_X_UP:
        print("Click it in the positive direction of x")
      elif direction == acce.DIR_X_DOWN:
        print("Click it in the negative direction of x")
      elif direction == acce.DIR_Y_UP:
        print("Click it in the positive direction of y")
      elif direction == acce.DIR_Y_DOWN:
        print("Click it in the negative direction of y")
      elif direction == acce.DIR_Z_UP:
        print("Click it in the positive direction of z")
      elif direction == acce.DIR_Z_DOWN:
        print("Click it in the negative direction of z")
      tap = False
      

        