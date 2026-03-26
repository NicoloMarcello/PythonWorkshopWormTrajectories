import h5py
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import numpy as np

# File paths for the 3 conditions
filepaths = {
    "mock conditioned": "Chemotaxis-Data-and-Analysis/Mock_worms/chemotaxis_mock_210825_3_20250722_161220/metadata_featuresN_oneworm.hdf5",
    "aversively conditioned": "Chemotaxis-Data-and-Analysis/Aversive_worms/chemotaxis_avsv_24_1_23_01_20240124_140022/metadata_featuresN_oneworm.hdf5",
    "sexually conditioned": "Chemotaxis-Data-and-Analysis/sexually_conditioned_worms/chemotaxis_sexc_24_1_26_09_20240126_143858/metadata_featuresN_oneworm.hdf5",
}

# Check if files exist
for condition, filepath in filepaths.items():
    if not os.path.exists(filepath):
        print(f"\nFile not found: {filepath}!")
        print("Please ensure the Chemotaxis-Data-and-Analysis repository is cloned in this folder.")
        quit()

# Scale factor to convert to micrometers
scale_factor = 13

# Colors for each condition
colors = {
    "mock conditioned": "red",
    "aversively conditioned": "blue",
    "sexually conditioned": "green",
}

# Create figure and axis
plt.figure(figsize=(6, 6))

# Load and plot each trajectory
for condition, filepath in filepaths.items():
    print(f"Loading {condition} dataset...")
    
    with h5py.File(filepath, "r") as f:
        traj_data = pd.DataFrame(f["trajectories_data"][:])
    
    # Get x and y coordinates
    x_coords = np.array(traj_data["coord_x"]) * scale_factor
    y_coords = np.array(traj_data["coord_y"]) * scale_factor
    
    # Normalize so first position is at (0, 0)
    x_normalized = x_coords - x_coords[0]
    y_normalized = y_coords - y_coords[0]
    
    # Plot the trajectory
    plt.scatter(x_normalized,y_normalized,s=2,c=colors[condition],label=condition,alpha=0.6,)
    
    print(f"  Plotted {len(x_normalized)} points")

# Labels and formatting
plt.xlabel("X Position (micrometers)", fontsize=12)
plt.ylabel("Y Position (micrometers)", fontsize=12)
plt.title("Worm Chemotaxis Trajectories", fontsize=14, fontweight="bold")
plt.legend(fontsize=11, loc="best")
plt.grid(True, alpha=0.3)
plt.axis("equal")

# Add odor gradient colorbar
sm = cm.ScalarMappable(cmap=cm.Blues, norm=Normalize(vmin=0, vmax=1))
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca(), orientation='horizontal', pad=0.15, shrink=0.8)
cbar.set_label('Odor Gradient', fontsize=11)
cbar.ax.set_xticklabels(['Weak', '', '', '', 'Strong'])

# Save and show
output_path = "images/worm_trajectories_comparison.png"
os.makedirs("images", exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"\nPlot saved to: {output_path}")

plt.show()
