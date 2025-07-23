import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Heatmap Generator from CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your data:", df.head())

    columns = df.columns.tolist()
    lat_col = st.selectbox("Select Latitude column", columns)
    lon_col = st.selectbox("Select Longitude column", columns)
    port_col = st.selectbox("Select Pressure Port column", columns)
    # Lap selection
    lap_col = st.selectbox("Select Lap column", columns)
    unique_laps = df[lap_col].dropna().unique()
    lap_options = ['All Laps'] + sorted([str(l) for l in unique_laps])
    selected_lap = st.selectbox("Select Lap to plot", lap_options)

    # Inputs for custom title and color scale
    custom_title = st.text_input("Enter a custom title for the graph", value=f"{port_col} Heatmap")
    vmin = st.number_input("Color scale minimum (vmin)", value=-80)
    vmax = st.number_input("Color scale maximum (vmax)", value=20)

    if st.button("Generate Heatmap"):
        # Data cleaning
        for col in [lat_col, lon_col, port_col, lap_col]:
            df[col] = pd.to_numeric(df[col], errors='coerce') if col != lap_col else df[col]
        df = df.dropna(subset=[lat_col, lon_col, port_col, lap_col])

        # Lap filtering
        if selected_lap != 'All Laps':
            try:
                # Try to convert selected_lap to the same type as in the DataFrame
                lap_val = type(df[lap_col].iloc[0])(selected_lap)
            except Exception:
                lap_val = selected_lap
            df = df[df[lap_col] == lap_val]

        # Normalize GPS
        df['x'] = (df[lon_col] - df[lon_col].mean()) * 1e5
        df['y'] = (df[lat_col] - df[lat_col].mean()) * 1e5

        # Plotting
        fig, ax = plt.subplots(figsize=(9, 8))
        sc = ax.scatter(df['x'], df['y'], c=df[port_col], cmap='coolwarm', s=8, vmin=vmin, vmax=vmax)
        ax.set_title(f"{port_col} – Centered Pressure" + (f" (Lap {selected_lap})" if selected_lap != 'All Laps' else " (All Laps)"))
        ax.set_xlabel("Relative Longitude")
        ax.set_ylabel("Relative Latitude")
        ax.axis('equal')
        ax.grid(True)
        fig.colorbar(sc, ax=ax, label='Δ Pressure (mbar)')

        plt.suptitle(custom_title, fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        st.pyplot(fig) 