"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import streamlit as st

import numpy as np
from numpy import sqrt 
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
    a0 = st.number_input("Initial Pre-Crack Length [mm]",value=50)
    colunas12,colunas22 = st.columns(2)

    with colunas12:
        st.caption("Geometric Properties")
        B = st.number_input("Specimen Width [mm]",value=25)
        thickness= st.number_input("Specimen Thickness [mm]",value=4.4)
        h=thickness/2
    with colunas22:
        st.caption("Material Properties")
        G13=st.number_input("Shear modulus (GPa)",value=2500)
        E2=st.number_input("Young’s modulus in the longitudinal direction (GPa)",value=8820)
        
E_inter=93600
C0=1.08

T=1.18*(sqrt(E2*E_inter))/G13
st.write(T)
delta=h*sqrt((E_inter/(11*G13))*(3-2*(T/(1+T))**2))
st.write(delta)
alpha=8/(B*h**3*E_inter)
st.write(alpha)
beta=12/(5*B*h*G13)
st.write(beta)
inc=a0+delta
Ef=(C0-(12*inc)/(5*B*h*G13))**(-1)*((8*inc**3)/(B*h**3))

st.write(Ef)
        
uploaded_file = st.file_uploader("Upload DCB RAW Data CSV file", type=["csv"])

run_button=st.button("Run")

if run_button:

    df = pd.read_csv(uploaded_file, sep=",",usecols= [1,2], names=["Displacement","Force"],header=6)


    # Filter out rows with zero displacement
    df = df.loc[df["Displacement"] != 0]

    # Adjust data to start from (0,0)
    df["Displacement"] = df["Displacement"] - df["Displacement"].iloc[0]
    df["Force"] = df["Force"]*1000
    df["Force"] = df["Force"] - df["Force"].iloc[0]


    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    # Display data as a table and as a graph in two different tabs
    with tab1:
        st.write(df)
    with tab2:

        fig1 = px.scatter(df, x='Displacement', y='Force', color_discrete_sequence=["black"], 
                     template="ggplot2", title="P − δ Curve", 
                     labels={"Displacement": "Displacement (mm)", "Force": "Force (kN)"},)

        st.plotly_chart(fig1, use_container_width=True)
        
    df['C']=df['Displacement']/df['Force']
    df['A']=((108*df['C']+12*sqrt(3*((4*beta**3+27*(-df['C'])**2*alpha)/(alpha))))*alpha**2)**(1/3)
    df['aeq']=df['A']/(6*alpha)-((2*beta)/(df['A']))
    df['GI']=((6*df["Force"]**2)/(B**2*h))*(((2*df['aeq']**2)/(E_inter*h**2))+((1)/(5*G13)))
    st.write(df)
    fig2 = px.scatter(df, x='aeq', y='GI', color_discrete_sequence=["black"], 
                     template="ggplot2", title="R Curve", 
                     labels={"aeq": "Crack Equivalent Length (mm)", "GI": "Gk (N/mm)"},)

    st.plotly_chart(fig2, use_container_width=True)
