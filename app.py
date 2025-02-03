import streamlit as st
import pandas as pd
import datetime
import time


def compound_yield(base, percent, duration):
    return round(base * (1 + percent) ** duration)

def compound_yield_with_yearly_contribution(base, yearlyContribution, percent, duration):
    return compound_yield(base, percent, duration) + round(yearlyContribution * ((1 + percent) ** duration - 1)/(1 + percent - 1))

st.title("Wow 401k")
starting_base = 2700000
base = int(st.text_input("base", str(starting_base)))
yearlyContribution = int(st.text_input("Yearly New Contribution", 10000))
percent = float(st.text_input("yearly yield %", "0.15") )
year_min= 2025
year_max= 2045
year = st.slider('Duration in year', min_value=year_min, max_value=year_max, step=1)

duration = year - year_min
st.write(f"duration = {duration}")

year_place_holder = st.empty()
year_place_holder.text = year
total_place_holder = st.empty()
total_0 = (base) * (1 + percent) ** duration
delta = yearlyContribution * ((1 + percent) ** duration - 1)/(1 + percent - 1)
total = base * (1 + percent) ** duration + yearlyContribution * ((1 + percent) ** duration - 1)/(1 + percent - 1)
st.markdown(":smile: Base Line Yield: " + str(round(total_0)))
st.markdown(":smile: Yearly New Yield: " + str(round(delta)))
st.markdown(":smile: Total Yield: " + str(round(total)))

if "df" not in st.session_state:
    st.session_state.df = {}
    st.session_state.year_list =[]
    st.session_state.amt =[]


st.session_state.year_list = list(range(year_min, year+1)) # reconstruct the year list each time
st.session_state.amt =[compound_yield_with_yearly_contribution(base, yearlyContribution, percent, x-min(st.session_state.year_list)) for x in st.session_state.year_list] 



st.session_state.df = {'Year': st.session_state.year_list,
                        'Yield': st.session_state.amt}

chart_data=pd.DataFrame(st.session_state.df)

if st.checkbox("Display Data"):
    st.write(chart_data)
#st.bar_chart(chart_data, x="Year", y="Yield", width=10)
st.line_chart(chart_data, x="Year", y="Yield", width=10)



