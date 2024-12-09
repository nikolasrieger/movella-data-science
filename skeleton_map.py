import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def normalize_angle_continuous(diff):
    return np.unwrap(np.deg2rad(diff)) * 180 / np.pi


def calculate_euler_differences(merged_df):
    merged_df["Euler_X_diff"] = normalize_angle_continuous(merged_df["Euler_X_file1"] - merged_df["Euler_X_file2"])
    merged_df["Euler_Y_diff"] = normalize_angle_continuous(merged_df["Euler_Y_file1"] - merged_df["Euler_Y_file2"])
    merged_df["Euler_Z_diff"] = normalize_angle_continuous(merged_df["Euler_Z_file1"] - merged_df["Euler_Z_file2"])


def rotate_point(length, angle_x, angle_y, angle_z):
    angle_x_rad, angle_y_rad, angle_z_rad = np.radians([angle_x, angle_y, angle_z])
    
    Rx = np.array([[1, 0, 0], [0, np.cos(angle_x_rad), -np.sin(angle_x_rad)], [0, np.sin(angle_x_rad), np.cos(angle_x_rad)]])
    Ry = np.array([[np.cos(angle_y_rad), 0, np.sin(angle_y_rad)], [0, 1, 0], [-np.sin(angle_y_rad), 0, np.cos(angle_y_rad)]])
    Rz = np.array([[np.cos(angle_z_rad), -np.sin(angle_z_rad), 0], [np.sin(angle_z_rad), np.cos(angle_z_rad), 0], [0, 0, 1]])

    rotation_matrix = np.dot(Rz, np.dot(Ry, Rx))
    point = np.array([length, 0, 0])
    return np.dot(rotation_matrix, point)


def update(frame):
    offset_x = merged_data['Euler_X_diff'].iloc[0]
    offset_y = merged_data['Euler_Y_diff'].iloc[0]
    offset_z = merged_data['Euler_Z_diff'].iloc[0]
    angle_upper_arm_x = merged_data['Euler_X_diff'].iloc[frame] - offset_x
    angle_upper_arm_y = merged_data['Euler_Y_diff'].iloc[frame] - offset_y
    angle_upper_arm_z = merged_data['Euler_Z_diff'].iloc[frame] - offset_z

    elbow_new = rotate_point(upper_arm_length, angle_upper_arm_x, angle_upper_arm_y, 0)
    wrist_new = rotate_point(forearm_length, angle_upper_arm_x, angle_upper_arm_y, angle_upper_arm_z) + elbow_new

    upper_arm_line.set_data([shoulder[0], elbow_new[0]], [shoulder[1], elbow_new[1]])
    upper_arm_line.set_3d_properties([shoulder[2], elbow_new[2]], 'z')
    forearm_line.set_data([elbow_new[0], wrist_new[0]], [elbow_new[1], wrist_new[1]])
    forearm_line.set_3d_properties([elbow_new[2], wrist_new[2]], 'z')
    elbow_dot.set_data([elbow_new[0]], [elbow_new[1]])
    elbow_dot.set_3d_properties([elbow_new[2]], 'z')
    wrist_dot.set_data([wrist_new[0]], [wrist_new[1]])
    wrist_dot.set_3d_properties([wrist_new[2]], 'z')
    return upper_arm_line, forearm_line, elbow_dot, wrist_dot

upper_arm_length = 30
forearm_length = 25
shoulder = np.array([0, 0, 0])

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)
ax.set_zlim(-50, 50)
upper_arm_line, = ax.plot([], [], [], label="Upper Arm", color="r", marker="o")
forearm_line, = ax.plot([], [], [], label="Forearm", color="g", marker="o")
elbow_dot, = ax.plot([], [], [], 'ro')
wrist_dot, = ax.plot([], [], [], 'go')

merged_data = pd.read_csv("Data/temp_merged.csv") 
calculate_euler_differences(merged_data)

ani = animation.FuncAnimation(fig, update, frames=len(merged_data), interval=100, blit=True, repeat=True)
plt.legend()
plt.tight_layout()
plt.show()
