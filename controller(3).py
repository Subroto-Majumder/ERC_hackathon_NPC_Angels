#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from path_planner import *
import math

def get_rotation (msg):
        global yaw , orientation_q
        orientation_q = msg.pose.pose.orientation
        yaw = euler_from_quaternion([orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])[2]
    

def rotate(target):
    yaw = 0.0
    k = 0.5
    vel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10)
    twist_cmd =Twist()


    while not rospy.is_shutdown():
        target_rad = target*math.pi/180
        angular_z = k * (target_rad-yaw)
        twist_cmd.angular.z = angular_z
        print(target_rad,yaw)
        vel_publisher.publish(twist_cmd)

        r.sleep()

        if angular_z/target_rad < 0.002:
            break
    

def move_to(prev , target):
        vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        r = rospy.Rate(10)  
        twist_cmd = Twist()
        angle_to_turn = math.degrees(math.atan((target[1]-prev[1])/(target[0]-prev[0])))
        rotate(angle_to_turn)

        r.sleep()
        d = dst([target , prev])
        t0 = rospy.Time.now().to_sec()
        while(rospy.Time.now().to_sec() - t0 <= 1):  
            twist_cmd.linear.x = d
            vel_publisher.publish(twist_cmd)
            r.sleep()
        twist_cmd.linear.x = 0
        vel_publisher.publish(twist_cmd)
        r.sleep()


def main():
    rospy.init_node('controller', anonymous=True)
    co_ordinates = [(1,1),(1,9),(0,5),(3,5)]
    coordinates = graph(co_ordinates,(0,0))
    

    for i in range(len(coordinates)-1):
        move_to(coordinates[i],coordinates[i+1])
        

    rospy.loginfo("Movement completed.")

if __name__ == '__main__':
    try:
        main()
        sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
     