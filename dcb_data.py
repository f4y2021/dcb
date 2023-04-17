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


uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Find the row index where "Displacement" is located
    displacement_row_index = None
    for row in range(len(df)):
        for col in range(len(df.columns)):
            if df.iloc[row, col] == 'Displacement':
                displacement_row_index = row
                break
        if displacement_row_index is not None:
            break

    if displacement_row_index is None:
        st.write("Error: Could not find 'Displacement' in CSV file.")
    else:
        # Skip the appropriate number of rows to read in the displacement and force data
        data_start_row = displacement_row_index + 2
        df = pd.read_csv(uploaded_file, skiprows=data_start_row, usecols=[1, 2])
    st.write(df)

