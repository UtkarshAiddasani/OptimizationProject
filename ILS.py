import random
class RobotOptimizer:
    def __init__(self, initial_guess, constraints):
        self.coordinates = initial_guess    # initial guess
        self.constraints = constraints      # set constraints
        self.best_score = float('inf')
        self.best_neighbour_history = []  # Initialize neighbour history here
        self.best_score_history = []      # Initialize score history here

    def call_robot_control_function(self, coordinates):         
        reprojection_error = random.uniform(0, 1)  
        total_time = random.uniform(0, 30)        
        return reprojection_error, total_time

    def calculate_objective(self, reprojection_error, total_time):
        
        return reprojection_error * 500 + total_time       # cost calculation

    def check_constraints(self, coordinates):
        return all(self.constraints[dim][0] <= coord <= self.constraints[dim][1] for dim, coord in enumerate(coordinates))     # verify constraints are satisfied 

    def generate_neighbours(self, coordinates):
        neighbours = []
        step_size = 0.5  # Define how much each coordinate can vary

        for i in range(len(coordinates)):
            if coordinates[i] + step_size <= self.constraints[i][1]:          # increment and decrement various coordinates 
                new_coord = coordinates.copy()
                new_coord[i] += step_size                                     
                neighbours.append(new_coord)

            if coordinates[i] - step_size >= self.constraints[i][0]:
                new_coord = coordinates.copy()
                new_coord[i] -= step_size
                neighbours.append(new_coord)
        #print(neighbours)

        return neighbours

    def optimize(self):
        for _ in range(300):  # Maximum of 300 trials
            reprojection_error, total_time = self.call_robot_control_function(self.coordinates)        # extract required data and calculate score
            current_score = self.calculate_objective(reprojection_error, total_time)

            if current_score < self.best_score:                     # stor accordingly
                self.best_score = current_score
                self.best_neighbour_history.append(self.coordinates.copy())  # Update history with a copy of coordinates
                self.best_score_history.append(self.best_score)

            neighbours = self.generate_neighbours(self.coordinates)              # generate neighbours
            best_neighbour = None                                                # reset these vars
            best_neighbour_score = float('inf')

            for neighbour in neighbours:                                         # verify it fits the constraints
                if not self.check_constraints(neighbour):
                    continue

                reprojection_error, total_time = self.call_robot_control_function(neighbour)          # calculate score
                neighbour_score = self.calculate_objective(reprojection_error, total_time)

                if neighbour_score < best_neighbour_score:                      # compare the scores and store accordingly
                    best_neighbour = neighbour 
                    best_neighbour_score = neighbour_score

            if best_neighbour_score < current_score:                            # compare the best of the iteration to the global best 
                self.coordinates = best_neighbour
                if current_score - best_neighbour_score < 5:  # Convergence criteria
                    break
        print(self.best_neighbour_history)

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
