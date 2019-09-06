
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
    
import logic_based_move as logic_move
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
#   ** 03/09/2019 Developed by XU Han
#   ** Parameters: set, list, tuple, or dict
#   ** Description: 
#   ** 1. The function is to change types, such as list, tuple and set, to a list type.
#   ** 2. The function is to deal with each item in the transformtion of data to String type.  
#   ** 3. The funciton is to truncate each item with String type. (Space Removal)
#   ** Return: list
#   ** Example: List -> List / [(1,  2), (3,3)] => ['(1,2)', '(3,3)']
#   ** Example: Set -> List / {(1,  2), (3,3)} => ['(1,2)', '(3,3)']
#
def data_standardised(v_list):
    v_list = list(v_list)
    for i in range(len(v_list)):
        v_list[i] = str(v_list[i]).replace(' ','')
        v_list[i] = ''+v_list[i]+''
    return v_list
    
T, F = True, False 
def PitWumpus_probability_distribution(self, width, height): 
    # Create a list of variable names to represent the rooms. 
    # A string '(i,j)' is used as a variable name to represent a room at (i, j)
    self.PW_variables = [] 
    for column in range(1, width + 1):
        for row in range(1, height + 1):
            self.PW_variables  = self.PW_variables  + ['(%d,%d)'%(column,row)]

    #--------- Add your code here -------------------------------------------------------------------
    p_false = 0.8  # w/p happen
    p_true = 1 - p_false # not happen
    var_values = {each: [T, F] for each in self.PW_variables}
    jdP_PWs = JointProbDist(self.PW_variables, var_values)
    events = all_events_jpd(self.PW_variables, jdP_PWs, {})
    for each_event in events:
        # Calculate the probability for this event
        # if the value of a variable is false, motiply by p_false which is 0.12, otherwise motiply by p_true which is 1-0.12 
        prob = 1 # initial value of the probability
        for (var, val) in each_event.items(): # for each (variable, value) pair in the dictionary
            prob = prob * p_false if val == F else prob * p_true
        # Assign the probability to this event
        jdP_PWs[each_event]= prob
    return jdP_PWs
    #---------------------------------------------------------------------------------------------------
#  Function 2. next_room_prob(self, x, y)
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
    self.next_move = (0,0)
    self.next_move = logic_move.next_room(self, x, y)
    
    if(self.next_move != (0,0)):
        return self.next_move
    else:
        # When the room is not safe, it requires to consider case 2.
        # Create a Set to store all visited rooms
        r_know = data_standardised(self.visited_rooms)
        
        # Create a list to rooms that is available to move
        r_query = data_standardised(self.cave.getsurrounding(x, y))
        for room in r_know:
            if room in r_query:
                r_query.remove(room)
            
        # Create a list to rooms that is to store unknown area.
        r_other = data_standardised(self.PW_variables)
        for room in r_know:
            if room in r_other:
                r_other.remove(room)
            
        for room in r_query:
            if room in r_other:
                r_other.remove(room)
        
        # Create a dict to store the room with the probability of PITS & WUMPUS
        known_pw = self.observation_pits(self.visited_rooms)
        # Create a dict to store the room with the probability of Breeze & Stench
        known_bs = self.observation_breeze_stench(self.visited_rooms)
        lowest_pr = 1
        for Pq in r_query:
            # the variable is used for the caculation of probabilities in True
            sum_true = 0 
            # the variable is used for the caculation of probabilities in False
            sum_false = 0 
            # the variable is used for the caculation of probabilities in T / T + F
            prob = 0
            
            # R_unknown = R_other + (R_query - Pq)
            r_unknown = r_other + r_query
            r_unknown.remove(Pq)
            print(self.jdP_PWs.show_approx())
            # Initialisation of the PW
            known_pw.update({Pq : T})
            events_true = all_events_jpd(r_unknown, self.jdP_PWs, known_pw)
            for event in events_true: 
                sum_true += self.consistent(known_bs, event) * self.jdP_PWs[event]

            known_pw[Pq] = F
            events_false = all_events_jpd(r_unknown, self.jdP_PWs, known_pw)
            for event in events_false: 
                sum_false += self.consistent(known_bs, event) * self.jdP_PWs[event] 
        
            # Nomalisation of the Probability
            prob = sum_true / (sum_true + sum_false)
            r_unknown.append(Pq)
            # Getting the lowest probability in each loop
            if (lowest_pr > prob):
                lowest_pr = prob
                self.next_move = tuple(eval(Pq))
     
        if(lowest_pr > self.max_pit_probability):
            return (0,0)
        else:
            return self.next_move
####################################################################################################
