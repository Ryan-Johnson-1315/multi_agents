import json

data = json.load(open('configs/all_stats.json', 'r'))


sim = {}
workers = {}
for i in data:
    for worker in data[i]:
    
        num_jobs = len(data[i][worker])
        time = 0
        pay  = 0
    
        for job in data[i][worker]:
            time += job[0]
            pay  += job[1]

        workers[f'worker_{worker}'] = {
            'Total Time': time,
            'Average Time': float(time / num_jobs),
            'Total Pay': pay,
            'Average Pay': float(pay / num_jobs),
            'Num Jobs': num_jobs
        }
    sim[f'sim_{i}'] = workers


json.dump(sim, open('configs/updated_avg.json', 'w'))