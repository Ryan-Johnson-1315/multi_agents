# import sys
# from utils import utilities
# import json
# import random
# import datetime

# if __name__ == "__main__":
#     config = json.load(open(sys.argv[1], 'r'))
#     workers = utilities.create_workers(config['workers'])
#     tasks = utilities.create_tasks(config['tasks'])
#     highest_score = 0
#     r = -1
#     log = open(f'logs/{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.log', 'w')

#     for i in range(0, 50):
#         total_money, total_time = 0, 0
#         max_time, max_money = 0, 0
#         for task in tasks:
#             max_time += task.get_time()
#             max_money += task.get_money()
#             worker = random.randint(0, 5)
#             # worker = 5
#             money, time = workers[worker].work(task)

#             total_money += money
#             total_time += time
#         tasks = utilities.create_tasks(config['tasks'])
        
#         time_score = round(1 - (total_time / max_time), 2)
#         money_score = round((total_money / max_money), 2)
#         score = round((1 - time_score) + money_score, 2)
#         output = f'''

# **********************************************
# Round: {i}
# ==============================================
# Total time:          {round(total_time, 2)} / {round(max_time, 2)} hrs
# Company benefits:  $ {round(total_money, 2)} / {round(max_money, 2)}
# Employee benefits: $ {round(max_money-  total_money, 2)} / {round(max_money, 2)}

# Cut time down by: % {time_score}
# Company kept:     $ {money_score}
#                     =
# Score:              {score}
# '''
#         print(output)
#         log.write(output)
#         if score >= highest_score:
#             highest_score = score
#             r = i
#     final = f'''
# ______________________
# Highest score: {highest_score}
# Round:         {r}
# '''
#     log.write(final)
#     print(final)
import gym
import gym_proj
import os
import numpy as np
# My stuff
from model.DQN import *
from sim.utils import *
from gym_proj.env.proj_env import *


if __name__ == "__main__":
    args = parse_args()
    m_config, e_config = load_configs(args)
    workers, tasks = config_sim(e_config)


    env = ProjEnv(workers, len(tasks))
    model = DQNAgent(len(workers), args.steps)

    # Notes:
    #     state_size: 4
    #         0: Current Money Made
    #         1: Time Left
    #         2: Tasks left
    #         3: Current Task
    for epoch in tqdm(range(args.epochs)):
        overall_reward = 0
        _, tasks = config_sim(e_config) # Workers are alwasy the same
        next_task = tasks.pop()
        curr_state = np.asarray(env.reset() + next_task.to_arr(), dtype=np.float32)


        # worker_id is the action
        worker_id = model.predict(curr_state) # Start with a brand new state 
        for i in range(args.steps):
            next_state, reward, done = env.step(worker_id, next_task)
            overall_reward += reward
            next_task = tasks.pop()
            next_state += next_task.to_arr()
            next_state = np.asarray(next_state, dtype=np.float32)


            model.remember(curr_state, worker_id, overall_reward, next_state, done)
            if done:
                model.update_target_model()
                break
            curr_state = next_state
            curr_state = np.asarray(curr_state, dtype=np.float32)
            worker_id = model.predict(curr_state)
        model.train()


print(f'Evaluating')
log = open('ouput.log', 'w')
for n in tqdm(range(0, 5)):
    _, tasks = config_sim(e_config)
    # Evaluate
    next_task = tasks.pop()
    curr_state = np.asarray(env.reset() + next_task.to_arr(), dtype=np.float32)

    worker_id = model.predict(curr_state) # Start with a brand new state 
    max_money = 0
    max_time = 0
    for i in range(args.steps):
        log.write(f'Current Task:\n')
        log.write(f'\tMoney ${next_task.get_money()}:\n')
        log.write(f'\tTime {next_task.get_time()}:\n')
        log.write(f'Worker: {worker_id}\n')
        log.write(f'Money earned: ${round(curr_state[0], 2)}\n')
        log.write(f'Time Left: {curr_state[1]}\n')
        log.write(f'Tasks Left: {curr_state[2]}\n')

        log.write('==========================\n')
        next_state, reward, done = env.step(worker_id, next_task)
        next_task = tasks.pop()
        next_state += next_task.to_arr()
        next_state = np.asarray(next_state, dtype=np.float32)

        max_time += next_task.get_time()
        max_money += next_task.get_money()


        if done:
            break
        curr_state = next_state
        curr_state = np.asarray(curr_state, dtype=np.float32)
        worker_id = model.predict(curr_state)
    log.write(f'Max money: ${max_money}\n')
    log.write(f'Max time: {max_time}\n')
    log.write('==============================================================================\n')
