"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import streamlit as st

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import re
import sys

st.set_page_config(page_title="DCB",page_icon="⏩")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    font-size:16px;font-weight:bold;height:2em;width:7em;
}
</style>""", unsafe_allow_html=True)


st.title('DCB Data Analysis')

# User Inputs

with st.expander("User Inputs"):

    colunas12,colunas22,colunas32 = st.columns(3)

    with colunas12:
        a0 = st.number_input("Initial Pre-Crack Length [mm]")
        B = st.number_input("Specimen Width [mm]")
    with colunas22:
        thickness= st.number_input("Specimen Thickness [mm]")
        h=thickness/2
    with colunas32:
        G13=st.number_input("Shear modulus (GPa)")
        E2=st.number_input("Young’s modulus in the longitudinal direction (GPa) ")


uploaded_file = st.file_uploader("Upload DCB RAW Data CSV file", type=["csv"])

run_button=st.button("Run")

if run_button:

    df = pd.read_csv(uploaded_file, sep=",",usecols= [1,2], names=["Displacement","Force"],header=6)


    # Filter out rows with zero displacement
    df = df.loc[df["Displacement"] != 0]

    # Adjust data to start from (0,0)
    df["Displacement"] = df["Displacement"] - df["Displacement"].iloc[0]
    df["Force"] = df["Force"] - df["Force"].iloc[0]


    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    # Display data as a table and as a graph in two different tabs
    with tab1:
        st.write(df)
    with tab2:

        fig = px.scatter(df, x='Displacement', y='Force', color_discrete_sequence=["black"], 
                     template="ggplot2", title="P − δ Curve", 
                     labels={"Displacement": "Displacement (mm)", "Force": "Force (kN)"},)

        st.plotly_chart(fig, use_container_width=True)
