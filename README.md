# 🚗 Regenerative Braking Efficiency Maximizer (CARLA + RL)

## 📌 Overview

This project implements a **Reinforcement Learning (RL)-based regenerative braking system** integrated with the CARLA autonomous driving simulator.

The goal is to:

* Maximize **energy recovery** during braking ⚡
* Maintain **smooth driving experience** 🚗
* Avoid **collisions and harsh braking**

The system uses:

* **CARLA Simulator** for realistic driving environment
* **BasicAgent** for autonomous navigation
* **PPO (Proximal Policy Optimization)** for learning braking strategy

---

## 🧠 System Architecture

```
Autonomous Driving (CARLA BasicAgent)
                +
Reinforcement Learning Model (PPO)
                ↓
Optimized Regenerative Braking
```

* BasicAgent → Handles steering & navigation
* RL Model → Controls braking (regen intensity)

---

## 🎯 Key Features

* ✅ Hybrid control (Rule-based + RL)
* ✅ Real-time vehicle simulation (CARLA)
* ✅ Energy recovery optimization
* ✅ Dynamic environment interaction
* ✅ Training visualization (graphs)

---

## 📂 Project Structure

```
regen/
│── env/
│   └── carla_env.py        # Custom RL environment
│
│── models/
│   └── train.py            # Training script (PPO)
│
│── inference/
│   └── run_model.py        # Run trained model
│
│── utils/
│   ├── reward.py           # Reward function
│   ├── sensors.py          # Sensor utilities
│   └── plotter.py          # Graph generation
│
│── config/
│   └── config.py           # Constants (mass, etc.)
│
│── graphs/                 # Output graphs
│── logs/                   # Training logs
│── main.py                 # Entry point
│── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install CARLA

* Download CARLA (0.9.x)
* Run simulator:

```bash
CarlaUE4.exe
```

---

### 2️⃣ Install Dependencies

```bash
pip install stable-baselines3
pip install gymnasium
pip install numpy matplotlib networkx
```

---

### 3️⃣ Set CARLA Python API

```bash
set PYTHONPATH=%PYTHONPATH%;C:\Path\To\CARLA\PythonAPI\carla\dist\carla-*.egg
```

---

## 🚀 How to Run

### ▶️ Train Model

```bash
python main.py
# Select option 1
```

---

### ▶️ Run Trained Model

```bash
python main.py
# Select option 2
```

---

## 📊 Outputs (Graphs)

After training, graphs are saved in `/graphs`:

* 📈 Speed vs Time
* 📉 Distance vs Time
* ⚡ Regenerative Braking
* 💰 Reward Curve
* 🔋 Energy Recovered
* 🛣️ Vehicle Path

---

## 📷 Results & Visualizations

### 🚗 Simulation 
<img width="800" height="600" alt="390876" src="https://github.com/user-attachments/assets/21762869-2014-4a95-9989-20027188cbf1" />

<img width="800" height="600" alt="392012" src="https://github.com/user-attachments/assets/c71cab30-3f79-47a9-b9c8-a5b7d62aed77" />

---

### 📊 Training Graphs

#### Speed Graph

<img width="640" height="480" alt="speed" src="https://github.com/user-attachments/assets/e0ea3f0b-27f6-41ad-a4c6-702075ee1068" />

#### Distance Graph

<img width="640" height="480" alt="distance" src="https://github.com/user-attachments/assets/ec156ba3-693d-4dcf-9112-6df8409ac563" />

#### Regen Braking

<img width="640" height="480" alt="regen" src="https://github.com/user-attachments/assets/0b95861f-c341-4eed-8c3a-bdd90250aebe" />

#### Reward Curve

<img width="640" height="480" alt="reward" src="https://github.com/user-attachments/assets/63de2a0a-349a-4290-bd56-28874382e95f" />

#### Energy Recovery

<img width="640" height="480" alt="energy" src="https://github.com/user-attachments/assets/8fa485a6-877f-42fb-88bd-22cacfefeabc" />


---



### 🎥 Demo Video

https://github.com/user-attachments/assets/f452a077-6fc9-4a84-b772-8e17e7bfaeaa





## Full video
https://drive.google.com/file/d/1ulkmTZd7qeW0q9_mHmWWex3r0VBJ6L1c/view?usp=sharing




---

## 🧮 Reward Function

The reward is designed to balance:

* ⚡ Energy recovery
* 🚗 Smooth braking
* 🚫 Collision avoidance
* ⚖️ Speed maintenance

Example:

```python
reward = (
    + energy_recovered
    - jerk
    - collision_penalty
    - over_braking_penalty
)
```

---

## 🚨 Challenges Faced

* Vehicle getting stuck (fixed with reset logic)
* RL over-braking (fixed via reward shaping)
* Sensor delays in CARLA
* Gym → Gymnasium compatibility issues

---

## 📈 Future Improvements

* 🚗 Multi-vehicle traffic scenarios
* 🌧️ Weather-based adaptation
* 📡 Real-time sensor fusion (LiDAR, camera)
* 🤖 Deep learning-based perception
* 📊 Comparison with traditional braking systems

---

## 🧠 Applications

* Electric Vehicles (EVs) ⚡
* Autonomous driving systems 🚗
* Smart energy optimization 🔋
* Driver behavior modeling

---

## 👨‍💻 Author

**Shaik Mohammed Samdani**
AIML Student | Developer | Research Enthusiast

---

## ⭐ Acknowledgements

* CARLA Simulator
* Stable-Baselines3
* OpenAI Gymnasium

---

## 📌 Note

This project demonstrates how **AI + simulation** can be used to solve real-world problems in **energy efficiency and autonomous driving**.

---

## 🚀 Final Thought

> “Not just making cars drive — but making them drive smarter.”
