import numpy as np
import random
import sys


random.seed(100)


# Takes an individual and changes him according to the uniform mutation process
def mutate(individual):
    possible_additions = set()
    for key in individual:
        right_block = (key[0]+1,key[1])
        left_block = (key[0]-1,key[1])
        up_block = (key[0],key[1]+1)
        down_block = (key[0],key[1]-1)
        if right_block not in individual:
            possible_additions.add((right_block, 'L'))
        if left_block not in individual:
            possible_additions.add((left_block, 'R'))
        if up_block not in individual:
            possible_additions.add((up_block, 'D'))
        if down_block not in individual:
            possible_additions.add((down_block, 'U'))
    
    chosen_mutation = random.sample(possible_additions,1)[0]
    individual[chosen_mutation[0]] = chosen_mutation[1]

# Returns a float containing the number of limbs value of the individual    
def calculate_limbs(individual):
    lmax = calculate_max_limbs(individual)
    if lmax == 0:
        return 0
    else: 
        l = 0
        for key, cur_dir in individual.items():
            if cur_dir == 'H':
                continue
            right_dir = individual.get((key[0]+1,key[1]))
            left_dir = individual.get((key[0]-1,key[1]))
            up_dir = individual.get((key[0],key[1]+1))
            down_dir = individual.get((key[0],key[1]-1))
            if right_dir == 'L' or left_dir == 'R' or up_dir == 'D' or down_dir == 'U':
                continue
            else:
                l += 1
        return float(l) / lmax

# Calculates the maximum number of limbs of an individual 
def calculate_max_limbs(individual):
    m = len(individual)
    if m >= 6:
        return 2 * int((m-6)/3) + (m-6) % 3 + 4
    else:
        return m-1

# Prints the provided individual on the command line        
def print_robot(individual):
    keys = set(individual.keys())
    min_x = min(keys, key = lambda t: t[0])[0]
    max_x = max(keys, key = lambda t: t[0])[0]
    min_y = min(keys, key = lambda t: t[1])[1]
    max_y = max(keys, key = lambda t: t[1])[1]
    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1, 1):
            try:
                sys.stdout.write(individual[(x,y)])
            except KeyError:
                sys.stdout.write(' ')
        print('')
            
        
# Performs the experiment with an int : population_size, generations and a String : output_path
def run_experiment(population_size, generations, output_path):
    population = np.array([dict({(0,0):'H'}) for i in range(population_size)]) 
    cur_id = 0
    f = open(output_path, 'w')
    f.write("generation id number_of_limbs\n")    
    for gen in range(generations):
        list(map(mutate, population))
        number_of_limbs = np.array(list(map(calculate_limbs,population)))
        for limbs in number_of_limbs:
            f.write("%d %d %f\n" %(gen+1, cur_id, limbs))
            cur_id+=1
        print("Generated gen %d" % (gen+1))
       
            
    f.close()
    
# Add code here for specific experiments with the system
# The code currently mutates a robot size times and prints him and his number_of_limbs  
r = dict({(0,0):'H'})
size = 10
for i in range(size):
    mutate(r)
print("Number of limbs are: " + str(calculate_limbs(r)))
print_robot(r)