import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import os

# ------------------------------
# Page Configuration & Styling
# ------------------------------
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Load custom CSS from file
css_file_path = "assets/styles.css"
if os.path.exists(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("Custom CSS file not found. Using default styles.")

# ------------------------------
# Header Section
# ------------------------------
st.markdown(
    """
    <div class="header" style="display: flex; justify-content: space-between; font-family:Roboto; align-items: center; background-color: #408a93; padding: 10px;">
        <!-- Left Section -->
        <div style="font-size: 1.6rem; font-weight: bold; color: white; margin-left: 10px;">
            Coastal and Marine Monitoring Projects
        </div>
        <!-- Right Section -->
        <div style="font-size: 1rem; font-weight: bold; margin-right: 20px;">
            <a href="https://data.ocean.gov.za/" target="_blank" style="color: white; text-decoration: none;">
                MIMS
            </a>
        </div>
    </div>
    <div style="text-align: left; font-size: 0.9rem; margin-left: 10px; font-family:Roboto; font-weight: bold; color: white; background-color: #408a93; padding: 5px;">
        Department of Forestry, Fisheries, and the Environment
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Function to Load & Clean Data
# ------------------------------
@st.cache_data
def load_data(file_path):
    """Loads and cleans the dataset safely."""
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        required_columns = {"Lat", "Lon", "Project_Name"}
        missing_columns = required_columns - set(df.columns)
        
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return pd.DataFrame()

        df.rename(columns={"Lat": "latitude", "Lon": "longitude"}, inplace=True)
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please check the backend data path.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Ensure it's properly formatted.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return pd.DataFrame()

# ------------------------------
# Load Data from Backend
# ------------------------------
default_data_path = "data/dffe_sampling_Stations.csv"

with st.spinner("Loading data..."):
    data = load_data(default_data_path)

# Get unique project names
predefined_projects = data["Project_Name"].dropna().unique().tolist() if not data.empty else []

# ------------------------------
# Assign Colors to Projects
# ------------------------------

# Default color palette (expand as needed)
default_colors = ["blue", "red", "green", "black", "purple", "cyan", "orange", "pink", "yellow", "brown"]

# Assign colors dynamically to projects
project_color_map = {}
used_colors = set()

for i, project in enumerate(predefined_projects):
    if project not in project_color_map:
        color = default_colors[i % len(default_colors)]  # Assign next color in list
        project_color_map[project] = color
        used_colors.add(color)

# ------------------------------
# Sidebar - Project Selection
# ------------------------------
if "projects_initialized" not in st.session_state:
    for project in predefined_projects:
        st.session_state[f"project-{project}"] = True  # Select all projects by default
    st.session_state["projects_initialized"] = True

with st.sidebar:
    st.markdown("### Select projects:")
    
    # Buttons for Select All / Unselect All
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Select All"):
            for project in predefined_projects:
                st.session_state[f"project-{project}"] = True
    with col2:
        if st.button("Unselect All"):
            for project in predefined_projects:
                st.session_state[f"project-{project}"] = False

    # Checkboxes for each project
    selected_projects = [
        project for project in predefined_projects
        if st.checkbox(project, value=st.session_state[f"project-{project}"], key=f"project-{project}")
    ]
    
    st.markdown("### Legend")
    # Toggle for showing legend
    show_legend = st.checkbox("Show Legend", value=True)

    
# Filter data based on selected projects
filtered_data = data[data["Project_Name"].isin(selected_projects)] if selected_projects else pd.DataFrame()

# ------------------------------
# Function to Generate Interactive Map
# ------------------------------
def generate_map(filtered_data, show_legend):
    """Generates a Leafmap interactive map with project layers."""
    m = leafmap.Map(
        center=[-35.0, 21.0],
        zoom=6,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        height=900,
    )

    if not filtered_data.empty:
        legend_dict = {}  # Store legend items

        for project, project_data in filtered_data.groupby("Project_Name"):
            color = project_color_map.get(project, "gray")  # Use assigned color or default to gray
            
            m.add_circle_markers_from_xy(
                project_data,
                x="longitude",
                y="latitude",
                radius=4,
                stroke=True,
                color=color,
                fill_color=color,
                fill_opacity=0.7,
                layer_name=f"{project} Layer",
            )

            legend_dict[project] = color  # Add to legend

        # Conditionally add a legend
        if show_legend and legend_dict:
            m.add_legend(title="Projects", legend_dict=legend_dict)

        m.add_layer_control()  # Enable layer toggling
        m.add_basemap()
    else:
        m.add_basemap("OpenStreetMap")
    return m

# ------------------------------
# Render the Map in Streamlit
# ------------------------------
leafmap_component = generate_map(filtered_data, show_legend)
leafmap_component.to_streamlit(height=900, use_container_width=True)
