
import streamlit as st
import pandas as pd

# Load the Excel file
excel_file = "Blowdown Gas Volumes - Copy.xlsx"

# Read the Examples sheet with correct header
examples_df = pd.read_excel(excel_file, sheet_name="Examples", header=1, engine="openpyxl")

# Drop rows with NaN in critical columns
examples_df = examples_df.dropna(subset=["Volume Type", "Valve Size [in]", "Duration [s]", "Release [MCF]"])

# Convert relevant columns to numeric
examples_df["Valve Size [in]"] = pd.to_numeric(examples_df["Valve Size [in]"], errors="coerce")
examples_df["Duration [s]"] = pd.to_numeric(examples_df["Duration [s]"], errors="coerce")
examples_df["Release [MCF]"] = pd.to_numeric(examples_df["Release [MCF]"], errors="coerce")

# Streamlit UI
st.title("Blowdown Valve Size Recommendation Dashboard")

# Volume type selector
volume_types = examples_df["Volume Type"].dropna().unique()
selected_volume_type = st.selectbox("Select Volume Type", volume_types)

# Filter data by selected volume type
filtered_df = examples_df[examples_df["Volume Type"] == selected_volume_type]

# Slider for target release volume
min_release = float(filtered_df["Release [MCF]"].min())
max_release = float(filtered_df["Release [MCF]"].max())

# Ensure min and max are not equal
if min_release == max_release:
    st.warning("Only one release volume available for this volume type.")
    target_release = min_release
else:
    target_release = st.slider("Select Target Release Volume (MCF)", min_value=min_release, max_value=max_release, value=min_release)

# Find the smallest valve size that meets or exceeds the target release
recommendation = filtered_df[filtered_df["Release [MCF]"] >= target_release].sort_values("Valve Size [in]").head(1)

if not recommendation.empty:
    valve_size = recommendation["Valve Size [in]"].values[0]
    duration = recommendation["Duration [s]"].values[0]
    actual_release = recommendation["Release [MCF]"].values[0]

    st.success(f"✅ Recommended Valve Size: **{valve_size} in**")
    st.info(f"⏱️ Expected Duration: **{duration} seconds**")
    st.info(f"📦 Actual Release Volume: **{actual_release} MCF**")
else:
    st.warning("No suitable valve size found for the selected volume type and target release.")

# Show filtered data table
with st.expander("Show Data Table"):
    st.dataframe(filtered_df[["Valve Size [in]", "Duration [s]", "Release [MCF]"]].sort_values("Valve Size [in]"))
