import streamlit as st
import pandas as pd
import datetime
import time


def compond_yield(base, percent, duration):
    return round(base * (1 + percent) ** duration)


st.title("Wow 401k")
base = int(st.text_input("base", "2000000"))
percent = float(st.text_input("yearly yield %", "0.15") )
year_min= 2024
year_max= 2034
year = st.slider('year?', min_value=year_min, max_value=year_max, step=1)

duration = year - year_min
st.write(f"duration = {duration}")

year_place_holder = st.empty()
year_place_holder.text = year
total_place_holder = st.empty()
total = base * (1 + percent) ** duration
st.markdown(str(round(total)))

if "df" not in st.session_state:
    st.session_state.df = {}
    st.session_state.year_list =[]
    st.session_state.amt =[]


st.session_state.year_list = list(range(year_min, year+1)) # reconstruct the year list each time
st.session_state.amt =[compond_yield(base, percent, x-min(st.session_state.year_list)) for x in st.session_state.year_list] 



st.session_state.df = {'Year': st.session_state.year_list,
                        'Yield': st.session_state.amt}

chart_data=pd.DataFrame(st.session_state.df)

if st.checkbox("Display Data"):
    st.write(chart_data)
#st.bar_chart(chart_data, x="Year", y="Yield", width=10)
st.line_chart(chart_data, x="Year", y="Yield", width=10)



