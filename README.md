# gridcitysmartcab
Self-driving agent trained using reinforcement learning (Q-learning algorithm) in a simple grid city world. Made with PyGame.

**RULE SUMMARY:**

The smartcab operates in an ideal, grid-like city (similar to New York City), with roads going in the North-South and East-West directions. Other vehicles are present on the road, but there are no pedestrians to be concerned with. At each intersection there is a traffic light that either allows traffic in the North-South direction or the East-West direction. 
- On a green light, a left turn is permitted if there is no oncoming traffic making a right turn or coming straight through the intersection.
- On a red light, a right turn is permitted if no oncoming traffic is approaching from your left through the intersection.

Violating a traffic rule or colliding with another car causes the agent to be penalized. Reaching the destination gives a reward.

**IMPORTANT VARIABLES:**
On a big picture level, the important things to know are: our location, where we want to go, and obstacles.
This could be defined as the following features

Next waypoint - where we want to go.

Lights - a boolean that tells us whether the light in front of us is green. This helps us know which ways we can move.

Cars left - We cannot turn right on red if there are cars coming from the left. Oncoming cars - We cannot turn left on green if there are cars oncoming.

I used the variables in the environment.py file to construct these features in the form of a python list tied to self.state.
There were two variables I chose to omit: right traffic and the deadline. I opted to leave out right traffic because they don’t really change our behavior like oncoming cars (can’t turn left on green) or left cars (can’t turn right on red) do. I left out a potential deadline feature because I didn’t want our car to potentially break traffic laws in an attempt to reach the ending before the deadline. Arriving a little earlier is not worth a potential car crash.

**Q-LEARNING VARIABLE OPTIMIZATION:**

Epsilon_greedy (Exploration Rate, I fixed the epsilon_decay to 0.001)

Alpha (Learning Rate)

Gamma (Discount Factor)

After a significant amount of testing, I found the following values to maximize the results for my program:
self.epsilon_greedy = 0.175 self.alpha = 0.6 self.gamma = 0.4

To find these values, I first fixed (admittedly arbitrarily) alpha to 0.6 and and gamma to 0.4 and tested epsilon greedy at ranges from 0.25 to 0.15, at increments of 0.025. I found the least crashes and traffic violations at 0.175. I then fixed epsilon_greedy at 0.175 and left gamma as it was and tested alpha at a range from 0.8 to 0.4, at increments of 0.1. I found the best results at alpha = 0.6. I then fixed both epsilon_greedy and alpha and tested for gamma at a range of 0.6 to 0.2, in increments of 0.1. I found the best results (again, measured in least violations and most successes out of 100) at gamma = 0.5.

This process could've admittedly been more scientific. However, when 100 trials are run, it gets the smartcab to the destination before the deadline 98 times out of 100, and the last 10 trials are accident/violation free. That's pretty solid.
