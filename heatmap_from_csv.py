import pandas as pd
import matplotlib.pyplot as plt


def get_user_columns(df):
    print("\nAvailable columns:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    lat_col = input("Enter the column name for Latitude: ")
    lon_col = input("Enter the column name for Longitude: ")
    port1_col = input("Enter the column name for Pressure Port 1: ")
    port2_col = input("Enter the column name for Pressure Port 2: ")
    return lat_col, lon_col, port1_col, port2_col

def main():
    # --- User Input for CSV ---
    csv_file = input("Enter the path to your CSV file: ")
    df = pd.read_csv(csv_file)

    # --- User Input for Columns ---
    lat_col, lon_col, port1_col, port2_col = get_user_columns(df)

    # --- Data Cleaning ---
    for col in [lat_col, lon_col, port1_col, port2_col]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=[lat_col, lon_col, port1_col, port2_col])

    # --- Normalize GPS ---
    df['x'] = (df[lon_col] - df[lon_col].mean()) * 1e5
    df['y'] = (df[lat_col] - df[lat_col].mean()) * 1e5

    # --- Select Lap 5 (last 1/5th as example) ---
    lap5 = df.iloc[len(df) * 4 // 5:].copy()

    # --- Plotting ---
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))
    vmin, vmax = -80, 20

    sc1 = axs[0].scatter(lap5['x'], lap5['y'], c=lap5[port1_col], cmap='coolwarm', s=8, vmin=vmin, vmax=vmax)
    axs[0].set_title(f"{port1_col} – Centered Pressure (Lap 5)")
    axs[0].set_xlabel("Relative Longitude")
    axs[0].set_ylabel("Relative Latitude")
    axs[0].axis('equal')
    axs[0].grid(True)
    fig.colorbar(sc1, ax=axs[0], label='Δ Pressure (mbar)')

    sc2 = axs[1].scatter(lap5['x'], lap5['y'], c=lap5[port2_col], cmap='coolwarm', s=8, vmin=vmin, vmax=vmax)
    axs[1].set_title(f"{port2_col} – Centered Pressure (Lap 5)")
    axs[1].set_xlabel("Relative Longitude")
    axs[1].set_ylabel("Relative Latitude")
    axs[1].axis('equal')
    axs[1].grid(True)
    fig.colorbar(sc2, ax=axs[1], label='Δ Pressure (mbar)')

    plt.suptitle(f"{csv_file} – {port1_col} vs {port2_col} Heatmaps (Lap 5, Clipped: -80 to +20 mbar)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

if __name__ == "__main__":
    main() 