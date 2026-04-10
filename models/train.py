from stable_baselines3 import PPO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.carla_env import CarlaRegenEnv
def train():
    env = CarlaRegenEnv()

    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=0.0003,
        ent_coef=0.01,   # encourages exploration
        verbose=1
    )

    model.learn(total_timesteps=20000)
    model.save("models/regen_model")
    from utils.plotter import plot_all

    plot_all(env.log_data)
    env.envs[0].close()
if __name__ == "__main__":
    train()