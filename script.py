import csv
import statistics
import traci

traci.start(["sumo-gui", "-c", ".\s-test.sumocfg"])

time_step_size = 1.0


with open('simulation_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    while traci.simulation.getMinExpectedNumber() > 0:
        # get the current time
        simulation_time = traci.simulation.getTime()
        # gives the step number
        time_step_number = int(simulation_time/time_step_size)
        # advance the simulation by one step
        traci.simulationStep()

        vehicle_ids = traci.vehicle.getIDList()
        # magenta
        # vehicle_ids = [vid for vid in traci.vehicle.getIDList()
        #    if 'west-end-car-flow' in vid]

        # blue
        # vehicle_ids = [vid for vid in traci.vehicle.getIDList()
        #    if 'northwest-end-car-flow' in vid]

        # red
        # vehicle_ids = [vid for vid in traci.vehicle.getIDList()
        #    if 'start-end-car-flow' in vid]

        vehicle_positions = {}
        vehicle_coordinates = []
        for vehicle_id in vehicle_ids:
            position = traci.vehicle.getPosition(vehicle_id)
            vehicle_positions[vehicle_id] = position
            vehicle_coordinates.append(position)

        positions_y = [pos[1] for pos in vehicle_positions.values()]
        positions_x = [pos[0] for pos in vehicle_positions.values()]

        std_dev_y = statistics.stdev(positions_y) if len(
            positions_y) >= 2 else None
        std_dev_x = statistics.stdev(positions_x) if len(
            positions_x) >= 2 else None
        std_dev = (std_dev_x, std_dev_y)

        mean_y = statistics.mean(positions_y) if len(
            positions_y) >= 2 else None
        mean_x = statistics.mean(positions_x) if len(
            positions_x) >= 2 else None
        mean = (mean_x, mean_y)

        if time_step_number == 0:
            header_row = ['TimeStamp'] + \
                ['Standard Deviation between Vehicle Coordinates'] + \
                ['Mean Position of Vehicle Coordinates'] + \
                ['Position of Vehicles']
            writer.writerow(header_row)

        row_data = [time_step_number] + [std_dev] + \
            [mean] + [vehicle_coordinates]
        writer.writerow(row_data)

    traci.close()
