# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 12:45:49 2018

@author: Arwin
"""
import argparse, os
parser = argparse.ArgumentParser(description='Reads in experiment data for groups C and D')
parser.add_argument('--input-path', '-i', metavar='INPUT_PATH', default=os.getcwd(),
                        help='The folder containing the runs of the experiment. Will default to the working directory if not provided.')
parser.add_argument('--output-path', '-o', metavar='OUTPUT_PATH', default=os.getcwd(),
                        help='Write the solution to this filepath. In case no output is given, writes to the experiment folder.')
parser.add_argument('--experiment-name', '-e', metavar = 'EXPERIMENT_NAME', required=True,
                        help='The name of the experiment that was performed.')
parser.add_argument('--world-name', '-w', metavar = 'WORLD_NAME', required=True,
                        help='The name of the world used for this experiment. ')
parser.add_argument('--group-name', '-g', metavar = 'GROUP_NAME', required=True,
                        help='The name of the group who ran the experiment e.g. C, D or CD.')
args = parser.parse_args()

