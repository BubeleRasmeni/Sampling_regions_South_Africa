Here’s the full **README.md** file, ready for you to copy and paste:  

---

### **README.md**
```md
# Sampling Regions South Africa 🌍

This **Streamlit dashboard** provides an **interactive map** visualizing **data collection projects** across South Africa, managed by the **Department of Forestry, Fisheries and the Environment (DFFE)**.  

## 🚀 Features
- 🗺 **Interactive Map** – Click on sampling stations to view details.
- 📍 **DFFE Data Collection Projects** – Visual representation of sampling efforts across South Africa.
- 📂 **Geospatial Data** – Load and display station locations dynamically.
- 🐳 **Marine & Environmental Data Points** – View metadata about different sampling stations.

---

## 📦 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/BubeleRasmeni/Sampling_regions_South_Africa.git
cd Sampling_regions_South_Africa
```

### **2️⃣ Install Dependencies**
It's recommended to use a **virtual environment**:
```bash
python -m venv env
source env/bin/activate   # On macOS/Linux
env\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### **3️⃣ Run the Streamlit App**
```bash
streamlit run sampling_regions.py
```
The app will be accessible at **`http://localhost:8501`**.

---

## 🐳 Running the App with Docker
If you prefer to run the app inside a **Docker container**, follow these steps.

### **1️⃣ Build the Docker Image**
```bash
docker build -t sampling-regions-app .
```

### **2️⃣ Run the Container**
```bash
docker run -p 8501:8501 sampling-regions-app
```
The app will be available at **`http://localhost:8501`**.

### **Using Docker Compose**
To run the app using **Docker Compose**, execute:
```bash
docker-compose up --build
```

This will:
- Build the Docker image (if not already built).
- Start the container with the correct settings.
- Mount the **data** and **assets** folders for persistence.

---

## 📂 Folder Structure
```
📁 sampling_regions/
│-- 📁 assets/       # Static files (logos, images)
│-- 📁 data/         # Data files (e.g., CSV, GeoJSON)
│-- sampling_regions.py   # Main Streamlit app
│-- Dockerfile       # Docker container setup
│-- docker-compose.yml # Docker Compose for multi-container setup
│-- requirements.txt # Python dependencies
│-- README.md        # Project documentation
│-- .gitignore       # Ignore unnecessary files in Git
```
---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📞 Contact
📧 **Developer:** [Bubele Rasmeni](https://github.com/BubeleRasmeni)  
---
