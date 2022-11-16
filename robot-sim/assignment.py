from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 python script. 
Functions defined:
1. drive
2. turn
3. find_silver_token
4. find_golden_token
5. check_g_pair
6. check_s_pair

the main program will stop once all the tokens are in pair
"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

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

def check_g_pair(dist_g_m, d_th):
    """
    function to check whether the golden token in pursuit is in a pair with a silver token.
    to do that, first the shortest distance between the golden token and the silver tokens are calculated and if the shortest distance is smaller than a threshold, then the token is in pair.
    Returns:
    	pair_gs (int) : If its a pair then 1 else 0
    """
    dist = 100
    diff_t = -1
    i = 1
    pair_gs = 0
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            if i==1:
                diff_t = abs(token.dist-dist_g_m)
            else:
                temp = abs(token.dist-dist_g_m)
                if temp<diff_t:
                    diff_t = temp
            i+=1
        
    if diff_t<1.3*d_th: # checking whether the minimum distance of the silver tokens with the golden token is below a threshold
        pair_gs = 1
    return pair_gs


def check_s_pair(dist_s, d_th):
    """
    function to check whether the silver token in pursuit is in a pair with a golden token.
    to do that, first the shortest distance between the silver token and the golden tokens are calculated and if the shortest distance is smaller than a threshold, then the token is in pair.
    Returns:
    	pair_sg (int) : If its a pair then 1 else 0
    """
    dist = 100
    diff_t = -1
    i = 1
    pair_sg = 0
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            if i==1:
                diff_t = abs(token.dist-dist_s)
            else:
                temp = abs(token.dist-dist_s)
                if temp<diff_t:
                    diff_t = temp
            i+=1
    if diff_t<1.2*d_th:# checking whether the minimum distance of the golden tokens with the silver token is below a threshold
        pair_sg = 1
    return pair_sg


pair_chk = 0 #variable to track whether all the tokens are in pair
dropped = 0 #variable to track whether silver token is dropped

while 1:
    dist_s, rot_y_s = find_silver_token()
    dist_g, rot_y_g = find_golden_token()
    if dist_s!=-1: # if silver token is detected, checking whether the token is pair
        pair_sg = check_s_pair(dist_s, d_th)
        if pair_sg == 1:# and dist_s>2*d_th: # if the golden token is in pair, rotate the robot and count the numbers to break once we find that all the tokens are in pair
            print("The silver token is pair with a golden token, again checking")
            turn(+10, 1)
            pair_chk+=1
            if pair_chk > 10:# breaking the loop once continously 10 rotations are done
                print("All the tokens are in pairs, robot is stopping")
                break
            continue
    if dist_s==-1: # if no silver token is detected, we make the robot turn 
        print("I don't see any token!!")
        turn(+10, 1)

    elif dist_s <d_th: # if we are close to the token, we try grab it.
        print("Found it!")
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            pair_chk = 0 # reinitialising to zero
            print("Gotcha!")
            
            while 1: # loop for dropping the silver token
                dist_g_m, rot_y_g_m = find_golden_token()
                #dist_s_m, rot_y_s_m = find_silver_token()
                if dist_g_m!=-1: # if golden token is detected, checking whether the token is in pair
                    pair_gs = check_g_pair(dist_g_m, d_th)
                    if pair_gs == 1 and dist_g_m>3*d_th: # the golden token is in pair, then rotating the robot
                        print("The golden token is pair with a silver token, again checking")
                        turn(+10, 1)
                        continue
                
                if dist_g_m==-1: # if no golden token is detected, we make the robot turn 
                    print("I don't see any token!!")
                    turn(+10, 1)
                    
                elif dist_g_m <(1.3*d_th): # if we are close to the golden token, we try to release the silver token.
                    print("Close to the golden token, releasing the silver token")
                    R.release()
                    drive(-40,1)
                    turn(+20,1)
                    dropped = 1
                    break

                elif -a_th<= rot_y_g_m <= a_th: # if the robot is well aligned with the token, we go forward
                    #print("Ah, that'll do.")
                    drive(10, 0.5)
                elif rot_y_g_m < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
                    #print("Left a bit...")
                    turn(-2, 0.5)
                elif rot_y_g_m > a_th:
                    #print("Right a bit...")
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

#"""
