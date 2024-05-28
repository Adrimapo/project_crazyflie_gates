import json
import math
import random

def get_world(dronePosition, droneRotation):
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

def get_gates_poses(dronePosition, droneRotation):
    minDist = 3 # m

    # Only generates one random gate 
    newX = random.uniform(15, 15)
    newY = random.uniform(15, 15)
    newZ = random.uniform(-1.5, 4)

    # Gets a gate with a min distance
    while math.sqrt((newX - dronePosition[0])**2 + (newY - dronePosition[1])**2) < minDist:
        newX = random.uniform(0, 15)
        newY = random.uniform(0, 15)
    
    angle_to_gate = math.atan2(newY - dronePosition[1], newX - dronePosition[0]) - math.pi / 2
    newYaw = random.uniform(-math.pi/2, math.pi/2)

    positions = [(newX, newY, newZ)]
    orientations = [(0.0, 0.0, angle_to_gate + newYaw)]


    return positions, orientations

def get_gates(world, n_gates, dronePosition, droneRotation):
    positions, orientations = get_gates_poses(dronePosition, droneRotation)

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
    NUM_GATES = 1

    # Random drone position
    dronePosition = [random.randint(-10, 10), random.randint(-10, 10), 0.3]
    droneRotation = [0, 0.0, random.uniform(0, 6.28)]

    # Creates the world.json
    world = get_world(dronePosition, droneRotation)
    data = get_gates(world, NUM_GATES, dronePosition, droneRotation)

    with open('../sim_config/world.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Creates the external_objects.yaml to generate the tfs
    externalObjectsData = get_external_objects_data(NUM_GATES)
    with open('../sim_config/external_objects.yaml', 'w') as f:
        f.write(externalObjectsData)

    print("Random world generated!!!")

if __name__ == '__main__':
    main()
