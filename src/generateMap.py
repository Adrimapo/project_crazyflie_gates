import json
import math
import random

NUM_GATES = 10

def get_world():
    dronePosition = [0.0, -3.5, 0.3]
    droneRotation = [0, 0.0, math.pi / 2]
    worldNames = ['empty', 'grass']

    world = {
        "world_name": random.choice(worldNames),
        "drones": [
            {
                "model_type": "quadrotor_base",
                "model_name": "cf0",
                "xyz": dronePosition,
                "rpy": droneRotation,
                "flight_time": 60,
                "payload": [
                    {
                        "model_name": "hd_camera",
                        "model_type": "hd_camera"
                    }
                ]
            }
        ],
        "objects": []
    }
    return world

def get_gates_poses(n_gates):
    # First gate is always the same
    positions = [(0.0, 0.0, 0.0)]
    orientations = [(0.0, 0.0, -1.57)]

    # Constant door values
    z = roll = pitch = 0.0

    for i in range(n_gates-1):
        # Angle between both gates
        center = orientations[-1][2]  # radians
        angle_width = 0.30  # radians
        pos_angle = random.uniform(center - angle_width, center + angle_width)

        # Estimates the x and y
        max_x = 8
        max_y = 4
        d_max = math.sqrt(max_x**2 + max_y**2)
        min_dist = 4

        # Normalizes between 0 and 1
        norm_sin = abs(center -pos_angle) / angle_width

        # Normalizes between minDist and maxDist
        d_min = (norm_sin * (d_max - min_dist)) + min_dist
        distance = random.uniform(d_min, d_max)

        # Gets the random x and y
        x = positions[-1][0] - distance * math.cos(pos_angle)
        y = positions[-1][1] - distance * math.sin(pos_angle)

        # Estimate yaw
        yaw_change = random.uniform(0, 1.04)
        if pos_angle < center:
            yaw_change = -yaw_change

        yaw = center + yaw_change

        # Save the coords
        positions.append((x, y, z))
        orientations.append((roll, pitch, yaw))

    return positions, orientations

def get_gates(world, n_gates):
    positions, orientations = get_gates_poses(n_gates)

    # Generate all the gates
    for i in range(n_gates):
        gate = {
            "model_type": "aruco_gate_2",
            "model_name": f"gate_{i}",
            "xyz": positions[i],
            "rpy": orientations[i],
            "object_bridges": [
                "pose"
            ]
        }
        world["objects"].append(gate) 

    return world

def get_external_objects_data(n_gates):
    world_str = "---\nobjects:\n"
    for i in range(n_gates):
        # Create string for each pose object
        pose_obj_str = f"- type: pose\n  frame: gate_{i}/link\n  pose_topic: \"/gate_{i}/gate_{i}/pose\"\n"  
        world_str += pose_obj_str 
    
    return world_str

def main():

    # Creates the world.json
    world = get_world()
    data = get_gates(world, NUM_GATES)

    with open('../sim_config/world.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Creates the external_objects.yaml to generate the tfs
    externalObjectsData = get_external_objects_data(NUM_GATES)
    with open('../sim_config/external_objects.yaml', 'w') as f:
        f.write(externalObjectsData)

    print("Random world generated!!!")

if __name__ == '__main__':
    main()
