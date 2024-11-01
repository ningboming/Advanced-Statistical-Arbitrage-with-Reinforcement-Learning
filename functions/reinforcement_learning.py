import numpy as np

# Function to update state based on prices
def update_state(prices, k=3):
    # Calculate percentage change and categorize
    d = []
    for i in range(1, len(prices)):
        pi_i = (prices[i] - prices[i-1]) / prices[i-1] * 100
        if pi_i > k:
            d.append(+2)  # Big increase
        elif 0 < pi_i <= k:
            d.append(+1)  # General increase
        elif -k <= pi_i < 0:
            d.append(-1)  # General decrease
        else:
            d.append(-2)  # Big decrease
    return d

# Function to convert state vector to index
def state_to_index(state):
    # Map the state values to a binary string representation
    state_str = ''.join([
        '11' if s == +2 else
        '10' if s == +1 else
        '01' if s == -1 else
        '00'
        for s in state
    ])
    # Convert the binary string to an integer index
    return int(state_str, 2)


# Function to choose an action based on epsilon-greedy policy
def choose_action(Q_table, state_index, current_position, epsilon):
    valid_actions = get_valid_actions(current_position)
    
    if np.random.random() < epsilon:
        return np.random.choice(valid_actions)
    else:
        valid_action_indices = [map_action_to_index(a) for a in valid_actions]
        best_action_index = np.argmax([Q_table[state_index][idx] for idx in valid_action_indices])
        return valid_actions[best_action_index]

def get_valid_actions(current_position):
    if current_position == 0:  # Neutral position
        return [0, 1]  # Can only buy or hold
    elif current_position == 1:  # Long position
        return [-1, 0]  # Can only sell or hold
    
def map_action_to_index(action):
    return action + 1  # Maps -1 to 0, 0 to 1, and 1 to 2

def RL_agent_training(training_series, Q_table, l, theta, learning_rate, discount_factor, epsilon, num_episodes):
    '''
    Q_table: the initialization of Q_table
    l: the size of how many time points considered in state space
    '''
    # The training loop:
    for episode in range(num_episodes):
        for series in training_series:
            current_position = 0  # Starting with a neutral position
            for t in range(len(series)-l-1):
                current_prices = series[t:t+l+1]
                state = update_state(current_prices, k=3)
                state_index = state_to_index(state)

                action = choose_action(Q_table, state_index, current_position, epsilon=epsilon)
                reward = action * (theta - current_prices[-1]) - np.abs(action) * 0.01

                # Get the next state
                next_prices = series[t+1:t+l+2]
                next_state = update_state(next_prices, k=3)
                next_state_index = state_to_index(next_state)

                # Update the Q-table
                best_future_reward = np.max(Q_table[next_state_index])
                td_target = reward + discount_factor * best_future_reward
                td_error = td_target - Q_table[state_index, map_action_to_index(action)]
                Q_table[state_index, map_action_to_index(action)] += learning_rate * td_error

                # Update current position
                if action == 1:
                    current_position += 1  # Long
                elif action == -1:
                    current_position += -1  # Short
                # No update needed for action == 0 (hold)
    return Q_table

def RL_agent_take_actions(test_series, Q_table, l):
    # Record actions
    test_actions = [0] * l

    current_position = 0
    for t in range(len(test_series)-l-1):
        current_prices = test_series[t:t+l+1]
        state = update_state(current_prices, k=3)
        state_index = state_to_index(state)

        action = choose_action(Q_table, state_index, current_position, epsilon=0)  # Choose the best action
        test_actions.append(action)

        # Update current position 
        if action == 1:
            current_position += 1
        elif action == -1:
            current_position += -1
        # No update needed for action == 0 (hold)

    # At the end time, close all the positions
    if current_position == 0:
        test_actions.append(0)
    elif current_position == 1:
        test_actions.append(-1)
    elif current_position == -1:
        test_actions.append(1)
    
    return test_actions