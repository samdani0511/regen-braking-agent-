import carla

import numpy as np
import cv2

import numpy as np
import cv2

def camera_callback(image, video_writer, env=None):
    # Convert CARLA raw image → numpy array
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))

    # Convert BGRA → BGR
    frame = array[:, :, :3]

    # 🔥 FIX: make writable copy (VERY IMPORTANT)
    frame = frame.copy()

    # ===== Overlay Info =====
    if env is not None:
        cv2.rectangle(frame, (5, 5), (350, 180), (0, 0, 0), -1)

        cv2.putText(frame, f"Speed: {env.current_speed:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"Regen: {env.current_regen:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

        cv2.putText(frame, f"Brake: {env.current_brake:.2f}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)

        cv2.putText(frame, f"Reward: {env.current_reward:.2f}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    # Write frame
    if video_writer is not None:
        video_writer.write(frame)

def attach_collision_sensor(world, vehicle):
    blueprint = world.get_blueprint_library().find('sensor.other.collision')

    sensor = world.spawn_actor(
        blueprint,
        carla.Transform(),
        attach_to=vehicle
    )

    collision_data = {"collision": False}

    def callback(event):
        collision_data["collision"] = True

    sensor.listen(callback)

    return sensor, collision_data

def attach_obstacle_sensor(world, vehicle):
    blueprint = world.get_blueprint_library().find('sensor.other.obstacle')

    blueprint.set_attribute("distance", "50")

    sensor = world.spawn_actor(
        blueprint,
        carla.Transform(carla.Location(x=2.5, z=1.0)),
        attach_to=vehicle
    )

    obstacle_data = {"distance": 50.0}

    def callback(event):
        obstacle_data["distance"] = event.distance

    sensor.listen(callback)

    return sensor, obstacle_data