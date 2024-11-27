app_css = """
<style>
/* Global Background and Header Styling */
.block-container {
    padding: 0rem;
    background-color: #408a93; /* Dark green background */

}
[data-testid="stHeader"] {
    padding-top: 0.0rem;
    padding-bottom: 0.0rem;
    height: 0rem;
    background-color: #408a93; /* Light gray background for header */
}
.main-title {
    color: #1F618D;
    font-weight: bold;
    text-align: center;
    font-size: 2.3rem;
}


/* Sidebar Styling */
.sidebar .sidebar-content {
    background-color: #AED6F1;
    padding: 2rem;
    border-radius: 10px;
}
.sidebar .sidebar-content h1 {
    color: #1F618D;
}
[data-testid="stSidebar"] {
    transition: margin-left 0.3s ease-in-out; /* Smooth slide animation */
    z-index: 1 !important; /* Ensure sidebar stays on top */
}
.sidebar-collapsed [data-testid="stSidebar"] {
    margin-left: -400px; /* Slide sidebar out of view */
}

/* Button Styling */
.stButton > button {
    color: #FFFFFF;
    background-color: #1F618D;
    border: none;
}

/* Alert and Success Message Styling */
.stAlert, .stSuccess, .stError {
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-weight: bold;
}

/* DataFrame and Map Styling */
.stDataFrame, .stMap {
    border-radius: 10px;
}
</style>
"""
