import argparse
import os
from pathlib import Path
import datetime

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Reads in the experiment data for evolutionary robotics experiments')
parser.add_argument('--input-path', '-i', metavar='INPUT_PATH', default=os.getcwd(),
                    help='The folder containing the runs of the experiment. Will default to the working directory if not provided.')
parser.add_argument('--output-path', '-o', metavar='OUTPUT_PATH',
                    help='Write the solution to this filepath. In case no output is given, writes to the experiment folder.')
parser.add_argument('--group-name', '-g', metavar='GROUP_NAME', required=True,
                    help='The name of the group who ran the experiment e.g. C, D or CD.')
parser.add_argument('--world-name', '-w', metavar='WORLD_NAME', default='tol_ground',
                    help='The name of the world used for this experiment. World name is tol_ground in case none is provided.')
parser.add_argument('--experiment-id', '-e', metavar='EXPERIMENT_ID', default=os.path.basename(os.getcwd()),
                    help='The name of the experiment that was performed. By default uses the name of the folder the code lies in.')
args = parser.parse_args()

group_name = args.group_name
world_name = args.world_name
experiment_id = args.experiment_id
experiment_path = Path(args.input_path) / experiment_id
output_base_path = experiment_path if args.output_path is None else args.output_path

if not experiment_path.exists():
    raise Exception(f'Experiment {str(experiment_path)} does not exist.')

dataframes = []
dataframes_history = []
for run_path in experiment_path.iterdir():
    if run_path.is_dir():
        run_id = run_path.name
        df = pd.read_csv(run_path / 'measures2.txt', sep=' ')
        df.rename(columns={'genome': 'genome_id'}, inplace=True)
        df = pd.pivot_table(df, values='value', index=['generation', 'genome_id'],
                            columns=['measures'], aggfunc='last')

        df_history = pd.read_csv(run_path / 'history.txt', sep=' ')
        df_history.rename(columns={'idgenome': 'genome_id', 'idparent1': 'parent1_id',
                                   'idparent2': 'parent2_id'}, inplace=True)
        df_history.columns.rename('measures', inplace=True)
        df_history.set_index(['generation', 'genome_id'], inplace=True)
        df_history.drop(df_history.columns[-1], axis=1, inplace=True)
        for c in ['parent1_id', 'parent2_id']:
            df_history[c] = df_history[c].replace('N', np.nan).astype(float)

        df = df.join(df_history, how='inner')
        df = pd.concat([df], keys=[run_id], names=['run_id'])
        dataframes.append(df)

df = pd.concat(dataframes)
n_rows = len(df)
n_files = len(dataframes)
print(f'Found {n_rows} rows in {n_files} runs ({n_rows // n_files} on average)')


def get_file_name(group_name: str, world_name: str, experiment_id: str, with_date: bool = False) -> str:
    if with_date:
        date = '_date=' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    else:
        date = ''
    name = f'experiment_grp={group_name}_wld={world_name}_exp={experiment_id}{date}.hdf5'
    return name


output_file_path = output_base_path / get_file_name(group_name, world_name, experiment_id)
print(f'Wrote hdf5 file to {str(output_file_path)}')
df.to_hdf(output_file_path, key='descriptors')
