## Worker - Task Reinforcement Simulation

### Installation
    > python3.7 -m venv env
    > which pip3
        env/bin/pip3
    > pip3 install -r requirements.txt
This will install all of the packages to run the simulation. 

### Run Simulation

Once everything is installed the simulation can be run with the following commmand

    python main.py --model_config configs/model.json --epochs 150

The simulation can be tweaked and changed by editing the config file. The config file will adjust how many workers there are, each workers take home money and time it takes to complete each task. Tasks can also be edited in the config file