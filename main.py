import sys
from utils import utilities
import json
import random

if __name__ == "__main__":
    config = json.load(open(sys.argv[1], 'r'))
    workers = utilities.create_workers(config['workers'])
    tasks = utilities.create_tasks(config['tasks'])
    highest_score = 0
    r = -1

    for i in range(0, 50):
        total_money, total_time = 0, 0
        max_time, max_money = 0, 0
        for task in tasks:
            max_time += task.get_time()
            max_money += task.get_money()
            worker = random.randint(0, 5)
            # worker = 5
            money, time = workers[worker].work(task)

            total_money += money
            total_time += time
        tasks = utilities.create_tasks(config['tasks'])
        print(f'\n*******************************************')
        print(f'Round: {i}')
        print(f'=============================================')
        print(f'Total time:         {round(total_time, 2)} hrs')
        print(f'Total money:      $ {round(total_money, 2)}')
        print(f'Needed time:        {round(max_time, 2)} hrs')
        print(f'Available money:  $ {round(max_money, 2)}')
        print()
        time_score = round(1 - (total_time / max_time), 2)
        money_score = round((total_money / max_money), 2)
        print(f'Cut time down by: % {time_score}')
        print(f'Company kept:     % {money_score}')
        score = round((1 - time_score) + money_score, 2)
        print(f'Score:              {score}')
        if score > highest_score:
            highest_score = score
            r = i
    print(f'______________________')
    print(f'Highest score: {score}')
    print(f'Round: {r}')
    