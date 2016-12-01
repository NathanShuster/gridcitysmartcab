import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
    # TODO: Initialize any additional variables here
        self.epsilon_greedy = 0.175
        self.epsilon_decay = 0.001
        
    
        self.state = []
        self.alpha = 0.6
        self.gamma = 0.4
        self.q_dict = {}
    
    
    def reset(self, destination=None):
        self.planner.route_to(destination)
    # TODO: Prepare for a new trip; reset any variables here, if required
    
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        # TODO: Update state
        self.state = [self.next_waypoint,
                      inputs["light"],
                      inputs["oncoming"],
                      inputs["left"]]
        
        # TODO: Select action according to your policy
        action = self.policy_recommendation(self.state)
        
        # Execute action and get reward
        reward = self.env.act(self, action)
        
        # TODO: Learn policy based on state, action, reward
        act_val = self.q_val_lookup(self.state, action)
        inputs = self.env.sense(self)
        self.next_waypoint = self.planner.next_waypoint()
        next_state = [self.next_waypoint,
                      inputs["light"],
                      inputs["oncoming"],
                      inputs["left"]]
        learned_value = reward + (self.gamma * self.max_q_val(next_state))
        new_q_val = act_val + (self.alpha * (learned_value - act_val))
        self.q_dict[str((self.state, action))] = new_q_val

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

    def policy_recommendation(self, state):
        possible_actions = [None, 'forward', 'left', 'right']
        if random.random() < self.epsilon_greedy:
            self.epsilon_greedy -= self.epsilon_decay
            return random.choice(possible_actions)
        best_action = possible_actions[0]
        best_q_val = 0
        for action in possible_actions[1:]:
            act_val = self.q_val_lookup(state, action)
            if act_val > best_q_val:
                best_action = action
                best_q_val = act_val
            elif act_val == best_q_val:
                best_action = random.choice([best_action, action])
        return best_action

    def max_q_val(self, state):
        max_val = 0
        for action in ['forward', 'left', 'right']:
            act_val = self.q_val_lookup(state, action)
            if act_val > max_val:
                max_value = act_val
        return max_val

    def q_val_lookup(self, state, action):
        val = self.q_dict.get(str((self.state, action)))
        if val == None:
            val = 0
        return val


def run():
    """Run the agent for a finite number of trials."""
    
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials
    
    # Now simulate it
    sim = Simulator(e, update_delay=0.0001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False
    
    sim.run(n_trials=100)  # run for a specified number of trials
# NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    print "Succesfully reached destination: {}".format(e.successes)
    print "Failed to reach destination: {}".format(e.failures)
    print "Penalties incurred en route: {}".format(e.penalties)


if __name__ == '__main__':
    run()
