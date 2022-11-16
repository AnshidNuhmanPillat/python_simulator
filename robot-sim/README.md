Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Assignment
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names.   

In the code, I have implemented six function
1. drive
2. turn
3. find_silver_token
4. find_golden_token
5. check_g_pair
6. check_s_pair
7. Main()

**Functions**

**1. drive:**   
Function for setting a linear velocity.  
Args: 
- speed (int): the speed of the wheels
- seconds (int): the time interval

set Motor1 speed and Motor2 speed same.   
run for set time.

**2. turn:**  
Function for setting an angular velocity.  
Args: 
- speed (int): the speed of the wheels
- seconds (int): the time interval

set Motor1 speed and Motor2 speed opposite to each other.   
run for set time.

**3. find_silver_token:**  
Function to find the closest silver token.  
Returns:
- dist (float): distance of the closest silver token (-1 if no silver token is detected)
- rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)

initialise the distance to hundred (a high value than the work area).
for tokens in view of robot
- if token distance less than the initialised value and token type is silver get distance and orientation and return
- if distance is same as the initialised value return -1 and -1


**4. find_golden_token:**  
Function to find the closest golden token.  
Returns:
- dist (float): distance of the closest golden token (-1 if no golden token is detected)
- rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)

initialise the distance to hundred (a high value than the work area).
for tokens in view of robot
- if token distance less than the initialised value and token type is golden get distance and orientation and return
- if distance is same as the initialised value return -1 and -1


**5. check_g_pair:**  
Function to check whether the golden token in pursuit is in a pair with a silver token.
To do that, first the shortest distance between the golden token and the silver tokens are calculated and if the shortest distance is smaller than a threshold, then the token is in pair.
Arg: 
- distance (float) : distance of the golden token from the robot
- distance threshold (float) : threshold to check when the tokens are in pair
Returns:
- pair_gs (int) : If its a pair then 1 else 0

initialise the distance to hundred (a high value than the work area).  
initialise difference vector to -1, since we are taking absolute value later.  
initialise vector to track the number of tokens.  
initialise the return variable.  

for tokens in view of robot
- if token distance less than the initialised value and token type is silver get distance and orientation and return
   - if the first value is taking then the difference is equal to the absolute(distance of the golden token from the robot -  distance of the silver token from the robot)
   - else a temporary variable is created smilarly and if the temporary value is less than the difference, then difference is updated
- if the difference is less than the threshold, the two tokens are considered are in pair and returned the variable 1 else 0 

**6. check_s_pair:**  
Function to check whether the silver token in pursuit is in a pair with a golden token.
To do that, first the shortest distance between the silver token and the golden tokens are calculated and if the shortest distance is smaller than a threshold, then the token is in pair.
Arg: 
- distance (float) : distance of the silver token from the robot
- distance threshold (float) : threshold to check when the tokens are in pair
Returns:
- pair_sg (int) : If its a pair then 1 else 0

initialise the distance to hundred (a high value than the work area).
initialise difference vector to -1, since we are taking absolute value later 
initialise vector to track the number of tokens
initialise the return variable

for tokens in view of robot
- if token distance less than the initialised value and token type is golden get distance and orientation and return
   - if the first value is taking then the difference is equal to the absolute(distance of the silver token from the robot -  distance of the golden token from the robot)
   - else a temporary variable is created smilarly and if the temporary value is less than the difference, then difference is updated
- if the difference is less than the threshold, the two tokens are considered are in pair and returned the variable 1 else 0

**Starting main function:**  
initialising the variable to track whether all the tokens are in pair.  
initialising the variable to track whether the silver token is droppped.  

while true, called find_silver_token and find_golden_token function to get distance and orientation of silver and golden token
- if the robot is detected then checked whether the silver token is in pair with a golden token; if yes then the variable is updated to track the pairing and then the robot is rotated. If the variable is above a limit, the loop is break 
- if the token is not detected, the robot is rotated
- if the robot is in the proximity of the silver token, grab the token
   - while true, called find_golden_token function to get distance and orientation of golden token
   - then if a golden token is deteced then checked whether the golden token is in pair, if yes robot is rotated
   - if no golden token is detected, rotate the robot
   - if the robot is cloaser to the golden token, then the silver token is dropped.
   - if the robot is aligned with the golden token, robot is moved forward
   - if the robot is not well aligned with the golden token, the robot is rotated to right or to the left
   

- if the robot is aligned with the silver token, robot is moved forward
- if the robot is not well aligned with the silver token, the robot is rotated to right or to the left


When done, you can run the program with:

```bash
$ python run.py assignment.py
```

To improve the code, currently finding the tokens randomly, instead if the closest token is used the runtime can be reduced.

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
