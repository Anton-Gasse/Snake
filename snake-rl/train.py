import ray
from ray.rllib.algorithms import ppo
from ray.tune.registry import register_env
from snake_env import SnakeEnv

register_env("Snake_Env", SnakeEnv)

ray.init()
algo = ppo.PPO(env="Snake_Env", config={
    "env_config": {},  # config to pass to env class
})

while True:
    print(algo.train())
