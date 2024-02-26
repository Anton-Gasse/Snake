from stable_baselines3 import DQN
from main_env import SnakeEnv

env = SnakeEnv({})
model = DQN.load('model', env=env)

obs = env.reset()[0]
done, truncated = False, False
while not done and not truncated:
    action, _states = model.predict(obs)
    obs, rewards, done, truncated, info = env.step(int(action))
    env.render()
print(done, truncated)