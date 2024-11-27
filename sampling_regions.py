import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
from css import app_css  # Import CSS as a string

# Set the page configuration to wide mode
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Apply CSS styling
st.markdown(app_css, unsafe_allow_html=True)

# Header Section
st.markdown(
    """
    <div class="header" style="display: flex; justify-content: space-between; font-family:Roboto; align-items: center; background-color: #408a93; padding: 0px;">
        <!-- Left Section -->
        <div style="font-size: 1.6rem; font-weight: bold; color: white; margin-left: 10px;">
            Marine Monitoring Projects
        </div>
        <!-- Right Section -->
        <div style="font-size: 0.2rem; font-weight: bold; font-family:Roboto; margin-right: 200px;margin-top: 5px">
            <a href="https://data.ocean.gov.za/" target="_blank" style="color: white; text-decoration: none;">
                MIMS
            </a>
        </div>
    </div>
    <div style="text-align: left; font-size: 0.8rem; margin-left: 10px; font-family:Roboto; font-weight: bold; color: white; background-color: #408a93; padding: 0px;">
        Department of Forestry, Fisheries, and the Environment
    </div>
    """,
    unsafe_allow_html=True,
)

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Header Styling */
    .header {
        background-color: #006400;
        padding: 1px;
        text-align: center;
        color: white;
        font-size: 1rem;
        font-family: Roboto;
    }
    .header a {
        color: #FFD700;
        margin-left: 20px;
        text-decoration: none;
        font-size: 1.2rem;
    }
    .header a:hover {
        text-decoration: underline;
    }
    .st-emotion-cache-12skds7 {
        height: 0rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        transition: margin-left 0.3s ease-in-out; /* Smooth slide animation */
        z-index: 1 !important;
    }
    .sidebar-collapsed [data-testid="stSidebar"] {
        margin-left: -400px; /* Slide sidebar out of view */
    }
    
    .st-emotion-cache-19u4bdk {
        position: fixed;
        top: 20rem;
        left: 0.2rem;
        z-index: 999990;
        display: flex;
        justify-content: center;
        align-items: start;
        transition: left 300ms;
        background-color: #408a93;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Function to load and clean the dataset
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        df.rename(columns={"Lat": "latitude", "Lon": "longitude"}, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        return pd.DataFrame()


# Load the dataset
data = load_data("data/dffe_sampling_Stations.csv")

# Dynamically generate the list of unique projects
predefined_projects = data["Project_Name"].dropna().unique().tolist()

# Initialize session state for project checkboxes
if "projects_initialized" not in st.session_state:
    for project in predefined_projects:
        st.session_state[f"project-{project}"] = True  # Select all projects by default
    st.session_state["projects_initialized"] = True

# Sidebar with layer controls for projects
with st.sidebar:
    st.markdown("### Select projects:")

    # Side-by-side buttons for "Select All" and "Unselect All"
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Select All"):
            for project in predefined_projects:
                st.session_state[f"project-{project}"] = True
            # st.experimental_rerun()
    with col2:
        if st.button("Unselect All"):
            for project in predefined_projects:
                st.session_state[f"project-{project}"] = False
            # st.experimental_rerun()

    # Display checkboxes for each project
    selected_projects = []
    for project in predefined_projects:
        if st.checkbox(
            project,
            value=st.session_state[f"project-{project}"],
            key=f"project-{project}",
        ):
            selected_projects.append(project)

# Filter the dataframe based on the selected projects
if selected_projects:
    filtered_data = data[data["Project_Name"].isin(selected_projects)]
else:
    filtered_data = (
        pd.DataFrame()
    )  # Return an empty dataframe if no project is selected


# Function to generate map with layers
def generate_map(filtered_data):
    m = leafmap.Map(
        center=[-35.0, 21.0],
        zoom=6,
        draw_control=False,
        measure_control=False,
        fullscreen_control=False,
        attribution_control=True,
        height="450px",
        width="800px",
    )

    if not filtered_data.empty:
        # Define project colors
        colors = ["blue", "red", "green", "orange", "purple", "cyan"]
        projects = filtered_data["Project_Name"].unique()
        project_color_map = {
            project: colors[i % len(colors)] for i, project in enumerate(projects)
        }

        # Add project layers
        for project in projects:
            project_data = filtered_data[filtered_data["Project_Name"] == project]
            color = project_color_map[project]
            m.add_circle_markers_from_xy(
                project_data,
                x="longitude",
                y="latitude",
                radius=3,
                stroke=True,
                color=color,
                fill_color=color,
                fill_opacity=0.7,
                layer_name=f"{project} Layer",
            )

        # Add a custom legend
        legend_dict = {project: project_color_map[project] for project in projects}
        m.add_legend(title="Projects", legend_dict=legend_dict)

        m.add_layer_control()  # Enable toggling of layers
        m.add_basemap()
    else:
        # Add a placeholder map with no data
        m.add_basemap("OpenStreetMap")

    return m


# Generate the map with the filtered data
leafmap_component = generate_map(filtered_data)
leafmap_component.to_streamlit(height=700, use_container_width=True)
