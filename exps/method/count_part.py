#!/usr/bin/env python3
import argparse
import warnings

import matplotlib.pyplot as plt

plt.switch_backend("agg")
warnings.filterwarnings("ignore")

from collections import Counter

from datasets.partnet_debug import PartNetPartDataset

parser = argparse.ArgumentParser(description="3D part assembly.")

# * Dataset.
parser.add_argument("--data_dir", type=str, default="../../prepare_data", help="data directory")
parser.add_argument(
    "--category",
    type=str,
    default="Lamp",
    choices=["Chair", "Table", "Lamp"],
    help="model def file",
)
parser.add_argument(
    "--train_data_fn",
    type=str,
    default="Lamp.train.npy",
    choices=["Chair.train.npy", "Table.train.npy", "Lamp.train.npy"],
    help="training data file that index all data tuples",
)
parser.add_argument(
    "--val_data_fn",
    type=str,
    default="Lamp.val.npy",
    choices=["Chair.val.npy", "Table.val.npy", "Lamp.val.npy"],
    help="validation data file that index all data tuples",
)
parser.add_argument("--level", type=str, default="3", help="level of dataset")


def main():
    # =================== Parameters Setting ===================
    args = parser.parse_args()

    PartNetPartDataset(
        args.data_dir,
        args.train_data_fn,
        args.category,
        level=args.level,
        max_num_part=20,
    )

    val_dataset = PartNetPartDataset(
        args.data_dir,
        args.val_data_fn,
        args.category,
        level=args.level,
        max_num_part=20,
    )

    # count duplicate part / class.
    num_ins = 0.0
    num_part = 0.0
    num_cate = 0.0
    for idx, data in enumerate(val_dataset):
        print(f"Processing: {idx}/{len(val_dataset)}")
        if data is None:
            continue
        num_ins += 1

        data[0]
        part_id = data[1].squeeze().numpy().tolist()
        num_part_per_ins = Counter(part_id).most_common()
        for key, value in num_part_per_ins:
            if int(key) == 0:
                continue
            if int(value) == 1:
                break
            if int(value) > 1:
                num_part += value
                num_cate += 1

    print(f"Num_part: {num_part} | Num_cate: {num_cate} | Ave_part_per_cate: {num_part / num_cate}")


if __name__ == "__main__":
    main()
