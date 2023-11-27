import random
class RobotOptimizer:
    def __init__(self, initial_guess, constraints):
        self.coordinates = initial_guess
        self.constraints = constraints
        self.best_score = float('inf')

    def call_robot_control_function(self, coordinates):
        # Replace this with your actual robot control function call
        reprojection_error = random.uniform(0, 1)  # Mock output
        total_time = random.uniform(0, 30)        # Mock output
        return reprojection_error, total_time

    def calculate_objective(self, reprojection_error, total_time):
        
        return reprojection_error * 500 + total_time

    def check_constraints(self, coordinates):
        return all(self.constraints[dim][0] <= coord <= self.constraints[dim][1] for dim, coord in enumerate(coordinates))

    def generate_neighbors(self, coordinates):
        neighbors = []
        step_size = 0.5  # Define how much each coordinate can vary

        for i in range(len(coordinates)):
            if coordinates[i] + step_size <= self.constraints[i][1]:
                new_coord = coordinates.copy()
                new_coord[i] += step_size
                neighbors.append(new_coord)

            if coordinates[i] - step_size >= self.constraints[i][0]:
                new_coord = coordinates.copy()
                new_coord[i] -= step_size
                neighbors.append(new_coord)
        #print(neighbors)

        return neighbors

    def optimize(self):
        for _ in range(300):  # Maximum of 300 trials
            reprojection_error, total_time = self.call_robot_control_function(self.coordinates)
            current_score = self.calculate_objective(reprojection_error, total_time)

            best_neighbour_history = []
            best_score_history = []

            if current_score < self.best_score:
                self.best_score = current_score
                #print(self.coordinates)
                best_neighbour_history.append(self.coordinates)
                best_score_history.append(self.best_score)

            neighbors = self.generate_neighbors(self.coordinates)
            #print(neighbors)
            best_neighbor = None
            best_neighbor_score = float('inf')

            for neighbor in neighbors:
                if not self.check_constraints(neighbor):
                    continue

                reprojection_error, total_time = self.call_robot_control_function(neighbor)
                neighbor_score = self.calculate_objective(reprojection_error, total_time)


                if neighbor_score < best_neighbor_score:
                    best_neighbor = neighbor
                    best_neighbor_score = neighbor_score

            if best_neighbor_score < current_score:
                self.coordinates = best_neighbor
                if current_score - best_neighbor_score < 5:  # Convergence criteria
                    break
            
            best_neighbour_history.append(best_neighbor)
            best_score_history.append(best_neighbor_score)

            print(best_neighbour_history)
        
        return self.coordinates, self.best_score

# Example usage
xmin = 0
xmax = 5
ymin = 0
ymax = 5
zmin = 0
zmax = 5
wyaw_min = 0
wyaw_max = 5
ppitch_min = 0
ppitch_max = 5
rroll_min = 0
rroll_max = 5

initial_guess = [1, 0, 0, 0, 0, 1]
constraints = [(xmin, xmax), (ymin, ymax), (zmin, zmax), (wyaw_min, wyaw_max), (ppitch_min, ppitch_max), (rroll_min, rroll_max)]
optimizer = RobotOptimizer(initial_guess, constraints)
optimized_coordinates, best_score = optimizer.optimize()
#print (optimized_coordinates)
