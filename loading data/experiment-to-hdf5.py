from pathlib import Path
import datetime
from typing import Optional

import numpy as np
import pandas as pd
import click


@click.command()
@click.argument('experiment-path', type=click.Path(exists=True, file_okay=False))
@click.argument('group-name', type=str)
@click.argument('world-name', type=str)
@click.option('--output-path', '-o', type=click.Path(exists=True, file_okay=False),
              help='Write the solution to this filepath. In case no output is given, writes to the experiment folder')
def convert(experiment_path: click.Path, group_name: str, world_name: str, output_path: Optional[click.Path]) -> None:
    experiment_path = Path(str(experiment_path))
    experiment_id = experiment_path.name
    output_base_path = experiment_path if output_path is None else output_path

    dataframes = []
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


if __name__ == '__main__':
    convert()
