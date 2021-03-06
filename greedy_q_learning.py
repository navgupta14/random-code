import numpy as np
from random import randint
from random import uniform
import matplotlib.pyplot as plt

# up, down, left, right
r = np.matrix([[-1, 0, -1, 0],
               [-1, 100, 0, 0],
               [-1, 0, 0, 0],
               [-1, 0, 0, -1],
               [0, 0, -1, 100],
               [-1, -1, -1, -1],
               [0, 0, 100, 0],
               [0, 0, 0, -1],
               [0, -1, -1, 0],
               [100, -1, 0, 0],
               [0, -1, 0, 0],
               [0, -1, 0, -1]])

# print(r)
#Q = np.matrix(np.zeros([12, 4]))
Q = np.random.rand(12, 4)
for x in range(12):
    for y in range(4):
        if r[x, y] == -1:
            Q[x, y] = -1
# num of states
n_states = 12

# Goal state index
goal_state = 5

# Discounting parameter(learning parameter)
gamma = 0.9

# Greediness parameter
epsilon = 0.2

# num of episodes
episodes = 1000

prevQ = 0.0
curQ = 0.0
Qs = []

def generate_resultant_state(state, action):
    if action == 0:
        return state - 4
    elif action == 1:
        return state + 4
    elif action == 2:
        return state - 1
    elif action == 3:
        return state + 1


# list of legal moves/actions available in this state
def generate_legal_actions(state):
    current_rewards = r[state, :]
    legal_moves = np.where(current_rewards >= 0)[1]
    legal_moves = np.squeeze(np.asarray(legal_moves))
    return legal_moves


# choosing random action out of available actions
def choose_random_action(available_actions):
    next_action = np.random.choice(available_actions)
    return next_action

# choosing max value generating action - Greedy approach
def choose_max_value_action(current_state, available_actions):
    next_best_action = available_actions[0]
    max_val = 0
    for action in available_actions:
        temp_val = Q[current_state, action]
        if temp_val > max_val:
            next_best_action = action
            max_val = temp_val
    return next_best_action


def update_Q(current_state, next_state, action):
    rsa = r[current_state, action]
    max_val = Q[next_state, :].max()
    new_q = rsa + (gamma * max_val)
    Q[current_state, action] = new_q

def plot(Qs):
    iterations = [x for x in range(episodes)]
    plt.plot(iterations, Qs)
    plt.show()

for episode in range(episodes):
    current_state = randint(0, n_states - 1)
    while current_state != goal_state:
        legal_actions = generate_legal_actions(current_state)
        if uniform(0, 1) > (1 - epsilon):
            random_legal_action = choose_random_action(legal_actions)
        else:
            random_legal_action = choose_max_value_action(current_state, legal_actions)
        next_state = generate_resultant_state(current_state, random_legal_action)
        update_Q(current_state, next_state, random_legal_action, )
        current_state = next_state
    for x in range(12):
        for y in range(4):
            curQ += Q[x, y]
    Qs.append(curQ - prevQ)
    prevQ = curQ
    curQ = 0

print(Q)
plot(Qs)
