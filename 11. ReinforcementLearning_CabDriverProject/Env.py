#!/usr/bin/env python
# coding: utf-8

# Import routines

# In[1]:


import numpy as np
import math
import random
import itertools
import time
import pandas as pd


# In[2]:


# Defining hyperparameters
m = 5 # number of cities, ranges from 1 ..... m
t = 24 # number of hours, ranges from 0 .... t-1
d = 7  # number of days, ranges from 0 ... d-1
C = 5 # Per hour fuel and other costs
R = 9 # per hour revenue from a passenger


# In[34]:


class CabDriver():

    def __init__(self):
        """initialise your state and define your action space and state space"""
        self.action_space = [(0,0)] + list(itertools.permutations([i for i in range(m)], 2))
        self.state_space = [list(i) for i in list(itertools.product(*[list(range(m)),list(range(t)),list(range(d))]))]
        self.state_init = random.choice(self.state_space)

        # Start the first round
        self.reset()


    ## Encoding state (or state-action) for NN input

    def state_encod_arch1(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. Hint: The vector is of size m + t + d."""
        state_encod = [0 for i in range(m+t+d)]
        state_encod[state[0]] = 1
        state_encod[m+state[1]] = 1
        state_encod[m+t+state[2]] = 1

        return state_encod


    # Use this function if you are using architecture-2 
    # def state_encod_arch2(self, state, action):
    #     """convert the (state-action) into a vector so that it can be fed to the NN. This method converts a given state-action pair into a vector format. Hint: The vector is of size m + t + d + m + m."""

        
    #     return state_encod


    ## Getting number of requests

    def requests(self, state):
        """Determining the number of requests basis the location. 
        Use the table specified in the MDP and complete for rest of the locations"""
        location = state[0]
        if location == 0:
            requests = np.random.poisson(2)
        if location == 1:
            requests = np.random.poisson(12)
        if location == 2:
            requests = np.random.poisson(4)
        if location == 3:
            requests = np.random.poisson(7)
        if location == 4:
            requests = np.random.poisson(8)


        if requests >15:
            requests =15
            
        if requests <1:
            requests =1

        possible_actions_index = random.sample(range(1, (m-1)*m +1), requests) # (0,0) is not considered as customer request
        actions = [self.action_space[i] for i in possible_actions_index]
        actions.append([0,0])

        return possible_actions_index,actions   



    def next_state_func(self, state, action, Time_matrix):
        """Takes state and action as input and returns next state"""
        run_time = 0
        
        t_curr = state[1]
            
        
        if action == (0,0):
            next_hour = t_curr+1
            next_day = state[2]
            if next_hour > 23:
                next_hour = next_hour - 24
                next_day = next_day+1
                if next_day>6:
                    next_day = next_day - 7
                    
            next_hour = int(next_hour)
            next_day = int(next_day)

            tip = 0
            tpq = 0
            
            tip = int(tip)
            tpq = int(tpq)
            
            next_state = [state[0],next_hour,next_day]
            run_time = run_time + next_hour
            run_time = int(run_time)
            
        elif state[0]!=action[0]:
            t1 = Time_matrix[state[0]][action[0]][state[1]][state[2]] #transit time (going from curr loc to pick up loc)
            
            next_hour = t_curr+t1
            next_day = state[2]
            if next_hour > 23:
                next_hour = next_hour - 24
                next_day = next_day+1
                if next_day>6:
                    next_day = next_day - 7
            next_hour = int(next_hour)
            next_day = int(next_day)
              
            t2 = Time_matrix[action[0]][action[1]][next_hour][next_day] #ride time (after reaching pick up loc from curr loc)
                
            tip = t_curr + t1         # time after reaching pick up loc
            tpq = tip + t2             # time after reaching drop loc
            
            if tpq > 23:
                tpq = tpq - 24
                next_day = next_day + 1
                if next_day > 6:
                    next_day = next_day - 7
                    
            tip = int(tip)
            tpq = int(tpq)
            next_day = int(next_day)
                    
            next_state = [action[1], tpq, next_day]
            run_time = run_time + state[1]+tpq
            run_time = int(run_time)
            
        else:
            t1 = Time_matrix[action[0]][action[1]][state[1]][state[2]]      #already at pick up loc, time taken to go from pick up to drop loc 
            tip = 0
            tpq = action[1]+t1
            next_day = state[2]
            if tpq>23:
                tpq = tpq - 24
                next_day = next_day+1
                if next_day>6:
                    next_day = next_day - 7
            
            tip = int(tip)        
            tpq = int(tpq)
            next_day = int(next_day)

            next_state = [action[1], tpq, next_day]
            run_time = run_time + tpq
            run_time = int(run_time)
            
        return next_state, tip, tpq, run_time
        

    def reward_func(self, state, action, Time_matrix):
        """Takes in state, action and Time-matrix and returns the reward"""
        if action == (0,0):
            reward = -C
        else:
            
            tip = self.next_state_func(state, action, Time_matrix)[1]
            tpq = self.next_state_func(state, action, Time_matrix)[2]
            
            reward = R*tpq - C*(tpq + tip)
        
        return reward


    def reset(self):
        return self.action_space, self.state_space, self.state_init

