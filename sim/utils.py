from argparse import ArgumentParser
import json
from sim.elements import *


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--env_config',
        help='Path to json file to configure the environment',
        required=False, type=str, default='configs/config.json'
    )
    
    parser.add_argument(
        '--steps',
        help='Number of simulations to run for each epoch',
        default=7500, type=int, required=False
    )

    parser.add_argument(
        '--epochs',
        default=100, type=int, required=False
    )
    return parser.parse_args()


def config_sim(config):
    return create_workers(config['workers']), create_tasks(config['tasks'])


def load_configs(args):
    env_config = json.load(open(args.env_config, 'r'))
    return env_config
