from tasks import task
from workers import worker
import random

def create_tasks(config: dict) -> task.Task:
    tasks = []
    for i in range(0, config['total'] + 1):
        t_ratio = config['time_money_ratio']
        time = round(random.uniform(t_ratio['min'], t_ratio['max']), 2)
        m_ratio = config['money']
        money = round(random.uniform(m_ratio['min'], m_ratio['max']), 2)
        t = task.Task(time, money)
        tasks.append(t)

    return tasks


def create_workers(config: dict) -> worker.Worker:
    workers = []
    time_taken = config['time_start'] 
    money_cost = config['money_start']

    for i in range(0, config['total'] + 1):
        w = worker.Worker(round(money_cost, 2), round(time_taken, 2), i)
        money_cost += config['money_increment']
        time_taken -= config['time_decrement']
        workers.append(w)
    return workers