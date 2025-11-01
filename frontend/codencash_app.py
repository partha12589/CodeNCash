"""
CodeNCash - AI-Powered Investment Advisor
Enhanced Interactive Frontend
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent.parent / "backend")
sys.path.insert(0, backend_path)

from services.portfolio_service import PortfolioGenerator
from services.chat_service import ChatHandler
from services.live_market_service import LiveMarketData
from services.visualization_service import PortfolioVisualizations
from assets.codencash_logo import LOGO_SVG, APP_NAME, TAGLINE

import time
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CodeNCash - AI Investment Advisor",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path(__file__).parent.parent / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def get_services():
    return {
        'portfolio': PortfolioGenerator(),
        'chat': ChatHandler(),
        'market': LiveMarketData(),
        'viz': PortfolioVisualizations()
    }

services = get_services()

# Initialize session state
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
    st.session_state.current_portfolio = None
    st.session_state.messages = []
    st.session_state.show_welcome = True

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)

col_logo, col_indices = st.columns([3, 2])

with col_logo:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown(f"*{TAGLINE}*")

with col_indices:
    # Live market indices
    indices = services['market'].get_market_indices()
    
    if indices:
        idx_col1, idx_col2 = st.columns(2)
        
        with idx_col1:
            if 'nifty' in indices:
                nifty = indices['nifty']
                delta_color = "normal" if nifty['change'] >= 0 else "inverse"
                st.metric(
                    "?? NIFTY 50",
                    f"{nifty['value']:,.0f}",
                    f"{nifty['change']:+.2f}%",
                    delta_color=delta_color
                )
        
        with idx_col2:
            if 'sensex' in indices:
                sensex = indices['sensex']
                delta_color = "normal" if sensex['change'] >= 0 else "inverse"
                st.metric(
                    "?? SENSEX",
                    f"{sensex['value']:,.0f}",
                    f"{sensex['change']:+.2f}%",
                    delta_color=delta_color
                )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR - INPUT FORM
# ============================================================================

with st.sidebar:
    st.markdown("## ?? Portfolio Builder")
    st.markdown("*Create your personalized investment portfolio*")
    st.markdown("")
    
    # Capital input with info
    capital = st.number_input(
        "?? Initial Investment",
        min_value=10000,
        max_value=100000000,
        value=500000,
        step=50000,
        help="Your starting investment amount in INR"
    )
    
    # Display formatted amount
    st.caption(f"?{capital:,}")
    
    st.markdown("")
    
    # Monthly SIP
    monthly_investment = st.number_input(
        "?? Monthly SIP Amount",
        min_value=0,
        max_value=10000000,
        value=10000,
        step=1000,
        help="Regular monthly investment (SIP)"
    )
    
    st.caption(f"?{monthly_investment:,}/month")
    
    st.markdown("")
    
    # Risk appetite with icons
    st.markdown("### ?? Risk Appetite")
    risk_appetite = st.select_slider(
        "",
        options=['Low', 'Medium', 'High'],
        value='Medium',
        help="Your comfort level with investment risk"
    )
    
    # Risk description
    risk_desc = {
        'Low': '?? Conservative - Focus on stability',
        'Medium': '?? Balanced - Mix of growth & safety',
        'High': '?? Aggressive - Maximum growth potential'
    }
    st.info(risk_desc[risk_appetite])
    
    st.markdown("---")
    
    # Investment preferences
    st.markdown("### ?? Investment Types")
    st.caption("Select where you want to invest:")
    
    mutual_funds = st.checkbox("?? Mutual Funds", value=True, help="Professionally managed funds")
    stocks = st.checkbox("?? Stocks (NSE/BSE)", value=True, help="Direct equity investments")
    debt_funds = st.checkbox("?? Debt Funds", value=True, help="Fixed income securities")
    bonds = st.checkbox("?? Government Bonds", value=False, help="Sovereign bonds")
    
    st.markdown("---")
    
    # Generate button
    generate_btn = st.button(
        "?? Generate My Portfolio",
        type="primary",
        use_container_width=True,
        help="Click to create your personalized portfolio"
    )
    
    # Stats
    st.markdown("")
    st.caption("?? **Tip:** Diversification reduces risk")
    st.caption(f"?? Selected: {sum([mutual_funds, stocks, debt_funds, bonds])} types")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Create main layout
main_col1, main_col2 = st.columns([1.5, 1], gap="large")

# ============================================================================
# LEFT COLUMN - CHAT INTERFACE
# ============================================================================

with main_col1:
    st.markdown("### ?? Chat with AI Advisor")
    
    # Welcome message
    if st.session_state.show_welcome and len(st.session_state.messages) == 0:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #151B3D 0%, #1a2351 100%); 
                    padding: 1.5rem; border-radius: 15px; border: 1px solid #2D3748;
                    margin-bottom: 1rem;'>
            <h4 style='color: #00D9A3; margin: 0 0 0.5rem 0;'>?? Welcome to CodeNCash!</h4>
            <p style='color: #A0AEC0; margin: 0; font-size: 14px;'>
                I'm your AI investment advisor. Ask me anything about investing in Indian markets!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Suggested questions
    if len(st.session_state.messages) == 0:
        st.markdown("**?? Try asking:**")
        
        suggestions = [
            "What's the best investment strategy for beginners?",
            "How does SIP investment work?",
            "Explain equity vs debt funds",
            "Best mutual funds for long-term growth?"
        ]
        
        cols = st.columns(2)
        for idx, suggestion in enumerate(suggestions):
            with cols[idx % 2]:
                if st.button(f"?? {suggestion[:35]}...", key=f"suggest_{idx}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": suggestion})
                    
                    context = ""
                    if st.session_state.current_portfolio:
                        context = f"User portfolio: {st.session_state.current_portfolio['risk_level']} risk, ?{st.session_state.current_portfolio['total_investment']:,}"
                    
                    response = services['chat'].get_response(suggestion, context)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.show_welcome = False
                    st.rerun()
    
    # Chat container
    chat_container = st.container(height=450, border=True)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about investments..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.show_welcome = False
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("?? Thinking..."):
                    context = ""
                    if st.session_state.current_portfolio:
                        context = f"User portfolio: {st.session_state.current_portfolio['risk_level']} risk, ?{st.session_state.current_portfolio['total_investment']:,}"
                    
                    response = services['chat'].get_response(prompt, context)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================================================
# RIGHT COLUMN - PORTFOLIO DISPLAY
# ============================================================================

with main_col2:
    st.markdown("### ?? Your Portfolio")
    
    # Generate portfolio
    if generate_btn:
        preferences = {
            "mutual_funds": mutual_funds,
            "stocks": stocks,
            "debt_funds": debt_funds,
            "bonds": bonds
        }
        
        if not any(preferences.values()):
            st.error("? Please select at least one investment type!")
        else:
            with st.spinner("?? Creating your personalized portfolio..."):
                time.sleep(0.8)
                
                portfolio = services['portfolio'].generate_portfolio(
                    capital, monthly_investment, risk_appetite, preferences
                )
                
                st.session_state.current_portfolio = portfolio
                st.session_state.portfolio_generated = True
            
            st.success("? Portfolio Created Successfully!")
            st.balloons()
            time.sleep(0.5)
            st.rerun()
    
    # Display portfolio
    if st.session_state.portfolio_generated and st.session_state.current_portfolio:
        portfolio = st.session_state.current_portfolio
        
        # Key metrics in cards
        st.markdown("""
        <div style='background: linear-gradient(135deg, #0066FF 0%, #00D9A3 100%);
                    padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;
                    box-shadow: 0 4px 15px rgba(0, 102, 255, 0.3);'>
            <h4 style='color: white; margin: 0 0 0.5rem 0;'>?? Portfolio Overview</h4>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 14px;'>
                Your personalized investment plan is ready!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("?? Investment", f"?{portfolio['total_investment']:,}")
            st.metric("?? Risk", portfolio['risk_level'])
        with m2:
            st.metric("?? Monthly SIP", f"?{portfolio['monthly_sip']:,}")
            one_year_gain = portfolio['projected_returns']['1_year']['gains']
            roi = (one_year_gain / portfolio['total_investment']) * 100
            st.metric("?? Expected ROI (1Y)", f"{roi:.1f}%")
        
        st.markdown("")
        
        # Expandable sections instead of tabs for better mobile support
        with st.expander("?? **Asset Allocation**", expanded=True):
            fig_pie = services['viz'].create_allocation_pie_chart(
                portfolio['allocation'],
                "Your Portfolio Mix"
            )
            st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")
        
        with st.expander("?? **Growth Projections**"):
            fig_returns = services['viz'].create_returns_chart(
                portfolio['projected_returns'],
                portfolio['total_investment'],
                portfolio['monthly_sip']
            )
            st.plotly_chart(fig_returns, use_container_width=True, key="returns_chart")
            
            # Summary table
            st.markdown("**?? Projected Returns:**")
            returns_data = []
            for period, values in portfolio['projected_returns'].items():
                year = period.replace('_', ' ').title()
                returns_data.append({
                    "Period": year,
                    "Total Value": f"?{values['total_value']:,.0f}",
                    "Gains": f"?{values['gains']:,.0f}"
                })
            st.table(pd.DataFrame(returns_data))
        
        with st.expander("?? **Investment Recommendations**"):
            if portfolio['recommendations']:
                # Stocks
                if 'stocks' in portfolio['recommendations']:
                    st.markdown(f"**?? Stocks** (?{portfolio['recommendations']['stocks']['amount']:,.0f})")
                    stocks_list = portfolio['recommendations']['stocks']['list']
                    enriched_stocks = services['market'].enrich_stock_data(stocks_list)
                    
                    for stock in enriched_stocks:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.markdown(f"**{stock['symbol']}**")
                            st.caption(stock['name'])
                        with col2:
                            if 'live_price' in stock:
                                st.markdown(f"?{stock['live_price']}")
                                st.caption("Live Price")
                        with col3:
                            if 'change_percent' in stock:
                                color = "??" if stock['change_percent'] >= 0 else "??"
                                st.markdown(f"{color} {stock['change_percent']:+.2f}%")
                    
                    st.markdown("---")
                
                # Mutual Funds
                if 'mutual_funds' in portfolio['recommendations']:
                    st.markdown(f"**?? Mutual Funds** (?{portfolio['recommendations']['mutual_funds']['amount']:,.0f})")
                    mf_list = portfolio['recommendations']['mutual_funds']['list']
                    
                    for mf in mf_list:
                        st.markdown(f"**{mf['name']}**")
                        st.caption(f"{mf['category']} ? Returns: {mf['returns_3y']}")
                        st.markdown("")
    
    else:
        # Welcome card
        st.markdown("""
        <div style='background: linear-gradient(135deg, #151B3D 0%, #1a2351 100%); 
                    padding: 2rem; border-radius: 15px; border: 1px solid #2D3748;
                    text-align: center; margin-top: 2rem;'>
            <h3 style='color: #00D9A3;'>?? Ready to Start?</h3>
            <p style='color: #A0AEC0; margin: 1rem 0;'>
                Fill in your details and click<br/>"Generate My Portfolio" to begin!
            </p>
            <div style='margin-top: 1.5rem; padding: 1rem; background: rgba(0,102,255,0.1); 
                        border-radius: 10px; border: 1px solid #0066FF;'>
                <p style='color: #0066FF; margin: 0; font-size: 14px; font-weight: 600;'>
                    ? Get personalized recommendations<br/>
                    ?? See interactive visualizations<br/>
                    ?? Chat with AI advisor<br/>
                    ?? Live market data
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.caption("?? **CodeNCash** - AI-Powered Investment Advisor")
with col_f2:
    st.caption("?? Live data from NSE, BSE & MFapi")
with col_f3:
    st.caption("?? Powered by Groq AI")

st.caption("?? *Disclaimer: This is for educational purposes. Consult a financial advisor before investing.*")
