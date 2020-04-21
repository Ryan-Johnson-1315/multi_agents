import random

# Any kind of task
class Task:
    def __init__(self, time: float, money: float):
        self._time_to_complete = time
        self._available_money  = money
    
    def get_money(self):
        return self._available_money
    
    def get_time(self):
        return self._time_to_complete
    
    def to_arr(self):
        return [self._time_to_complete, self._available_money]

    def get_rank(self):
        return self._rank

    def __str__(self):
        return f"""
Time for completion:   {self._time_to_complete} hrs
Money upon completion: $ {self._available_money}
"""


# Each worker
class Worker:
    def __init__(self, pay: float, time: float, rank: int):
        self._pay  = pay
        self._time = time
        self._rank = rank
    
    def work(self, task: Task):
        money_made = (1 - self._pay) * task.get_money()
        time_used  = self._time * task.get_time()
        return round(money_made, 2), round(time_used, 2)
    
    def __str__(self):
        return f"""
Time to finish the job is:  % {self._time * 100} of time
Cost to pay me for the job: % {self._pay * 100} of cost
"""

def create_tasks(config: dict):
    tasks = []
    for i in range(0, config['total'] + 1):
        t_ratio = config['time_money_ratio']
        time = round(random.uniform(t_ratio['min'], t_ratio['max']), 2)
        m_ratio = config['money']
        money = round(random.uniform(m_ratio['min'], m_ratio['max']), 2)
        t = Task(time, money)
        tasks.append(t)

    return tasks


def create_workers(config: dict):
    workers = []
    time_taken = config['time_start'] 
    money_cost = config['money_start']

    for i in range(0, config['total'] + 1):
        w = Worker(round(money_cost, 2), round(time_taken, 2), i)
        money_cost += config['money_increment']
        time_taken -= config['time_decrement']
        workers.append(w)
        # print(w)
    return workers

