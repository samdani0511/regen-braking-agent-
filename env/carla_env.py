import gymnasium as gym
from gymnasium import spaces
import numpy as np
import carla
from utils.reward import compute_reward
from config.config import *
import time
from navigation.basic_agent import BasicAgent

time.sleep(5)

class CarlaRegenEnv(gym.Env):

    def __init__(self):
        super(CarlaRegenEnv, self).__init__()
    
        import time
        import carla
        self.log_data = {
            "speed": [],
            "distance": [],
            "regen": [],
            "reward": [],
            "energy": [],
            "x": [],
            "y": []
        }



                
        # 1️⃣ Connect to CARLA
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(20.0)
    
        print("Connecting to CARLA...")
        time.sleep(5)
        self.stuck_steps = 0
    
        # 2️⃣ Get world
        self.world = self.client.get_world()
    
        # 3️⃣ Cleanup old vehicles
        actors = self.world.get_actors().filter('vehicle.*')
        for actor in actors:
            actor.destroy()
    
        # 4️⃣ Spawn vehicle
        blueprint_library = self.world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter('vehicle.*')[0]
    
        spawn_points = self.world.get_map().get_spawn_points()
    
        self.vehicle = None
        for sp in spawn_points:
            self.vehicle = self.world.try_spawn_actor(vehicle_bp, sp)
            if self.vehicle is not None:
                print("Vehicle spawned successfully")
                break
    
        if self.vehicle is None:
            raise Exception("Vehicle spawn failed")
        
        self.agent = BasicAgent(self.vehicle)
        # Set destination (random point)
        spawn_points = self.world.get_map().get_spawn_points()
        destination = spawn_points[10].location

        self.agent.set_destination([
            destination.x,
            destination.y,
            destination.z
        ])


        # Spawn obstacle vehicle ahead
        obstacle_bp = blueprint_library.filter('vehicle.*')[1]
        
        spawn_transform = self.vehicle.get_transform()
        
        # Place obstacle 20m ahead
        spawn_transform.location.x += 20  
        
        self.obstacle_vehicle = self.world.try_spawn_actor(obstacle_bp, spawn_transform)
        # 5️⃣ NOW attach sensors (after vehicle exists)
        camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')

        camera_transform = carla.Transform(
            carla.Location(x=-6, z=3),
            carla.Rotation(pitch=-20)
        )
        
        self.camera = self.world.spawn_actor(
            camera_bp,
            camera_transform,
            attach_to=self.vehicle
        )
        
        def camera_callback(image):
            image.save_to_disk(f"output/{image.frame}.png")
        
        self.camera.listen(camera_callback)
        from utils.sensors import attach_collision_sensor, attach_obstacle_sensor
    
        self.collision_sensor, self.collision_data = attach_collision_sensor(self.world, self.vehicle)
        self.obstacle_sensor, self.obstacle_data = attach_obstacle_sensor(self.world, self.vehicle)
    
        # 6️⃣ Init previous values
        self.prev_speed = 0
        self.prev_acc = 0
    
        # 7️⃣ Spaces
        self.action_space = spaces.Box(
            low=0.0, 
            high=0.7,   # limit max braking
            shape=(1,), 
            dtype=np.float32
        )    
    
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, 0, 0], dtype=np.float32),
            high=np.array([1, 1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )

    def get_speed(self):
        vel = self.vehicle.get_velocity()
        
        # speed = sqrt(x^2 + y^2 + z^2)
        speed = (vel.x**2 + vel.y**2 + vel.z**2) ** 0.5
        
        return speed
    
    def get_acceleration(self):
        acc = self.vehicle.get_acceleration()
        return (acc.x**2 + acc.y**2 + acc.z**2) ** 0.5

    def get_state(self):
        vel = self.vehicle.get_velocity()
        acc = self.vehicle.get_acceleration()

        speed = np.sqrt(vel.x**2 + vel.y**2 + vel.z**2)
        acceleration = np.sqrt(acc.x**2 + acc.y**2 + acc.z**2)

        distance = self.obstacle_data.get("distance", 50.0)
        control = self.vehicle.get_control()

        # Normalize
        speed /= MAX_SPEED
        acceleration /= MAX_ACC
        distance /= MAX_DISTANCE

        return np.array([speed, acceleration, distance, control.brake], dtype=np.float32)

    def step(self, action):
        if self.agent.done():
            import random
            spawn_points = self.world.get_map().get_spawn_points()
            destination = random.choice(spawn_points).location
        
            self.agent.set_destination([
                destination.x,
                destination.y,
                destination.z
            ])
        regen = float(action[0])
    
        control = self.agent.run_step()
        control.throttle = max(control.throttle, 0.3)
        control.brake = control.brake * 0.3 + regen * 0.7

        self.vehicle.apply_control(control)
        print(f"Agent control → Throttle: {control.throttle}, Brake: {control.brake}, Steer: {control.steer}")
        state = self.get_state()
    
        speed = state[0] * MAX_SPEED
        acc = state[1] * MAX_ACC
        distance = state[2] * MAX_DISTANCE
    
        collision = 1 if self.collision_data["collision"] else 0
        reward = compute_reward(
                self.prev_speed, speed,
                acc, self.prev_acc,
                regen, distance,
                collision
            )
        # Detect stuck
        if speed < 0.5:
            self.stuck_steps += 1
        else:
            self.stuck_steps = 0
        
        # If stuck too long → end episode
        if self.stuck_steps > 50:
            print("Vehicle stuck → resetting episode")
            terminated = True
        speed = self.get_speed()
        
        if speed < 0.1:
            control.throttle = 0.6
            control.brake = 0.0
            
        self.prev_speed = speed
        self.prev_acc = acc

        # Position
        transform = self.vehicle.get_transform()
        x = transform.location.x
        y = transform.location.y
        
        # Energy calculation
        energy = max(0, 0.5 * 1500 * (self.prev_speed**2 - speed**2))
        
        # Log data
        self.log_data["speed"].append(speed)
        self.log_data["distance"].append(distance)
        self.log_data["regen"].append(regen)
        self.log_data["reward"].append(reward)
        self.log_data["energy"].append(energy)
        self.log_data["x"].append(x)
        self.log_data["y"].append(y)
        terminated = collision == 1
        truncated = False
        print(f"Speed: {speed:.2f}, Regen: {regen:.2f}, Distance: {distance:.2f}, Collision: {collision}")
        print(self.vehicle.get_velocity())
    
        return state, reward, terminated, truncated, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
    
        # Destroy old actors
        self.vehicle.destroy()
        self.collision_sensor.destroy()
        self.obstacle_sensor.destroy()
    
        # Respawn everything
        self.__init__()
    
        return self.get_state(), {}
    
    def close(self):
        if hasattr(self, "camera"):
            self.camera.destroy()
        if hasattr(self, "collision_sensor"):
            self.collision_sensor.destroy()
        if hasattr(self, "obstacle_sensor"):
            self.obstacle_sensor.destroy()
        if hasattr(self, "vehicle"):
            self.vehicle.destroy()