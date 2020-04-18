from gym.envs.registration import register

register(
    id='work-v0',
    entry_point='gym_work.envs:WorkEnv'
)