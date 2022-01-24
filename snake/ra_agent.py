#!/usr/bin/env python3

class RA_agent:
    def __init__(self):

# parser to parse the ltlf formula

        self.states = {"q1","q2","q3"}
        self.transitions()
        self.initialState  = "q1"
        self.finalState    = "q3"
        

    def transitions(self):

        self.transition = {

            ("q1","q1"):-0.1,
            ("q1","q2"):1,
            ("q2","q2"):-0.1,
            ("q2","q3"):1,
            ("q3","q2"):1,
            ("q3","q3"):0
        }

        self.state_dict = {

            (False,False):"q1",
            (True,False):"q2",
            (True,True):"q3" 

        }


    def reset(self):
        self.initialState = "q1" #return state q1

    def compute_RA_state(self,fd):
        if  self.initialState  = "q1":
            red_state=False
            green_state=False
        if  self.initialState  = "q2":
            red_state=True
            green_state=False
        if  self.initialState  = "q3":
            red_state=True
            green_state=True       
        if fd =="red":
            red_state=True
        if fd== "green":
            green_state=True
        return red_state, green_state
        
            
    def trace(self,food): 
        ##  note add state in env.step function; 
        ##   no eat : food = None l eat red: food = "red" | eat green : food = "green"
        
        ra_reward  = 0
        key_state = self.compute_RA_state(food) #(red,green) (True False)

        state  = self.state_dict[key_state]
        
        if self.transition.get((self.initialState,state)) != None:
            ra_reward = self.transition[(self.initialState,state)]
            self.initialState = state 
            if self.initialState=self.finalState:
                self.reset()
                
        elif self.transition.get((self.initialState,state)) == None:
            ra_reward=0
            self.initialState = state 
            if self.initialState=self.finalState:
                self.reset() 
 

        return ra_reward


