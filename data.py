import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_name1 = "rf2"
file_name2 = "rf3"


def clean_csv(input_file, output_file, skiprows=11):
    df1 = pd.read_csv(input_file, skiprows=skiprows)
    df1.to_csv(output_file, index=False)
    print(f"Cleaned file saved to: {output_file}")


def merge_csv(input_file1, input_file2, output_file="merged.csv"):
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    merged_df = pd.merge(
        df1, df2, on="PacketCounter", how="inner", suffixes=("_file1", "_file2")
    )
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to: {output_file}")
    return merged_df


def normalize_angle_continuous(diff):
    normalized_diff = np.array(diff, dtype=float)
    unwrapped_diff = np.unwrap(np.deg2rad(normalized_diff)) * 180 / np.pi
    return unwrapped_diff


def plot_euler_differences(merged_df):
    merged_df["Euler_X_diff_raw"] = (
        merged_df["Euler_X_file1"] - merged_df["Euler_X_file2"]
    )
    merged_df["Euler_Y_diff_raw"] = (
        merged_df["Euler_Y_file1"] - merged_df["Euler_Y_file2"]
    )
    merged_df["Euler_Z_diff_raw"] = (
        merged_df["Euler_Z_file1"] - merged_df["Euler_Z_file2"]
    )
    merged_df["Euler_X_diff"] = normalize_angle_continuous(
        merged_df["Euler_X_diff_raw"]
    )
    merged_df["Euler_Y_diff"] = normalize_angle_continuous(
        merged_df["Euler_Y_diff_raw"]
    )
    merged_df["Euler_Z_diff"] = normalize_angle_continuous(
        merged_df["Euler_Z_diff_raw"]
    )

    plt.figure(figsize=(12, 6))
    plt.plot(
        merged_df["PacketCounter"],
        merged_df["Euler_X_diff"],
        label="Euler_X Difference",
        color="r",
    )
    plt.plot(
        merged_df["PacketCounter"],
        merged_df["Euler_Y_diff"],
        label="Euler_Y Difference",
        color="g",
    )
    plt.plot(
        merged_df["PacketCounter"],
        merged_df["Euler_Z_diff"],
        label="Euler_Z Difference",
        color="b",
    )
    plt.xlabel("PacketCounter")
    plt.ylabel("Normalized Difference (Degrees)")
    plt.title("Normalized Euler Angle Differences (X, Y, Z)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


clean_csv(f"Data/{file_name1}.csv", f"Data/temp_{file_name1}_clean.csv")
clean_csv(f"Data/{file_name2}.csv", f"Data/temp_{file_name2}_clean.csv")

merged_data = merge_csv(
    f"Data/temp_{file_name1}_clean.csv",
    f"Data/temp_{file_name2}_clean.csv",
    "Data/temp_merged.csv",
)

plot_euler_differences(merged_data)
