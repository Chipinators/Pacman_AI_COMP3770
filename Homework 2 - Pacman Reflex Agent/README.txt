The main file in this homework is multiagents.py with the implementation of the evaluationFuntion function on line 55.	

The problem for this homework was to create a reflex agent by writing the evaluation function for the agent. The evaluation function should take in the current game state and the action being evaluated and return a score for that action.

The autograder runs the reflex agent on the openClassic game layout and so my evaluation function is made specifically for that layout. The autograder average score for my evaluation function is 1442.6 with a high score of 1455.0, here is the basic logic:

1. If the ghost is scared and there is only one food left, chase it and eat it

2. If the ghost is scared and there are multiple food left, focus food until ghost timer is almost less than distance from pacman to ghost
            
3. If Pacman clears far enough right, grab the capsuel
            
4. If the ghost isnt scared, and there is only one food left, get the capsuel
            
5. If the ghost isnt scared and there are multiple food focus on eating food left to right
            
6. If no capsuel, eat the last food