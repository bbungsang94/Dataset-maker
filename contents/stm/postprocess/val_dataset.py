import os
from tqdm import tqdm
import numpy as np
import pandas as pd
import torch

from contents.stm.preprocess.convention import get_interactions


def to_csv(root=r"D:\Creadto\Heritage\Dataset\SMPL-Measure\parameter"):
    interactions = get_interactions()
    kor_columns = []
    eng_columns = []
    positions = []
    for interaction in interactions:
        kor, eng, _, _, pose = interaction
        kor_columns.append(kor)
        eng_columns.append(eng)
        positions.append(pose)

    files = os.listdir(root)
    table = np.zeros((len(files), len(interactions)))
    for i, file in tqdm(enumerate(files)):
        full_path = os.path.join(root, file)
        dictionary = torch.load(full_path)
        table[i] = dictionary['output']['measure']
    eng_table = pd.DataFrame(eng_columns)
    pos_table = pd.DataFrame(positions)
    df = pd.DataFrame(table)
    csv = pd.concat([eng_table.T, pos_table.T, df], ignore_index=True)
    csv.columns = kor_columns
    csv.to_csv(os.path.join(r"D:\Creadto\Heritage\Dataset\SMPL-Measure\csv", "temp.csv"),
               index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    to_csv()