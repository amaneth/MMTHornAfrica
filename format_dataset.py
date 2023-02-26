import os
import jsonlines
import pandas as pd
import argparse

def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def export_csv_files(output_dir, df, direction='orm_eng_law'):
    
    create_dir(output_dir)
    
    filename = output_dir + '/' + direction + '.csv'
    df.to_csv(filename, index=False)


def export_json_files(output_dir, source_path, direction='orm_eng_law'):
    df = pd.read_csv(source_path)
    print(df.columns)
    to_be_saved = []
    src_data = df['source_lang'].values
    tgt_data = df['target_lang'].values
    src_lang, tgt_lang = direction.split('_')
    N_sent = df.shape[0]
    for s in range(N_sent):
        text_string = {"translation": {src_lang:src_data[s], tgt_lang:tgt_data[s]}}
        to_be_saved.append(text_string)

    create_dir(output_dir)
    filename = output_dir + '/' + direction + '.json'  

    with jsonlines.open(filename, 'w') as writer:
        writer.write_all(to_be_saved)
        


def parallel_translation_data(source_path, target_path, input_path):

    df_source = pd.read_csv(source_path, sep=r'\n', header=None, engine='python')
    df_target = pd.read_csv(target_path, sep=r'\n', header=None, engine = 'python')

    print(len(df_source),len(df_target))

    src_data, tg_data = df_source.iloc[:, 0].values, df_target.iloc[:, 0].values

    df_data = pd.DataFrame(src_data, columns=['source_lang'])
    df_data['target_lang'] = tg_data

    return df_data





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input',default='.')
    #parser.add_argument('--output', default='../csvfiles')
    parser.add_argument('--source', required = True)
    parser.add_argument('--target', required = False)
    parser.add_argument('--to', default = 'csv')
    parser.add_argument('--direction', required = True)

    arguments = parser.parse_args()
    input_dir = arguments.input
    source_path = arguments.source
    target_path = arguments.target
    filetype = arguments.to
    direction = arguments.direction

    
    if filetype == 'json':
        export_json_files('../jsonfiles',source_path, direction=direction)
    else:
        parallel_df = parallel_translation_data(source_path, target_path, input_dir)  # replace direction with whatever translation direction
        export_csv_files('../csvfiles', parallel_df, direction=direction)

