import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import numpy as np
from matplotlib.pyplot import cm


def plot_mean_and_max_fitness(mean_fitness, max_fitness):
    """
    Plots mean and max fitness over generations, averaged over all runs
    :param mean_fitness: Mean fitness
    :param max_fitness: Max fitness
    :return:
    """
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
    """
    Obtains the body image
    :param exp_path: Path containing the experiment data
    :param generation: Generation number
    :param robot_id: ID of the robot
    :return: Image of the robot body
    """
    search_dir = exp_path + "/selectedpop" + str(generation)
    regex = "body_%s_" % robot_id
    for file_name in os.listdir(search_dir):
        if re.match(regex, file_name):
            robot_img = mpimg.imread(os.path.join(search_dir, file_name))
            return robot_img


def fetch_brain_image(exp_path, generation, robot_id):
    """
    Obtains the brain image
    :param exp_path: Path containing the experiment data
    :param generation: Generation number
    :param robot_id: ID of the robot
    :return: Image of the robot brain
    """
    search_dir = exp_path + "/selectedpop" + str(generation)
    robot_brain_img = mpimg.imread(os.path.join(search_dir, "brain_%s.png" % robot_id))
    return robot_brain_img


def find_best_in_gen(exp_name):
    """
    Finds the robot IDs which are best in each generation
    :param exp_name: Name of the experiment
    :return: Vector containing robot IDs which are best in each generation
    """
    exp_path = base_dir + exp_name
    evolution_file_path = exp_path + "/evolution.txt"
    evol_df = pd.read_csv(evolution_file_path, sep=' ')
    best_in_gen = evol_df['idbest_fin']
    return best_in_gen


def display_best_body_in_gen(exp_name):
    """
    Displays the best body in each generation in a single figure
    :param exp_name: Name of the experiment to use for the display
    :return:
    """
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
    """
    Displays the best body in each generation in a sequence
    :param exp_name: Name of the experiment to use for the display
    :return:
    """
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
    """
    Displays the best brain in each generation in a sequence
    :param exp_name: Name of the experiment to use for the display
    :return:
    """
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
    """
    Calculates mean of all the measures over all generations in a given run
    :param measures_df: DataFrame of measures
    :return: Vector of mean measures
    """
    mean_measures = pd.DataFrame(columns=measures_list)
    for i in xrange(2, n_gens + 1):
        gen_measures = measures_df.loc[measures_df.generation == i]
        for m in measures_list:
            measure_mean = gen_measures.loc[gen_measures.measures == m, 'value'].mean()
            mean_measures.loc[i - 2, m] = measure_mean
    return mean_measures


def plot_mean_measures(mean_measures):
    """
    Plots all the mean measures (averaged over all runs) in a single figure
    :param mean_measures: Vector of averaged mean measures
    :return:
    """
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

    n_runs = 5  # Number of runs
    n_gens = 100  # Number of generations
    base_dir = "/home/nithinholla/projects/revolve-simulator/l-system/experiments/"  # Base directory for the experiment data
    exp_names = ["test6", "test7", "test8", "test9", "test10"]  # Names of all the experiments
    chosen_exp = "test6"  # Experiment name for which to display best bodies and brains

    max_fitness_averaged = pd.Series(0, index=range(n_gens))
    mean_fitness_averaged = pd.Series(0, index=range(n_gens))
    mean_measures_averaged = None

    for exp_name in exp_names:
        exp_path = base_dir + exp_name
        evolution_file_path = exp_path + "/evolution.txt"
        measures_file_path = exp_path + "/measures2.txt"

        evol_df = pd.read_csv(evolution_file_path, sep=' ')  # DataFrame for data from evolution.txt
        measures_df = pd.read_csv(measures_file_path, sep=' ')  # DataFrame for data from measures2.txt
        measures_list = measures_df.measures.unique()

        mean_measures = calculate_mean_measures(measures_df)
        if mean_measures_averaged is None:
            mean_measures_averaged = pd.DataFrame(0, index=range(n_gens - 1), columns=measures_list)
        mean_measures_averaged = mean_measures_averaged.add(mean_measures)  # Aggregate measures

        mean_fitness_averaged = mean_fitness_averaged.add(evol_df['meanfit_fin'])  # Aggregate mean fitness
        max_fitness_averaged = max_fitness_averaged.add(evol_df['maxfit_fin'])  # Aggregate max fitness

    mean_fitness_averaged /= n_runs  # Obtain average
    max_fitness_averaged /= n_runs  # Obtain average
    mean_measures_averaged /= n_runs  # Obtain average

    plot_mean_and_max_fitness(mean_fitness_averaged, max_fitness_averaged)
    display_best_body_in_gen(chosen_exp)
    display_best_body_in_gen_seq(chosen_exp)
    display_best_brain_in_gen_seq(chosen_exp)
    plot_mean_measures(mean_measures_averaged)
