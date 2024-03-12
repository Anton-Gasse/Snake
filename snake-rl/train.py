from stable_baselines3 import PPO
from main_env import SnakeEnv

env = SnakeEnv({})

try:
    model = PPO.load('./models/model', env=env)
    print("found model")
except:
    print("found no model")
    model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=500000, log_interval=10)
model.save('./models/model')
