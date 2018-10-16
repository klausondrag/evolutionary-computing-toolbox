# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:45:49 2018

@author: Arwin
"""
import argparse, os
parser = argparse.ArgumentParser(description='Reads in the experiment data for evolutionary robotics experiments')
parser.add_argument('--input-path', '-i', metavar='INPUT_PATH', default=os.getcwd(),
                        help='The folder containing the runs of the experiment. Will default to the working directory if not provided.')
parser.add_argument('--output-path', '-o', metavar='OUTPUT_PATH', default=os.getcwd(),
                        help='Write the solution to this filepath. In case no output is given, writes to the experiment folder.')
parser.add_argument('--experiment-name', '-e', metavar='EXPERIMENT_NAME', default=os.path.basename(os.getcwd()),
                        help='The name of the experiment that was performed. By default uses the name of the folder the code lies in.')
parser.add_argument('--world-name', '-w', metavar='WORLD_NAME', default='tol_ground',
                        help='The name of the world used for this experiment. World name is tol_ground in case none is provided.')
parser.add_argument('--group-name', '-g', metavar='GROUP_NAME', required=True,
                        help='The name of the group who ran the experiment e.g. C, D or CD.')
args = parser.parse_args()
# This code adds a command line interface to parse arguments needed for reading in data
# Simply add the code at the top of the reading in procedure and read the arguments as
# args.input_path gives the input path, args.world_name gives the name of the world and so on
