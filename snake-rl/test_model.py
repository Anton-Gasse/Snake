from stable_baselines3 import PPO
from main_env import SnakeEnv

env = SnakeEnv({})
model = PPO.load('./models/model', env=env)

obs = env.reset()[0]
done, truncated = False, False
while not done and not truncated:
    action, _states = model.predict(obs)
    obs, rewards, done, truncated, info = env.step(int(action))
    env.render()
print(done, truncated)