from tasks import task

class Worker:
    def __init__(self, pay: float, time: float, rank: int):
        self._pay  = pay
        self._time = time
        self._rank = rank
    
    def work(self, task: task.Task):
        money_made = (1 - self._pay) * task.get_money()
        time_used  = self._time * task.get_time()
        return round(money_made, 2), round(time_used, 2)
    
    def __str__(self):
        return f"""
Time to finish the job is:  % {self._time * 100} of time
Cost to pay me for the job: % {self._pay * 100} of cost
        """