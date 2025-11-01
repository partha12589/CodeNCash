import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioGenerator
from utils.chat_handler import ChatHandler
from utils.market_data import IndianMarketData
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Finbot - Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🤖 Finbot: Your Personal Investment Advisor")
st.markdown("*Your AI-powered guide to building the perfect Indian investment portfolio*")
st.markdown("---")

# Initialize session state
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
    st.session_state.current_portfolio = None

# Initialize handlers
portfolio_gen = PortfolioGenerator()
chat_handler = ChatHandler()
market_data = IndianMarketData()

# Sidebar for user inputs
with st.sidebar:
    st.header("📊 Investment Details")
    
    # Capital input
    capital = st.number_input(
        "Initial Capital (₹)", 
        min_value=10000, 
        value=100000,
        step=10000,
        help="Your starting investment amount"
    )
    
    # Monthly investment
    monthly_investment = st.number_input(
        "Monthly Investment (₹)", 
        min_value=0, 
        value=5000,
        step=1000,
        help="Regular monthly SIP amount"
    )
    
    # Risk appetite
    risk_appetite = st.select_slider(
        "Risk Appetite",
        options=['Low', 'Medium', 'High'],
        value='Medium',
        help="Low = Conservative, Medium = Balanced, High = Aggressive"
    )
    
    # Investment preferences
    st.subheader("Investment Preferences")
    mutual_funds = st.checkbox("✅ Mutual Funds", value=True)
    stocks = st.checkbox("📈 Stocks (NSE/BSE)", value=True)
    debt_funds = st.checkbox("🏦 Debt Funds", value=True)
    bonds = st.checkbox("📋 Bonds", value=False)
    
    st.markdown("---")
    
    # Generate portfolio button
    generate_btn = st.button("🚀 Generate Portfolio", type="primary", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("💬 Chat with Finbot")
    st.caption("Ask me anything about investments in India")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Chat container
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about mutual funds, stocks, debt funds, returns, risk, etc..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # Get context from current portfolio if available
        context = ""
        if st.session_state.current_portfolio:
            context = f"User has portfolio: {st.session_state.current_portfolio['risk_level']} risk, ₹{st.session_state.current_portfolio['total_investment']} capital"
        
        # Get AI response
        response = chat_handler.get_response(prompt, context)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response)
        
        st.rerun()

with col2:
    st.subheader("📈 Portfolio Summary")
    
    # Generate portfolio
    if generate_btn:
        # Collect preferences
        preferences = {
            "mutual_funds": mutual_funds,
            "stocks": stocks,
            "debt_funds": debt_funds,
            "bonds": bonds
        }
        
        # Check if at least one preference is selected
        if not any(preferences.values()):
            st.error("❌ Please select at least one investment option!")
        else:
            # Generate portfolio
            portfolio = portfolio_gen.generate_portfolio(
                capital, monthly_investment, risk_appetite, preferences
            )
            
            # Store in session state
            st.session_state.current_portfolio = portfolio
            st.session_state.portfolio_generated = True
            
            # Display success message
            st.success("✅ Portfolio Generated Successfully!")
    
    # Display portfolio if it exists
    if st.session_state.portfolio_generated and st.session_state.current_portfolio:
        portfolio = st.session_state.current_portfolio
        
        # Investment summary
        st.metric("Total Investment", f"₹{portfolio['total_investment']:,}")
        st.metric("Monthly SIP", f"₹{portfolio['monthly_sip']:,}")
        st.metric("Risk Level", portfolio['risk_level'])
        
        st.markdown("**Asset Allocation:**")
        for asset_type, percentage in portfolio['allocation'].items():
            st.write(f"• {asset_type.title()}: {percentage}%")
        
        # Projected returns
        st.markdown("**Projected Returns:**")
        for period, values in portfolio['projected_returns'].items():
            period_name = period.replace("_", " ").title()
            st.write(f"**{period_name}:**")
            st.write(f"  💰 Total Value: ₹{values['total_value']:,.0f}")
            st.write(f"  📈 Gains: ₹{values['gains']:,.0f}")

        
        # Investment recommendations
        if portfolio['recommendations']:
            st.markdown("**Recommended Investments:**")
            
            # Stocks recommendations
            if 'stocks' in portfolio['recommendations']:
                with st.expander(f"📈 Stocks (₹{portfolio['recommendations']['stocks']['amount']:,.0f})"):
                    stocks_list = portfolio['recommendations']['stocks']['list']
                    for stock in stocks_list:
                        st.write(f"**{stock['symbol']}** - {stock['name']}")
                        st.caption(f"Sector: {stock['sector']}")
            
            # Mutual funds recommendations
            if 'mutual_funds' in portfolio['recommendations']:
                with st.expander(f"💰 Mutual Funds (₹{portfolio['recommendations']['mutual_funds']['amount']:,.0f})"):
                    mf_list = portfolio['recommendations']['mutual_funds']['list']
                    for mf in mf_list:
                        st.write(f"**{mf['name']}**")
                        st.caption(f"Category: {mf['category']} | 3Y Returns: {mf['returns_3y']}")
            
            # Debt recommendations
            if 'debt' in portfolio['recommendations']:
                with st.expander(f"🏦 Debt Options (₹{portfolio['recommendations']['debt']['amount']:,.0f})"):
                    debt_list = portfolio['recommendations']['debt']['list']
                    for debt in debt_list:
                        st.write(f"**{debt['name']}**")
                        st.caption(f"Type: {debt['type']} | Interest: {debt.get('interest_rate', 'N/A')}")
    else:
        st.info("👈 **Fill in your details and click 'Generate Portfolio'** to get started!")

# Footer
st.markdown("---")
st.caption("💡 Finbot provides investment suggestions based on Indian markets (NSE/BSE). Consult a financial advisor for personalized advice.")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
