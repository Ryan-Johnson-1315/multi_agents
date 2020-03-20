import gym
import gym_proj
import os
import numpy as np
from collections import defaultdict

# My stuff
from model.DQN import *
from sim.utils import *
from gym_proj.env.proj_env import *


if __name__ == "__main__":
    args = parse_args()
    e_config = load_configs(args)
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
        _, tasks = config_sim(e_config) # Workers are always the same
        next_task = tasks.pop()
        curr_state = np.asarray(env.reset() + next_task.to_arr(), dtype=np.float32)

        curr_state = np.reshape(curr_state, [1, 5])

        # worker_id is the action
        worker_id = model.predict(curr_state) # Start with a brand new state 
        for i in range(args.steps):
            next_state, reward, done = env.step(worker_id, next_task)
            overall_reward += reward
            if len(tasks) < 1:
                _, tasks = config_sim(e_config)
            next_task = tasks.pop()
            next_state += next_task.to_arr()
            next_state = np.asarray(next_state, dtype=np.float32)
            next_state = np.reshape(next_state, [1, 5])


            model.remember(curr_state, worker_id, overall_reward, next_state, done)
            if done:
                break
            curr_state = next_state
            curr_state = np.asarray(curr_state, dtype=np.float32)
            worker_id = model.predict(curr_state)
        
        model.update_target_model()
        model.train()

    model.save('configs/model.h5')

    print(f'Evaluating')
    sims = {}
    for n in tqdm(range(5)):
        stats = defaultdict(list)
        _, tasks = config_sim(e_config)
        # Evaluate
        next_task = tasks.pop()
        curr_state = np.asarray(env.reset() + next_task.to_arr(), dtype=np.float32)
        curr_state = np.reshape(curr_state, [1, 5])

        worker_id = model.predict(curr_state) # Start with a brand new state 
        max_money = 0
        max_time = 0
        for i in range(args.steps):
            stats[f'{worker_id}'].append(next_task.to_arr())
            next_state, reward, done = env.step(worker_id, next_task)
            next_task = tasks.pop()
            next_state += next_task.to_arr()
            next_state = np.asarray(next_state, dtype=np.float32)
            next_state = np.reshape(next_state, [1, 5])


            max_time += next_task.get_time()
            max_money += next_task.get_money()



            if done:
                break
            curr_state = next_state
            curr_state = np.asarray(curr_state, dtype=np.float32)
            curr_state = np.reshape(curr_state, [1, 5])

            worker_id = model.predict(curr_state)
        sims[f'test_{n}'] = stats
        

    # json.dump(sims, open('configs/all_stats.json', 'w'))
    tmp = {}
    works = {}
    for i in sims:
        for worker in sorted(sims[i]):
        
            num_jobs = len(sims[i][worker])
            time = 0
            pay  = 0
        
            for job in sims[i][worker]:
                time += job[0]
                pay  += job[1]

            works[f'worker_{worker}'] = {
                'Total Time': time,
                'Average Time': float(time / num_jobs),
                'Total Pay': pay,
                'Average Pay': float(pay / num_jobs),
                'Num Jobs': num_jobs
            }
        tmp[f'sim_{i}'] = works
        works = {}

    for c, w in enumerate(workers):
        print(f'{c}. {w}')

    json.dump(tmp, open('configs/averages.json', 'w'))