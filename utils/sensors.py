import carla

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