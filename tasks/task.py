# 
class Task:
    def __init__(self, time: float, money: float):
        self._time_to_complete = time
        self._available_money  = money
    
    def get_money(self):
        return self._available_money
    
    def get_time(self):
        return self._time_to_complete

    def get_rank(self):
        return self._rank

    def __str__(self):
        return f"""
Time for completion:   {self._time_to_complete} hrs
Money upon completion: $ {self._available_money}
        """