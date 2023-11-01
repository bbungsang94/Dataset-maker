import os
import pandas as pd

def make_dataset(root=r"D:\Creadto\Heritage\Dataset\SMPL2Measure\raw", filename="dataset.csv"):
    full_path = os.path.join(root, filename)
    file = pd.read_csv(full_path, index_col="Index")
    dataset = file.dropna(subset=['성별'])
    dataset = dataset.drop(['BANNED'], axis=1)
    dataset.to_csv(os.path.join(root, "real_dataset.csv"))
    pass

if __name__ == "__main__":
    make_dataset()