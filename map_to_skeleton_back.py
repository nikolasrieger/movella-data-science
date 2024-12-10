import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# File names
file_names = [
    "unten",
    "mitte",
    "oben",
]

# Cleaning function
def clean_csv(input_file, output_file, skiprows=11):
    df = pd.read_csv(input_file, skiprows=skiprows)
    df.to_csv(output_file, index=False)
    print(f"Cleaned file saved to: {output_file}")


# Merge function
def merge_csv(file_paths, output_file="merged.csv"):
    dfs = [pd.read_csv(path) for path in file_paths]
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(
            merged_df, df, on="PacketCounter", how="inner", suffixes=(None, f"_file{dfs.index(df) + 1}")
        )
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to: {output_file}")
    return merged_df


# Normalize angle
def normalize_angle_continuous(diff):
    return np.unwrap(np.deg2rad(diff)) * 180 / np.pi


# Calculate Euler differences
def calculate_euler_differences(merged_df, section):
    merged_df[f"Euler_X_diff_{section}"] = normalize_angle_continuous(
        merged_df[f"Euler_X_file{section}"] - merged_df[f"Euler_X_file{section + 1}"]
    )
    merged_df[f"Euler_Y_diff_{section}"] = normalize_angle_continuous(
        merged_df[f"Euler_Y_file{section}"] - merged_df[f"Euler_Y_file{section + 1}"]
    )
    merged_df[f"Euler_Z_diff_{section}"] = normalize_angle_continuous(
        merged_df[f"Euler_Z_file{section}"] - merged_df[f"Euler_Z_file{section + 1}"]
    )


# Plotting differences
def plot_euler_differences(merged_df):
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    sections = ["Lower", "Middle", "Upper"]
    colors = ["r", "g", "b"]

    for i, section in enumerate(sections):
        axes[i].plot(
            merged_df["PacketCounter"],
            merged_df[f"Euler_X_diff_{i+1}"],
            label=f"{section} X Difference",
            color=colors[0],
        )
        axes[i].plot(
            merged_df["PacketCounter"],
            merged_df[f"Euler_Y_diff_{i+1}"],
            label=f"{section} Y Difference",
            color=colors[1],
        )
        axes[i].plot(
            merged_df["PacketCounter"],
            merged_df[f"Euler_Z_diff_{i+1}"],
            label=f"{section} Z Difference",
            color=colors[2],
        )
        axes[i].set_title(f"{section} Back Normalized Differences")
        axes[i].set_xlabel("PacketCounter")
        axes[i].set_ylabel("Normalized Difference (Degrees)")
        axes[i].legend()
        axes[i].grid()

    plt.tight_layout()
    plt.show()


# Clean files
cleaned_files = []
for file_name in file_names:
    cleaned_file = f"Data/temp_{file_name}_clean.csv"
    clean_csv(f"Data/{file_name}.csv", cleaned_file)
    cleaned_files.append(cleaned_file)

# Merge data
merged_data = merge_csv(cleaned_files, "Data/temp_merged.csv")

# Calculate differences
for section in range(1, 4):
    calculate_euler_differences(merged_data, section)

# Plot
plot_euler_differences(merged_data)

# Animation Functionality
def rotate_point(length, angle_x, angle_y, angle_z):
    angle_x_rad, angle_y_rad, angle_z_rad = np.radians([angle_x, angle_y, angle_z])
    
    Rx = np.array([[1, 0, 0], [0, np.cos(angle_x_rad), -np.sin(angle_x_rad)], [0, np.sin(angle_x_rad), np.cos(angle_x_rad)]])
    Ry = np.array([[np.cos(angle_y_rad), 0, np.sin(angle_y_rad)], [0, 1, 0], [-np.sin(angle_y_rad), 0, np.cos(angle_y_rad)]])
    Rz = np.array([[np.cos(angle_z_rad), -np.sin(angle_z_rad), 0], [np.sin(angle_z_rad), np.cos(angle_z_rad), 0], [0, 0, 1]])

    rotation_matrix = np.dot(Rz, np.dot(Ry, Rx))
    point = np.array([length, 0, 0])
    return np.dot(rotation_matrix, point)


def update(frame):
    offsets = [
        merged_data[f"Euler_X_diff_{i+1}"].iloc[0]
        for i in range(3)
    ]
    elbow_new = rotate_point(30, *offsets)
    wrist_new = rotate_point(25, *offsets)

    upper_arm_line.set_data([shoulder[0], elbow_new[0]], [shoulder[1], elbow_new[1]])
    upper_arm_line.set_3d_properties([shoulder[2], elbow_new[2]], 'z')
    forearm_line.set_data([elbow_new[0], wrist_new[0]], [elbow_new[1], wrist_new[1]])
    forearm_line.set_3d_properties([elbow_new[2], wrist_new[2]], 'z')
    return upper_arm_line, forearm_line


# Animation Setup
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_zlim(-50, 50)
upper_arm_line, = ax.plot([], [], [], label="Upper Arm", color="r", marker="o")
forearm_line, = ax.plot([], [], [], label="Forearm", color="g", marker="o")

shoulder = np.array([0, 0, 0])

ani = animation.FuncAnimation(fig, update, frames=len(merged_data), interval=100, blit=True, repeat=True)
plt.legend()
plt.tight_layout()
plt.show()
