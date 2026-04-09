# Regenerative Braking Optimization using RL

## 🚗 Overview
This project uses CARLA simulator and Reinforcement Learning (PPO)
to optimize regenerative braking for EVs.

## ⚡ Features
- Energy recovery optimization
- Smooth braking (jerk minimization)
- Collision avoidance
- Adaptive control policy

## 🧠 Tech Stack
- CARLA Simulator
- Stable-Baselines3 (PPO)
- Python, Gym

## ▶️ Run

Start CARLA first:
./CarlaUE4.sh

Train:
python models/train.py

Run:
python inference/run_model.py