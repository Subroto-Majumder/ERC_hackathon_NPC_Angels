import cv2
import numpy as np
import math
from sensor_msgs.msg import Image
from task_status.msg import Taskstatus
import rospy 


def callback_f(msg):
    image = msg.data
    image_area = image.shape[0] * image.shape[1]

    lower_red = np.array([0, 0, 200], dtype = "uint8") 
    upper_red= np.array([0, 0, 255], dtype = "uint8")

    lower_blue = np.array([200, 0, 0], dtype = "uint8") 
    upper_blue= np.array([255, 0, 0], dtype = "uint8")

    red_mask = cv2.inRange(image, lower_red, upper_red)
    blue_mask = cv2.inRange(image, lower_blue, upper_blue)

    red_output = cv2.bitwise_and(image, image, mask =  red_mask) 
    blue_output = cv2.bitwise_and(image, image, mask =  blue_mask) 

    red_gray = cv2.cvtColor(red_output, cv2.COLOR_BGR2GRAY)
    red_blur = cv2.GaussianBlur(red_gray, (35, 35), 5)
    red_ret, red_thresh = cv2.threshold(red_blur, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    red_pixels = cv2.countNonZero(red_thresh)
    red_area_ratio = (red_pixels / image_area) * 100

    blue_gray = cv2.cvtColor(blue_output, cv2.COLOR_BGR2GRAY)
    blue_blur = cv2.GaussianBlur(blue_gray, (35, 35), 5)
    blue_ret, blue_thresh = cv2.threshold(blue_blur, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blue_pixels = cv2.countNonZero(blue_thresh)
    blue_area_ratio = (blue_pixels / image_area) * 100

    if blue_area_ratio>5:
        task = "Iron Extraction ongoing"
    elif red_area_ratio>5:
        task = "Zinc Extraction ongoing"
    else:
        pass
    Task_s =Taskstatus()
    Task_s.status=task
    pub.publish(Task_s)


pub = rospy.Publisher('task_status',Taskstatus,queue_size=10)
sub = rospy.Subscriber('/camera/rgb/image_raw', Image, callback_f)

rospy.spin()
