from config.config import MASS, EFFICIENCY, W_ENERGY, W_JERK, W_COLLISION, W_OVERBRAKE, W_LATE

def compute_reward(prev_speed, speed, acc, prev_acc, regen, distance, collision):

    # Energy recovery
    energy = 0.5 * MASS * (prev_speed**2 - speed**2)
    energy = max(0, energy)
    energy_recovered = EFFICIENCY * energy

    # Jerk
    jerk = abs(acc - prev_acc)

    # Over braking
    over_braking = max(0, regen - 0.8)

    # Late braking
    safe_distance = speed * 0.5
    late_braking = 1 if distance < safe_distance else 0
    
    reward = 0
    
    # Encourage movement
    reward += 0.1 * speed  
    
    # Energy recovery
    reward += 0.5 * energy_recovered  
    
    # Penalize stopping too much
    if speed < 1:
        reward -= 2  
    
    # Penalize collision
    reward -= 20 * collision  
    
    # Penalize over braking
    reward -= 2 * max(0, regen - 0.7)
    reward = (
        W_ENERGY * energy_recovered
        - W_JERK * jerk
        - W_COLLISION * collision   # ← now comes from sensor
        - W_OVERBRAKE * over_braking
        - W_LATE * late_braking
    )

    return reward