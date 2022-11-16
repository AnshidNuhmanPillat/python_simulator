from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1
The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:
1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1
	When done, run with:
	$ python run.py solutions/exercise3_solution.py
"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y


"""
function for grabbing the silver token
"""
""" 
def robot_grab(d_th,a_th):
    grabbed = -1 # variable to know whether the robot grabbed or not
    pair_chk = 0 # variable for checking whether all the silver and golden tokens are in pairs
    while 1:
        dist_s, rot_y_s = find_silver_token()
        dist_g, rot_y_g = find_golden_token()
        if dist_s==-1: # if no silver token is detected, we make the robot turn
            print("I don't see any token!!")
            turn(+10, 1)
        elif (dist_g!=-1 and (abs(dist_s-dist_g)<d_th and abs(rot_y_s-rot_y_g)<a_th)): # checking whether the silver token found is close to a golden tocken
            print("The silver token is pair with a golden token, again checking")
            turn(+10,1)
            pair_chk+=1
            
        elif dist_s <d_th: # if we are close to the token, we try grab it.
            print("Found it!")
            if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
                grabbed = 1
            else:
                print("Aww, I'm not close enough.")
        elif -a_th<= rot_y_s <= a_th: # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(10, 0.5)
        elif rot_y_s < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y_s > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
        
        if grabbed==1: # when the robot grabs the silver box, breaks out of the loop
            break
    return grabbed,pair_chk
    
"""    
    



pair_chk = 0 
dropped = 0

while 1:
    dist_s, rot_y_s = find_silver_token()
    dist_g, rot_y_g = find_golden_token()
    if dist_s==-1: # if no silver token is detected, we make the robot turn 
        print("I don't see any token!!")
        turn(+10, 1)
    elif (dist_g!=-1 and (abs(dist_s-dist_g)<(1.3*d_th) and abs(rot_y_s-rot_y_g)<a_th)): # checking whether the silver token found is close to a golden tocken
        print("The silver token is pair with a golden token, again checking")
        turn(+10,1)
        pair_chk+=1


    elif dist_s <d_th: # if we are close to the token, we try grab it.
        print("Found it!")
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            
            while 1: # loop for dropping the silver token
                dist_g_m, rot_y_g_m = find_golden_token()
                dist_s_m, rot_y_s_m = find_silver_token()
                
                if dist_g_m==-1: # if no golden token is detected, we make the robot turn 
                    print("I don't see any token!!")
                    turn(+10, 1)
                elif (dist_g!=-1 and (abs(dist_s-dist_g)<d_th and abs(rot_y_s-rot_y_g)<a_th)): # checking whether the golden token found is close to a silver tocken
                    print("The golden token is pair with a silver token, again checking")
                    turn(+10,1)
                    
                elif dist_g_m <(1.3*d_th): # if we are close to the golden token, we try to release the silver token.
                    print("Close to the golden token, releasing the silver token")
                    R.release()
                    drive(-40,1)
                    turn(+20,1)
                    dropped = 1
                    break

                elif -a_th<= rot_y_g_m <= a_th: # if the robot is well aligned with the token, we go forward
                    print("Ah, that'll do.")
                    drive(10, 0.5)
                elif rot_y_g_m < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
                    print("Left a bit...")
                    turn(-2, 0.5)
                elif rot_y_g_m > a_th:
                    print("Right a bit...")
                    turn(+2, 0.5)
        else:
            print("Aww, I'm not close enough.")
    elif -a_th<= rot_y_s <= a_th: # if the robot is well aligned with the token, we go forward
        #print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y_s < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        #print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y_s > a_th:
        #print("Right a bit...")
        turn(+2, 0.5)

    if pair_chk == 10: # checking whether all the silver and golden tokens are in pairs
        break # breaking away from the loop
