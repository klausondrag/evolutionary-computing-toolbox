import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import numpy as np
from matplotlib.pyplot import cm


def plot_mean_and_max_fitness(mean_fitness, max_fitness):
    
    plt.figure(1)
    plt.xlim(0, n_gens + 15)
    plt.plot(mean_fitness, label='mean fitness')
    plt.plot(max_fitness, label='max fitness')
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Mean and max fitness over generations")
    plt.legend(loc='upper right')
    plt.show()
    
    
def fetch_body_image(exp_path, generation, robot_id):
    
    search_dir = exp_path + "/selectedpop" + str(generation)
    regex = "body_%s_" % robot_id
    for file_name in os.listdir(search_dir):
        if re.match(regex, file_name):
            robot_img = mpimg.imread(os.path.join(search_dir, file_name))   
            return robot_img


def fetch_brain_image(exp_path, generation, robot_id):

    search_dir = exp_path + "/selectedpop" + str(generation)
    robot_brain_img = mpimg.imread(os.path.join(search_dir, "brain_%s.png" % robot_id))
    return robot_brain_img


def find_best_in_gen(exp_name):

    exp_path = base_dir + exp_name
    evolution_file_path = exp_path + "/evolution.txt"
    evol_df = pd.read_csv(evolution_file_path, sep=' ')
    best_in_gen = evol_df['idbest_fin']
    return best_in_gen

    
def display_best_body_in_gen(exp_name):

    exp_path = base_dir + exp_name
    best_in_gen = find_best_in_gen(exp_name)

    for (index, best_id) in best_in_gen.iteritems():
        if index > 0:
            robot_img = fetch_body_image(exp_path, index + 1, best_id)
            plt.figure(2)
            plt.subplot(5, 10, index + 1)
            plt.axis('off')
            plt.imshow(robot_img)
            plt.title("G" + str(index + 1))
    plt.show()


def display_best_body_in_gen_seq(exp_name):

    exp_path = base_dir + exp_name
    best_in_gen = find_best_in_gen(exp_name)

    for (index, best_id) in best_in_gen.iteritems():
        if index > 0:
            robot_img = fetch_body_image(exp_path, index + 1, best_id)
            plt.figure(3)
            plt.clf()
            plt.imshow(robot_img)
            plt.axis('off')
            plt.title("Generation " + str(index + 1))
            plt.pause(0.5)
            plt.show()


def display_best_brain_in_gen_seq(exp_name):

    exp_path = base_dir + exp_name
    best_in_gen = find_best_in_gen(exp_name)

    for (index, best_id) in best_in_gen.iteritems():
        if index > 0:
            robot_brain_img = fetch_brain_image(exp_path, index + 1, best_id)
            plt.figure(4)
            plt.clf()
            plt.imshow(robot_brain_img)
            plt.axis('off')
            plt.title("Generation " + str(index + 1))
            plt.pause(0.5)
            plt.show()

def calculate_mean_measures(measures_df):

    mean_measures = pd.DataFrame(columns=measures_list)
    for i in xrange(2, n_gens + 1):
        gen_measures = measures_df.loc[measures_df.generation == i]
        for m in measures_list:
            measure_mean = gen_measures.loc[gen_measures.measures == m, 'value'].mean()
            mean_measures.loc[i - 2, m] = measure_mean
    return mean_measures
    
    
def plot_mean_measures(mean_measures):
    
    plt.figure(4) 
    plt.xlim(0, n_gens + 15)
    plt.ylim(-0.1, 1.1)
    number_of_plots = len(mean_measures.columns)
    color = iter(cm.rainbow(np.linspace(0, 1, number_of_plots)))
    for m in measures_list:
        c = next(color)
        plt.plot(range(2, n_gens + 1), mean_measures[m].values, label=m, linewidth=1.5, color=c)
    plt.legend(loc='upper right', fontsize='small')
    plt.xlabel("Generation")
    plt.ylabel("Mean value of measure")        
    plt.show()    


if __name__ == "__main__":
    
    n_runs = 3  
    n_gens = 50
    base_dir = "/home/nithinholla/projects/revolve-simulator/l-system/experiments/baseline/"
    exp_names = ["nithin", "lromor", "klaus"]
    chosen_exp = "lromor"
    
    mean_fitness_averaged = pd.Series(0, index=range(n_gens))
    max_fitness_averaged = pd.Series(0, index=range(n_gens))
    mean_measures_averaged = None
    
    for exp_name in exp_names:
        exp_path = base_dir + exp_name
        evolution_file_path = exp_path + "/evolution.txt"
        measures_file_path = exp_path + "/measures2.txt"
        
        evol_df = pd.read_csv(evolution_file_path, sep=' ')
        measures_df = pd.read_csv(measures_file_path, sep=' ')
        measures_list = measures_df.measures.unique()
        
        mean_measures = calculate_mean_measures(measures_df)
        if mean_measures_averaged is None:
            mean_measures_averaged = pd.DataFrame(0, index=range(n_gens - 1), columns=measures_list)
        mean_measures_averaged = mean_measures_averaged.add(mean_measures)

        mean_fitness_averaged = mean_fitness_averaged.add(evol_df['meanfit_fin'])
        max_fitness_averaged = max_fitness_averaged.add(evol_df['maxfit_fin'])
    
    mean_fitness_averaged /= n_runs
    max_fitness_averaged /= n_runs
    mean_measures_averaged /= n_runs

    plot_mean_and_max_fitness(mean_fitness_averaged, max_fitness_averaged)
    display_best_body_in_gen(chosen_exp)
    display_best_body_in_gen_seq(chosen_exp)
    display_best_brain_in_gen_seq(chosen_exp)
    plot_mean_measures(mean_measures_averaged)
