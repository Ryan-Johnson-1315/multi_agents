import sys
from utils import utilities
import json
import random
import datetime

if __name__ == "__main__":
    config = json.load(open(sys.argv[1], 'r'))
    workers = utilities.create_workers(config['workers'])
    tasks = utilities.create_tasks(config['tasks'])
    highest_score = 0
    r = -1
    log = open(f'logs/{datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}.log', 'w')

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
        
        time_score = round(1 - (total_time / max_time), 2)
        money_score = round((total_money / max_money), 2)
        score = round((1 - time_score) + money_score, 2)
        output = f'''

**********************************************
Round: {i}
==============================================
Total time:          {round(total_time, 2)} / {round(max_time, 2)} hrs
Company benefits:  $ {round(total_money, 2)} / {round(max_money, 2)}
Employee benefits: $ {round(max_money- total_money, 2)} / {round(max_money, 2)}

Cut time down by: % {time_score}
Company kept:     $ {money_score}
                    =
Score:              {score}
'''
        print(output)
        log.write(output)
        if score >= highest_score:
            highest_score = score
            r = i
    final = f'''
______________________
Highest score: {highest_score}
Round:         {r}
'''
    log.write(final)
    print(final)
