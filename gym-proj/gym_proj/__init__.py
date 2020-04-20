from gym.envs.registration import register

register(
    id='proj-v0',
    entry_point='gym_proj.env:ProjEnv',
)   