import gym
from gym import error, spaces, utils
from gym.utils import seeding


"""
    Notes:
        state_size: 4
            0: Current Money Made
            1: Time Left
            2: Tasks left
            3: Current Task
"""

class ProjEnv(gym.Env):
    def __init__(self, workers: list, total_tasks):
        self._workers = workers
        self._starting_num_tasks = total_tasks
        self.reset()
        super().__init__()
    

    # Returns state
    # worker_id is the action the model predicts
    def step(self, worker_id, current_task):
        money_made, time_taken = self._workers[worker_id].work(current_task)

        self._money_made += money_made
        self._tasks_left -= 1
        self._time_left -= time_taken

        state = [self._money_made, self._time_left, self._tasks_left] # This is what goes into the model
        reward = self.get_reward(money_made, time_taken, current_task)
        return state, reward, self._done 


    # TODO: Need to add if money gets below x, penalize and quit
    def get_reward(self, money_made, time_used, current_task):
        reward = 0
        max_time = current_task.get_time()   # How long was it estimated to finish the task?
        max_money = current_task.get_money() # How much money was available upon completion
        self._max_money += max_money

        reward += (money_made / max_money) * 1.5 # Give this some weight in the equation
        reward += (max_time / time_used)  # if you did it in more time than was estimated
                                          # don't give as good of a reward

        # Give more motivation to get more tasks done
        if self._tasks_left/self._starting_num_tasks < .1: # Figured it out and did all the tasks in the time left
            reward *= 4 
        elif self._tasks_left/self._starting_num_tasks < .25: # Figured it out and did all the tasks in the time left
            reward *= 2
        elif self._tasks_left/self._starting_num_tasks < .5: # Figured it out and did all the tasks in the time left
            reward *= 1.5
        elif self._tasks_left/self._starting_num_tasks < .75: # Figured it out and did all the tasks in the time left
            reward *= 1.2
        
        # All of the tasks are finished
        if self._time_left < 0:
            self._done = True
            # Got most of them done, good job!
            if self._tasks_left/self._starting_num_tasks < .2:
                reward /= self._tasks_left/self._starting_num_tasks
                reward /= self._money_made/self._max_money
            else:
                reward *= -(1 - self._tasks_left/self._starting_num_tasks)
                reward *= -(1 - self._money_made/self._max_money)

        return reward

    def reset(self):
        self._time_left = len(self._workers) * 20  * 5 # 20 hours a week, 5 days
        # print(f'TIME LEFT: {self._time_left}')
        self._tasks_left = self._starting_num_tasks
        self._money_made = 0
        self._max_money = 0
        self._done = False

        return [self._money_made, self._time_left, self._tasks_left]