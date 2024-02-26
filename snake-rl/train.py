# import ray
# from ray.rllib.algorithms import ppo
# from ray.tune.registry import register_env
# from snake_env import SnakeEnv

# register_env("Snake_Env", SnakeEnv)

# ray.init()
# algo = ppo.PPO(env="Snake_Env", config={
#     "env_config": {},  # config to pass to env class
# })

# while True:
#     print(algo.train())
from stable_baselines3 import DQN
from main_env import SnakeEnv

env = SnakeEnv({})

try:
    model = DQN.load('model', env=env)
except:
    print("found no model")
    model = DQN("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=1000000, log_interval=10)
model.save('model')
obs = env.reset()[0]
done, truncated = False, False
while not done and not truncated:
    action, _states = model.predict(obs)
    obs, rewards, done, truncated, info = env.step(int(action))
    env.render()
print(done, truncated)