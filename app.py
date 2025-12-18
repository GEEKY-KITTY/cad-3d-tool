import streamlit as st
import cadquery as cq
import trimesh
import numpy as np
import tempfile
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import feedparser  # NEW: For reading live news

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
    p, li, a {
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
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
        nozzle_size = st.number_input("Nozzle (mm)", 0
