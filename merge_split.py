import os
import jsonlines
import pandas as pd
import argparse

def merge(datasets, names):

    df1 = pd.read_csv(datasets[0])
    for df in datasets[1:]:
        df1 = df1.append(df)
    df1.to_csv(names[0])

def split(datasets, names):

    with open(datasets[0]) as final, open(names[0], 'w') as first,\
    open(names[1], 'w') as second:
        for line in final.readlines():
            source,target = line.split('\t')
            first.write(source+'\n')
            second.write(target)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', default='merge')
    parser.add_argument('-d', '--datasets', nargs='+', required=True)
    parser.add_argument('-n', '--names', nargs='+', required=True)

    arguments = parser.parse_args()
    action = arguments.action
    datasets = arguments.datasets
    names = arguments.names
    #print(datasets)

    if action == 'merge':
        merge(datasets, names)
    else:
        split(datasets, names)


