import matplotlib.pyplot as plt
import os

def plot_all(data):
    os.makedirs("graphs", exist_ok=True)

    # 1. Speed
    plt.figure()
    plt.plot(data["speed"])
    plt.title("Speed vs Time")
    plt.xlabel("Step")
    plt.ylabel("Speed")
    plt.savefig("graphs/speed.png")
    plt.close()

    # 2. Distance
    plt.figure()
    plt.plot(data["distance"])
    plt.title("Distance vs Time")
    plt.savefig("graphs/distance.png")
    plt.close()

    # 3. Regen
    plt.figure()
    plt.plot(data["regen"])
    plt.title("Regen Braking vs Time")
    plt.savefig("graphs/regen.png")
    plt.close()

    # 4. Reward
    plt.figure()
    plt.plot(data["reward"])
    plt.title("Reward vs Time")
    plt.savefig("graphs/reward.png")
    plt.close()

    # 5. Energy
    plt.figure()
    plt.plot(data["energy"])
    plt.title("Energy Recovered")
    plt.savefig("graphs/energy.png")
    plt.close()

    # 6. Path
    plt.figure()
    plt.plot(data["x"], data["y"])
    plt.title("Vehicle Path")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig("graphs/path.png")
    plt.close()