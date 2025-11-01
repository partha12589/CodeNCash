"""
Quick test to verify charts are working
Run this to see if visualizations work correctly
"""

import streamlit as st
from utils.visualizations import PortfolioVisualizations

st.title("?? Chart Test Page")

viz = PortfolioVisualizations()

# Test 1: Pie Chart
st.header("Test 1: Pie Chart")
allocation = {'equity': 30, 'mutual_funds': 30, 'debt': 30, 'liquid': 10}
fig_pie = viz.create_allocation_pie_chart(allocation, "Test Allocation")
st.plotly_chart(fig_pie, use_container_width=True)

# Test 2: Returns Chart
st.header("Test 2: Returns Projection Chart")
projected_returns = {
    '1_year': {'total_value': 550000, 'gains': 50000},
    '3_year': {'total_value': 750000, 'gains': 150000},
    '5_year': {'total_value': 950000, 'gains': 300000}
}
fig_returns = viz.create_returns_chart(projected_returns, 500000, 10000)
st.plotly_chart(fig_returns, use_container_width=True)

# Test 3: Gains Bar Chart
st.header("Test 3: Gains Bar Chart")
fig_gains = viz.create_gains_bar_chart(projected_returns)
st.plotly_chart(fig_gains, use_container_width=True)

# Test 4: Diversification Chart
st.header("Test 4: Diversification Chart")
recommendations = {
    'stocks': {'amount': 150000, 'list': []},
    'mutual_funds': {'amount': 200000, 'list': []},
    'debt': {'amount': 150000, 'list': []}
}
fig_div = viz.create_diversification_chart(recommendations)
st.plotly_chart(fig_div, use_container_width=True)

st.success("? All charts rendered successfully!")
st.info("If you can see all 4 charts above, the visualization module is working correctly!")
