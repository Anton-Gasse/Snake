from stable_baselines3 import PPO
from stable_baselines3 import DQN
from main_env import SnakeEnv

env = SnakeEnv({})

try:
    model = PPO.load('./models/model', env=env)
    print("found model")
except:
    print("found no model")
    model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=1500000, log_interval=4)
model.save('./models/model')
