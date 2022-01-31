#!/usr/bin/env python3
class RA_agent:
    def __init__(self):

# setup DFA state and transitions

        self.states = {"q1","q2","q3"}
        self.transitions()
        self.initialState  = "q1"
        self.finalState    = "q3"
        

    def transitions(self):

        self.transition = {

            ("q1","q1"):0,
            ("q1","q2"):10,
            ("q2","q2"):-5,
            ("q2","q3"):20,
            ("q3","q2"):20,
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
        if  self.initialState  == "q1":
            red_state=False
            green_state=False
        if  self.initialState  == "q2":
            red_state=True
            green_state=False
        if  self.initialState  == "q3":
            red_state=True
            green_state=True       
        if fd =="red":
            red_state=True
            print("red")
        if fd== "green":
            green_state=True
            print("green")
        return red_state, green_state
        
            
    def trace(self,food,e): 
        ##  note add state in env.step function; 
        ##  no eat : food = None | eat red: food = "red" | eat green : food = "green"
        if food=="no food":
            ra_reward  = 0
        else :
        
            key_state = self.compute_RA_state(food) #(red,green) (True False)
            
            if self.state_dict.get(key_state) == None:
                self.reset()
                ra_reward=-5
            else:
                ra_state  = self.state_dict[key_state]
            
                if self.transition.get((self.initialState,ra_state)) != None:
                    if [(self.initialState,ra_state)]==[("q2","q3")]:
                        print ("pair")
                        e.pair+=1
                        e.update_score()
                    ra_reward = self.transition[(self.initialState,ra_state)]
                    self.initialState = ra_state 
                    if self.initialState==self.finalState:
                        #pa+=1
                        self.reset()
                        
                elif self.transition.get((self.initialState,ra_state)) == None:
                    ra_reward=0
                    self.initialState = ra_state 
                    if self.initialState==self.finalState:
                        self.reset() 
 
        return ra_reward


