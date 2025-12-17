import streamlit as st
import cadquery as cq
import trimesh
import numpy as np
import tempfile
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- 1. CONFIGURATION & ASSETS ---
st.set_page_config(
    page_title="CURIOSITY 3D | Platform",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL CSS (3D BACKGROUND & ANIMATIONS) ---
st.markdown("""
    <style>
    /* 1. The Moving 3D Grid Background */
    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(102, 252, 241, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(102, 252, 241, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        background-position: center center;
    }
    
    /* 2. Text & Headers */
    h1, h2, h3, h4 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    p, li {
        color: #c5c6c7;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* 3. Cyberpunk Cards */
    div.css-1r6slb0, .stMetric {
        background: rgba(11, 12, 16, 0.8);
        border: 1px solid #1f2833;
        border-left: 3px solid #66fcf1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 5px;
    }

    /* 4. Buttons */
    .stButton > button {
        background: transparent;
        border: 2px solid #45a29e;
        color: #66fcf1;
        border-radius: 0px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: #45a29e;
        color: black;
        box-shadow: 0 0 15px #45a29e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def visualize_mesh(mesh):
    x, y, z = mesh.vertices.T
    i, j, k = mesh.faces.T
    fig = go.Figure(data=[go.Mesh3d(
        x=x, y=y, z=z, i=i, j=j, k=k,
        color='#66fcf1', opacity=0.30, name='Model',
        flatshading=True
    )])
    # Add wireframe points for tech look
    if len(x) < 5000:
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z, mode='markers',
            marker=dict(size=1, color='#ffffff', opacity=0.3)
        ))
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)', aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("CURIOSITY 3D")
    st.caption("Engineering & Education Hub")
    st.markdown("---")
    page = st.radio("Navigation", ["🛠️ Converter Tool", "🚀 Future of CAD", "📰 Industry News"])
    st.markdown("---")
    
    if page == "🛠️ Converter Tool":
        st.header("Printer Specs")
        nozzle_size = st.number_input("Nozzle (mm)", 0.2, 1.2, 0.4)
        export_format = st.selectbox("Export Format", ["stl", "obj", "3mf", "ply"])

# --- 5. PAGE LOGIC ---

# === PAGE 1: THE TOOL ===
if page == "🛠️ Converter Tool":
    st.title("Intelligent CAD Converter")
    st.markdown("Convert **STEP** files to printable meshes with instant **DFM Analysis**.")
    
    uploaded_file = st.file_uploader("Upload STEP File", type=["step", "stp"])

    if uploaded_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, uploaded_file.name)
            temp_stl = os.path.join(temp_dir, "temp.stl")
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.status("Processing Geometry...", expanded=True) as status:
                try:
                    model = cq.importers.importStep(input_path)
                    cq.exporters.export(model, temp_stl)
                    status.update(label="Geometry Tessellated", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.stop()

            mesh = trimesh.load(temp_stl)
            
            c1, c2 = st.columns([3, 2])
            with c1:
                st.subheader("Interactive View")
                st.plotly_chart(visualize_mesh(mesh), use_container_width=True)
            with c2:
                st.subheader("Analysis")
                st.metric("Volume", f"{mesh.volume/1000:.1f} cm³")
                st.metric("Bounding Box", f"{mesh.extents[0]:.0f}x{mesh.extents[1]:.0f}x{mesh.extents[2]:.0f} mm")
                
                if not mesh.is_watertight:
                    st.error("⚠️ Non-Manifold Mesh")
                
                # Export
                if export_format != "stl":
                    out_path = os.path.join(temp_dir, f"out.{export_format}")
                    mesh.export(out_path)
                    data = open(out_path, "rb").read()
                else:
                    data = open(temp_stl, "rb").read()
                
                st.download_button(f"Download .{export_format.upper()}", data, file_name=f"{base_name}.{export_format}")

# === PAGE 2: FUTURE OF CAD ===
elif page == "🚀 Future of CAD":
    st.title("The Future of Prototyping")
    st.markdown("### From Parametric Modeling to Generative AI")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **Computer-Aided Design (CAD)** is undergoing a massive shift. We are moving away from explicitly drawing lines and arcs (Parametric) toward describing goals and constraints (Generative).
        
        * **Generative Design:** The computer explores thousands of iterations to find the optimal strength-to-weight ratio.
        * **AI Integration:** Tools like "Text-to-3D" allow rapid concepting before engineering begins.
        * **Digital Twins:** Real-time simulation of parts before they are ever physically printed.
        """)
        
        st.info("💡 **Did you know?** AI-driven topology optimization can reduce part weight by 40% while maintaining structural integrity.")

    with col2:
        # DATA VISUALIZATION: Market Growth
        data = pd.DataFrame({
            "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            "Market Size (Billion USD)": [9.9, 11.5, 12.6, 15.2, 18.3, 22.4, 26.8, 32.5]
        })
        
        fig = px.bar(
            data, x="Year", y="Market Size (Billion USD)",
            title="Global 3D Printing Market Growth",
            color="Market Size (Billion USD)",
            color_continuous_scale="teal"
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Evolution of Design")
    
    c_img1, c_img2, c_img3 = st.columns(3)
    with c_img1:
        st.image("https://images.unsplash.com/photo-1581094794329-c8112a89af12?q=80&w=600&auto=format&fit=crop", caption="Past: Manual Drafting")
    with c_img2:
        st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=600&auto=format&fit=crop", caption="Present: Parametric CAD")
    with c_img3:
        st.image("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=600&auto=format&fit=crop", caption="Future: AI Generative")

# === PAGE 3: NEWS ===
elif page == "📰 Industry News":
    st.title("Curated Industry Insights")
    st.markdown("Stay updated with the latest in Additive Manufacturing.")
    
    # Mock Article Data
    articles = [
        {
            "title": "Ultimaker announces S7 Pro Bundle",
            "desc": "The new flagship printer features integrated material handling and air filtration.",
            "tag": "Hardware"
        },
        {
            "title": "Bambu Lab disrupts consumer market",
            "desc": "High-speed coreXY systems are making advanced prototyping accessible to hobbyists.",
            "tag": "Market"
        },
        {
            "title": "NASA uses 3D Printing for Rocket Nozzles",
            "desc": "New copper alloys allow for heat resistance previously impossible with casting.",
            "tag": "Aerospace"
        },
        {
            "title": "AI in Slicing: The end of support failure?",
            "desc": "New algorithms predict overhang failure and adjust cooling automatically.",
            "tag": "Software"
        }
    ]
    
    for art in articles:
        with st.container():
            st.markdown(f"""
            <div style="
                background-color: #1a1a1d; 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 20px; 
                border-left: 5px solid #45a29e;">
                <h3 style="margin:0; color: #66fcf1;">{art['title']}</h3>
                <span style="background-color: #45a29e; color: black; padding: 2px 8px; font-size: 12px; border-radius: 4px; font-weight: bold;">{art['tag']}</span>
                <p style="margin-top: 10px; color: #c5c6c7;">{art['desc']}</p>
            </div>
            """, unsafe_allow_html=True)