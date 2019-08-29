# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
temp = []
width = 4
height = 4
number_pits = 3
for column in range(1, width + 1):
        for row in range(1, height + 1):
            temp  = temp  + ['(%d,%d)'%(column,row)]
temp.remove('(1,1)')
p_false = 0.2  # w/p happen
p_true = 1 - 0.2 # not happen
var_values = {each: [T, F] for each in temp}
Pr_N_rooms = JointProbDist(temp, var_values)
# Pr_N_rooms_initial = pow(p_false,number_pits+1)*pow(p_true,width*height-number_pits-2)
events = all_events_jpd(temp, Pr_N_rooms, {})

for each_event in events:
    # Calculate the probability for this event
    # if the value of a variable is false, motiply by p_false which is 0.12, otherwise motiply by p_true which is 1-0.12 
    prob = 1 # initial value of the probability
    for (var, val) in each_event.items(): # for each (variable, value) pair in the dictionary
        prob = prob * p_false if val == F else prob * p_true
    # Assign the probability to this event
    Pr_N_rooms[each_event]= prob

# print(Pr_N_rooms.show_approx())

for each in temp:
    p = enumerate_joint_ask(each, {}, Pr_N_rooms)
    print(each,  p.show_approx())
count = 0       
# for event in self.visted_rooms:
    
visited_rooms = set()
visited_rooms.add((1,2))
type(visited_rooms)