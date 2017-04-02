import math


def main():
    infinity = math.inf
    # Graph in Adjacency Matrix form for proof of concept
    adjacency_matrix = [[       0,        5,        1, infinity, infinity, infinity],
                        [       3,        0, infinity,        3,        6, infinity],
                        [       1,        3,        0,        3, infinity,        0],
                        [infinity,       -4,        3,        0,        5, infinity],
                        [infinity,        6, infinity,        4,        0,        2],
                        [infinity, infinity,        0,        2, infinity,        0]]

    # Finds the smallest path distance to normalize the graph
    offset = min([item for sublist in adjacency_matrix for item in sublist]) * -1
    if offset != 0:
        offset = offset + 1

    # Normalize the Adjacency MAtrix with the calculated offset
    for row in range(0, len(adjacency_matrix)):
        for col in range(0, len(adjacency_matrix)):
            if row != col and adjacency_matrix[row][col] != infinity:
                adjacency_matrix[row][col] = adjacency_matrix[row][col] + offset

    # Holds the shortest paths from each starting vertex to every other vertex
    shortest_paths = []
    # Hard coding starting vertex to 0 to only test 1 starting point
    starting_vertex = 0
    # for starting_vertex in range(0, len(adjacency_matrix)):
    # If the Bellman-Ford runs into a negative cycle it will return False and exit the program
    valid_cycle = bellman_ford(adjacency_matrix, starting_vertex, offset)
    if (valid_cycle):
        shortest_paths.append(valid_cycle)
    else:
        exit(-1)

    # Single print for now
    # shortest_paths will only contains the paths starting from A
    print(shortest_paths)
    print_paths(shortest_paths, cities)

# Prints the paths from the cities in the desired format
def print_paths(shortest_paths, cities):
    cities = ["Dallas", "New York", "Chicago", "Los Angeles", "Houston", "Salt Lake City"]
    for start in range(0, len(cities)):
        print("%s TO" % cities[start])
        for end in range(0, len(cities)):
            print("\t %s:\t\t%d distance in %d hops" % (cities[end], shortest_paths[start][end]['distance'], shortest_paths[start][end]['hops']))
        print("\n")


def bellman_ford(adjacency_matrix, start_position, offset):
    debug = False
    # Number of vertices
    num_of_vertices = len(adjacency_matrix)
    # Distances list to hold the shortest value to each
    distances_list = []
    # Loops to create the distance list
    for vertex in range(0, num_of_vertices):
        if vertex is start_position:
            distances_list.append({'distance': 0, 'hops': 0})
        else:
            distances_list.append({'distance': math.inf, 'hops': 0})

    # Perform Relaxation Passes
    for passes in range(0, num_of_vertices):
        if debug:
            print("Pass #%d" % passes)
            print("------------------------")
        # Loops through each vertex incrementally and checks its edges
        for start in range(0, num_of_vertices):
            if debug:
                print("* Vertex { %d } Connections *" % start)
            # Only check the edges if there is already a path to the vertex
            if distances_list != math.inf:
                # Starting vertex for directed edges
                current_vertex = distances_list[start]
                # Find all connected edges by brute force
                for end in range(0, num_of_vertices):
                    # Uses the Adjacency Matrix to result in a value of True if the two vertices are connected
                    connected = adjacency_matrix[start][end] != math.inf
                    # Only continues if there is a connection, the connection is not itself, and the connection is not the original starting point
                    if connected and start != end and start_position != end:
                        # Grabs the current shortest path from the starting point to the destination and gets the actual distance from the offset * hops
                        current_shortest = distances_list[end]['distance'] - (distances_list[end]['hops'] * offset)
                        # Calculates actual the distance of the new path
                        new_path = current_vertex['distance'] + adjacency_matrix[start][end] - (offset * (current_vertex['hops'] + 1))

                        if debug:
                            print("Path { %d } -> { %d }" % (start, end))
                            print("Current Shortest to { %d }: %f" % (end, current_shortest))
                            print("New Path to { %d }: %d" % (end, new_path))

                        if new_path < current_shortest:
                            # If we are on the last path and relaxation is still possible, then we have a negative edge
                            if passes == num_of_vertices - 1:
                                print("Negative cycle error in final relaxation.")
                                print("Exiting Program")
                                return False
                            else:
                                # Update the shortest path
                                distances_list[end] = {'distance': current_vertex['distance'] + adjacency_matrix[start][end], 'hops': current_vertex['hops'] + 1}
                                if debug:
                                    print(distances_list)
                                    print("\n")
        # Middle of no-where print line for prettier debug output
        if debug:
            print("\n")

    # Remove the offset from all the distances to get the actual path lengths
    for i in range(0, len(distances_list)):
        distance = distances_list[i]['distance']
        hops = distances_list[i]['hops']
        distances_list[i]['distance'] = distance - (offset * hops)
    # Return distances list
    return distances_list

# Call main close your eyes
main()
