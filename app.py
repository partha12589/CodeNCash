import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioGenerator
from utils.chat_handler import ChatHandler
from utils.market_data import IndianMarketData
from utils.live_market_data import LiveMarketData, POPULAR_SCHEME_CODES
from utils.visualizations import PortfolioVisualizations
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Finbot - AI Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header with live market data
st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)
col_title, col_indices = st.columns([2, 1])

with col_title:
    st.title("🤖 Finbot: AI Investment Advisor")
    st.markdown("*Your AI-powered guide to building the perfect Indian investment portfolio*")

with col_indices:
    # Display live market indices
    live_data = LiveMarketData()
    indices = live_data.get_market_indices()
    
    if indices:
        if 'nifty' in indices:
            nifty = indices['nifty']
            change_color = "🟢" if nifty['change'] >= 0 else "🔴"
            st.metric(
                "NIFTY 50",
                f"₹{nifty['value']:,.2f}",
                f"{change_color} {nifty['change']:.2f}%"
            )
        
        if 'sensex' in indices:
            sensex = indices['sensex']
            change_color = "🟢" if sensex['change'] >= 0 else "🔴"
            st.metric(
                "SENSEX",
                f"₹{sensex['value']:,.2f}",
                f"{change_color} {sensex['change']:.2f}%",
                delta_color="off"
            )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
    st.session_state.current_portfolio = None

# Initialize handlers
portfolio_gen = PortfolioGenerator()
chat_handler = ChatHandler()
market_data = IndianMarketData()
live_market = LiveMarketData()
visualizer = PortfolioVisualizations()

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
    
    # Suggested questions (show only if no messages yet)
    if len(st.session_state.messages) == 0:
        st.markdown("**💡 Suggested Questions:**")
        suggested_cols = st.columns(2)
        
        suggestions = [
            "What are the best mutual funds for beginners?",
            "How does SIP investment work?",
            "Explain the difference between debt and equity funds",
            "What is the ideal portfolio for retirement planning?"
        ]
        
        for idx, suggestion in enumerate(suggestions):
            col_idx = idx % 2
            with suggested_cols[col_idx]:
                if st.button(f"💭 {suggestion[:30]}...", key=f"suggest_{idx}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    
                    # Get context
                    context = ""
                    if st.session_state.current_portfolio:
                        context = f"User has portfolio: {st.session_state.current_portfolio['risk_level']} risk, ₹{st.session_state.current_portfolio['total_investment']} capital"
                    
                    # Get AI response
                    response = chat_handler.get_response(suggestion, context)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
    
    # Chat container
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Show typing indicator if generating
        if 'generating' in st.session_state and st.session_state.generating:
            with st.chat_message("assistant"):
                st.markdown("💭 *Thinking...*")
    
    # Chat input
    if prompt := st.chat_input("Ask about mutual funds, stocks, debt funds, returns, risk, etc..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.generating = True
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Show typing indicator
            with st.chat_message("assistant"):
                with st.spinner("💭 Thinking..."):
                    # Get context from current portfolio if available
                    context = ""
                    if st.session_state.current_portfolio:
                        context = f"User has portfolio: {st.session_state.current_portfolio['risk_level']} risk, ₹{st.session_state.current_portfolio['total_investment']} capital"
                    
                    # Get AI response
                    response = chat_handler.get_response(prompt, context)
                
                st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.generating = False
        
        st.rerun()

with col2:
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    st.subheader("📈 Portfolio Summary")
    
    # Generate portfolio with loading animation
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
            # Show loading animation
            with st.spinner("🔄 Generating your personalized portfolio..."):
                time.sleep(0.5)  # Brief pause for UX
                
                # Generate portfolio
                portfolio = portfolio_gen.generate_portfolio(
                    capital, monthly_investment, risk_appetite, preferences
                )
                
                # Store in session state
                st.session_state.current_portfolio = portfolio
                st.session_state.portfolio_generated = True
                
            # Display success message with animation
            st.success("✅ Portfolio Generated Successfully!")
            st.balloons()
    
    # Display portfolio if it exists
    if st.session_state.portfolio_generated and st.session_state.current_portfolio:
        portfolio = st.session_state.current_portfolio
        
        # Investment summary with enhanced metrics
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("💰 Total Investment", f"₹{portfolio['total_investment']:,}")
            st.metric("📅 Monthly SIP", f"₹{portfolio['monthly_sip']:,}")
        with metric_col2:
            st.metric("🎯 Risk Level", portfolio['risk_level'])
            # Calculate expected 1-year return
            one_year_return = portfolio['projected_returns']['1_year']['gains']
            return_pct = (one_year_return / portfolio['total_investment']) * 100
            st.metric("📈 Expected Return (1Y)", f"{return_pct:.1f}%")
        
        st.markdown("---")
        with m2:
            st.metric("🎯 Risk Level", portfolio['risk_level'])
            # Calculate expected 1-year return
            one_year_return = portfolio['projected_returns']['1_year']['gains']
            return_pct = (one_year_return / portfolio['total_investment']) * 100
            st.metric("📈 Expected Return (1Y)", f"{return_pct:.1f}%")
        
        st.markdown("---")
         # PDF Download Button
        from utils.pdf_generator import generate_portfolio_pdf
        
        try:
            pdf_data = generate_portfolio_pdf(portfolio)
            
            st.download_button(
                label="📄 Download Portfolio as PDF",
                data=pdf_data,
                file_name=f"CodeNCash_Portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
        
        st.markdown("")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Allocation", "📈 Projections", "💼 Recommendations"])
        
        with tab1:
            # Asset Allocation Pie Chart
            fig_pie = visualizer.create_allocation_pie_chart(
                portfolio['allocation'],
                "Your Portfolio Allocation"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Distribution bar chart if recommendations exist
            if portfolio['recommendations']:
                fig_dist = visualizer.create_diversification_chart(
                    portfolio['recommendations']
                )
                st.plotly_chart(fig_dist, use_container_width=True)
        
        with tab2:
            # Returns projection chart
            fig_returns = visualizer.create_returns_chart(
                portfolio['projected_returns'],
                portfolio['total_investment'],
                portfolio['monthly_sip']
            )
            st.plotly_chart(fig_returns, use_container_width=True)
            
            # Gains bar chart
            fig_gains = visualizer.create_gains_bar_chart(
                portfolio['projected_returns']
            )
            st.plotly_chart(fig_gains, use_container_width=True)
        
        with tab3:
            st.markdown("### 🎯 Personalized Recommendations")

        
            # Investment recommendations with live data
            if portfolio['recommendations']:
                # Stocks recommendations with live prices
                if 'stocks' in portfolio['recommendations']:
                    with st.expander(f"📈 Stocks (₹{portfolio['recommendations']['stocks']['amount']:,.0f})", expanded=True):
                        stocks_list = portfolio['recommendations']['stocks']['list']
                        enriched_stocks = live_market.enrich_stock_data(stocks_list)
                        
                        for stock in enriched_stocks:
                            cols = st.columns([3, 2, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{stock['symbol']}**")
                                st.caption(f"{stock['name']} | {stock['sector']}")
                            
                            with cols[1]:
                                if 'live_price' in stock:
                                    st.markdown(f"<span class='live-indicator'></span>₹{stock['live_price']}", unsafe_allow_html=True)
                                    st.caption(f"Live Price")
                            
                            with cols[2]:
                                if 'change_percent' in stock:
                                    change = stock['change_percent']
                                    color = "🟢" if change >= 0 else "🔴"
                                    st.markdown(f"{color} {change:+.2f}%")
                                    st.caption(f"Today")
                            
                            st.markdown("---")
                
                # Mutual funds recommendations with live NAV
                if 'mutual_funds' in portfolio['recommendations']:
                    with st.expander(f"💰 Mutual Funds (₹{portfolio['recommendations']['mutual_funds']['amount']:,.0f})"):
                        mf_list = portfolio['recommendations']['mutual_funds']['list']
                        
                        # Add scheme codes to funds
                        for mf in mf_list:
                            mf['scheme_code'] = POPULAR_SCHEME_CODES.get(mf['name'])
                        
                        enriched_funds = live_market.enrich_fund_data(mf_list)
                        
                        for mf in enriched_funds:
                            cols = st.columns([3, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{mf['name']}**")
                                st.caption(f"{mf['category']} | 3Y Returns: {mf['returns_3y']}")
                            
                            with cols[1]:
                                if 'current_nav' in mf:
                                    st.markdown(f"NAV: ₹{mf['current_nav']}")
                                    st.caption(f"As of {mf.get('nav_date', 'N/A')}")
                            
                            st.markdown("---")
                
                # Debt recommendations
                if 'debt' in portfolio['recommendations']:
                    with st.expander(f"🏦 Debt Options (₹{portfolio['recommendations']['debt']['amount']:,.0f})"):
                        debt_list = portfolio['recommendations']['debt']['list']
                        for debt in debt_list:
                            cols = st.columns([3, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{debt['name']}**")
                                st.caption(f"Type: {debt['type']}")
                            
                            with cols[1]:
                                st.markdown(f"**{debt.get('interest_rate', 'N/A')}**")
                                st.caption(f"Interest Rate")
                            
                            st.markdown("---")
            else:
                st.info("No specific recommendations available for selected preferences.")
    else:
        # Welcome card when no portfolio is generated
        st.info("👈 **Fill in your details and click 'Generate Portfolio'** to get started!")
        
        # Show example metrics
        st.markdown("### 🌟 What You'll Get:")
        st.markdown("""
        - 📊 **Personalized Portfolio** based on your risk appetite
        - 📈 **Live Market Data** for stocks and mutual funds
        - 💹 **Growth Projections** for 1, 3, and 5 years
        - 🎯 **Specific Recommendations** from Indian markets
        - 💬 **AI Assistant** to answer all your investment questions
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("💡 Finbot provides investment suggestions based on Indian markets (NSE/BSE). Consult a financial advisor for personalized advice.")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
