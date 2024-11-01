def DM_take_actions(series, theta, std, k):
    # Record actions
    action_list = []
    current_position = 0
    for i in range(len(series)):
        # update action
        if current_position == 0 and series[i] < theta - k * std:
            action = 1
        elif current_position == 1 and series[i] > theta + k * std:
            action = -1
        else:
            action = 0
        action_list.append(action)

        # Update current position 
        if action == 1:
            current_position += 1
        elif action == -1:
            current_position += -1

    return action_list