import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stable_baselines3 import PPO
from env.carla_env import CarlaRegenEnv

def run():
    env = CarlaRegenEnv()
    model = PPO.load("models/regen_model")

    obs, _ = env.reset()

    while True:
        action, _ = model.predict(obs)
        obs, reward, done, _, _ = env.step(action)

        if done:
            obs, _ = env.reset()
    env.close()

if __name__ == "__main__":
    run()