
#----- IFN680 Assignment 1 -----------------------------------------------#
#  The Wumpus World: a probability based agent
#
#  Implementation of two functions
#   1. PitWumpus_probability_distribution()
#   2. next_room_prob()
#
#    Student no: PUT YOUR STUDENT NUMBER HERE
#    Student name: PUT YOUR NAME HERE
#
#-------------------------------------------------------------------------#
from random import *
from AIMA.logic import *
from AIMA.utils import *
from AIMA.probability import *
from tkinter import messagebox

#--------------------------------------------------------------------------------------------------------------
#
#  The following two functions are to be developed by you. They are functions in class Robot. If you need,
#  you can add more functions in this file. In this case, you need to link these functions at the beginning
#  of class Robot in the main program file the_wumpus_world.py.
#
#--------------------------------------------------------------------------------------------------------------
#   Function 1. PitWumpus_probability_distribution(self, width, height)
#
# For this assignment, we treat a pit and the wumpus equally. Each room has two states: 'empty' or 'containing a pit or the wumpus'.
# A Boolean variable to represent each room: 'True' means the room contains a pit/wumpus, 'False' means the room is empty.
#
# For a cave with n columns and m rows, there are totally n*m rooms, i.e., we have n*m Boolean variables to represent the rooms.
# A configuration of pits/wumpus in the cave is an event of these variables.
#
# The function PitWumpus_probability_distribution() below is to construct the joint probability distribution of all possible
# pits/wumpus configurations in a given cave, two parameters
#
# width : the number of columns in the cave
# height: the number of rows in the cave
#
# In this function, you need to create an object of JointProbDist to store the joint probability distribution and  
# return the object. The object will be used by your function next_room_prob() to calculate the required probabilities.
#
# This function will be called in the constructor of class Robot in the main program the_wumpus_world.py to construct the
# joint probability distribution object. Your function next_room_prob() will need to use the joint probability distribution
# to calculate the required conditional probabilities.
#
def PitWumpus_probability_distribution(self, width, height): 
    # Create a list of variable names to represent the rooms. 
    # A string '(i,j)' is used as a variable name to represent a room at (i, j)
    
    self.PW_variables = [] 
    for column in range(1, width + 1):
        for row in range(1, height + 1):
            self.PW_variables  = self.PW_variables  + ['(%d,%d)'%(column,row)]

    #--------- Add your code here -------------------------------------------------------------------
    self.PW_variables.remove('(1,1)')
    knownpw = self.observation_pits(self.visited_rooms)
    knownbs = self.observation_breeze_stench(self.visited_rooms)
    available_rooms = list(self.available_rooms)
    number_of_pit = self.cave.number_of_pit
    p_false =0.2 #should be replaced by self.max_pit_probability  # w/p happen
    p_true = 1-0.2#should be replaced by 1 - self.max_pit_probability # not happen
    
    var_values = {each: [T, F] for each in available_rooms}
    Pr_N_rooms = JointProbDist(available_rooms, var_values)
    events = all_events_jpd(available_rooms, Pr_N_rooms, {})

    for each_event in events:
    # Calculate the probability for this event
    # if the value of a variable is false, motiply by p_false which is 0.2, otherwise motiply by p_true which is 1-0.2 
        prob = 1 # initial value of the probability
        ##没有考虑 stentch和breeze
        for (var, val) in each_event.items(): # for each (variable, value) pair in the dictionary
            if val == F:
                prob = prob * p_false
            else: prob = prob * p_true
    # Assign the probability to this event
        Pr_N_rooms[each_event]= prob
        
    return Pr_N_rooms
 
    
    
    
            
        
#---------------------------------------------------------------------------------------------------
#   Function 2. next_room_prob(self, x, y)
#
#  The parameters, (x, y), are the robot's current position in the cave environment.
#  x: column
#  y: row
#
#  This function returns a room location (column,row) for the robot to go.
#  There are three cases:
#
#    1. Firstly, you can call the function next_room() of the logic-based agent to find a
#       safe room. If there is a safe room, return the location (column,row) of the safe room.
#    2. If there is no safe room, this function needs to choose a room whose probability of containing
#       a pit/wumpus is lower than the pre-specified probability threshold, then return the location of
#       that room.
#    3. If the probabilities of all the surrounding rooms are not lower than the pre-specified probability
#       threshold, return (0,0).
#
def next_room_prob(self, x, y):
    
    knownpw = self.observation_pits(self.visited_rooms)
    knownbs = self.observation_breeze_stench(self.visited_rooms)
    rquery = self.cave.getsurrounding(x,y)
    new_room = (0,0)
    ##删选安全的room
    for each_s in rquery:
        if each_s not in self.visited_rooms:
            # call check_safety() to do a resolution reasoning to find a safe room
            if (self.check_safety(each_s[0],each_s[1]) == False):  
                rquery.remove(each_s) 
    lowest_pr = 1
    for each_room in rquery:
        ##选出最小的概率，没有则返回（0，0）a
        pr_query = enumerate_joint_ask(each_room,{},self.PitWumpus_probability_distribution(self.cave.WIDTH,self.cave.HEIGHT)) 
        
        if pr_query.prob[False] < lowest_pr:
            lowest_pr = pr_query.prob[False]
            new_room = each_room
            
    if lowest_pr > 0.2:  #should be replaced by self.max_pit_probability
            return (0,0)    
    return new_room        
    
    #--------- Add your code here -------------------------------------------------------------------





#---------------------------------------------------------------------------------------------------
 
####################################################################################################
