# 🧊 CAD-3D-Tool

**A local, browser-based engineering platform for converting STEP files to printable formats and performing DFM (Design for Manufacturing) analysis.**

This tool was built to solve the common engineering bottleneck of opening heavy CAD software (like Fusion 360 or SolidWorks) just to export a simple mesh for 3D printing. It provides a lightweight, "drag-and-drop" web interface for immediate conversion and verification.

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B) ![Status](https://img.shields.io/badge/Status-Active-success)

## 🚀 Features

* **Universal Conversion:** Convert industry-standard `.STEP` files into `.STL`, `.OBJ`, `.3MF`, `.PLY`, or `.GLB`.
* **Instant DFM Checks:** Automatically analyzes geometry for:
    * **Watertightness:** Ensures the mesh is manifold and slicer-ready.
    * **Volume & Bounding Box:** Quick physical dimension verification.
    * **Feature Viability:** Checks if the smallest features are printable based on your specific nozzle size.
* **Interactive 3D Viewer:** Built-in web viewer to inspect geometry, rotate, and zoom before downloading.
* **Educational Hub:** dedicated pages for Industry News and the Future of CAD (Generative Design & AI).

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based web framework)
* **Geometry Kernel:** [CadQuery](https://cadquery.readthedocs.io/) (OCP/OpenCASCADE wrapper for parametric STEP handling)
* **Mesh Analysis:** [Trimesh](https://trimesh.org/) (Geometry verification and format translation)
* **Visualization:** [Plotly](https://plotly.com/) (Interactive 3D rendering)

## 📦 Installation (Local Machine)

Because this tool uses a complex geometry kernel, it requires **Conda** to manage binary dependencies.

### Prerequisites
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.

 Step 1: Clone & Environment Setup
1.  Clone this repository or download the source code.
2.  Open your terminal (Anaconda Prompt on Windows) and navigate to the folder.
3.  Create the environment from the provided config file:

```bash
conda env create -f environment.yml
Step 2: Activate & Run
Activate the environment:

Bash

conda activate cad_app
Launch the tool:

Bash

streamlit run app.py
The tool will automatically open in your default web browser at http://localhost:8501.

☁️ Deployment (Streamlit Cloud)
This app is configured for deployment on Streamlit Community Cloud.

Push this code to a GitHub repository.

Log in to share.streamlit.io.

Deploy the app by selecting your repository.

Note: The build process takes ~5-8 minutes due to the installation of the CadQuery engine.

📄 File Structure
app.py - The main application script containing the UI and logic.

environment.yml - Configuration file for Conda to install dependencies (CadQuery, Trimesh, etc.).

README.md - Documentation.

🔮 Future Roadmap
[ ] Slicing Preview: Generate G-code previews directly in the browser.

[ ] Wall Thickness Heatmap: Visual indication of areas too thin for printing.

[ ] Batch Processing: Upload multiple STEP files and convert them all at once.
