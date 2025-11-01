import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioGenerator
from utils.chat_handler import ChatHandler
from utils.market_data import IndianMarketData
from utils.live_market_data import LiveMarketData, POPULAR_SCHEME_CODES
from utils.visualizations import PortfolioVisualizations
from datetime import datetime
import time
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="CodeNCash - AI Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check if logo exists
logo_path = Path("logo.png")  # or logo.jpg, logo.svg
logo_exists = logo_path.exists()

# Header with logo and live market data
st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)

# Create columns for header layout
if logo_exists:
    col_logo, col_title, col_indices = st.columns([0.5, 2, 1.5])
else:
    col_title, col_indices = st.columns([2, 1.5])

# Logo column
if logo_exists:
    with col_logo:
        st.image(str(logo_path), width=80)

# Title column
with col_title:
    st.markdown('<h1 class="gradient-text" style="margin:0;">💰 CodeNCash</h1>', unsafe_allow_html=True)
    st.markdown("*AI-Powered Investment Portfolio Generator for Indian Investors*")
    st.caption("🤖 Smart. Personalized. Profitable.")

# Market indices column
with col_indices:
    live_data = LiveMarketData()
    indices = live_data.get_market_indices()
    
    if indices:
        idx_col1, idx_col2 = st.columns(2)
        
        with idx_col1:
            if 'nifty' in indices:
                nifty = indices['nifty']
                change_color = "🟢" if nifty['change'] >= 0 else "🔴"
                st.metric(
                    "NIFTY 50",
                    f"₹{nifty['value']:,.2f}",
                    f"{change_color} {nifty['change']:.2f}%"
                )
        
        with idx_col2:
            if 'sensex' in indices:
                sensex = indices['sensex']
                change_color = "🟢" if sensex['change'] >= 0 else "🔴"
                st.metric(
                    "SENSEX",
                    f"₹{sensex['value']:,.2f}",
                    f"{change_color} {sensex['change']:.2f}%"
                )

st.markdown('</div>', unsafe_allow_html=True)

# Quick stats bar
stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.markdown("**📊 Asset Classes**")
    st.caption("Equity • Debt • Hybrid")

with stats_col2:
    st.markdown("**🎯 Risk Profiles**")
    st.caption("Low • Medium • High")

with stats_col3:
    st.markdown("**📈 Live Data**")
    st.caption("NSE • BSE • MF")

with stats_col4:
    st.markdown("**🤖 AI Powered**")
    st.caption("LLaMA 3.3 70B")

st.markdown("---")

# Initialize session state
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
    st.session_state.current_portfolio = None
if 'portfolio_history' not in st.session_state:
    st.session_state.portfolio_history = []
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

# Initialize handlers
portfolio_gen = PortfolioGenerator()
chat_handler = ChatHandler()
market_data = IndianMarketData()
live_market = LiveMarketData()
visualizer = PortfolioVisualizations()

# Sidebar for user inputs
with st.sidebar:
    # Logo in sidebar if exists
    if logo_exists:
        st.image(str(logo_path), width=100)
        st.markdown("---")
    
    st.markdown("### 📊 Investment Profile")
    
    # Investment Goal (NEW FEATURE)
    investment_goal = st.selectbox(
        "🎯 Investment Goal",
        ["Wealth Creation", "Retirement Planning", "Child Education", "Tax Saving", "Emergency Fund"],
        help="Select your primary investment goal"
    )
    
    # Time Horizon (NEW FEATURE)
    time_horizon = st.selectbox(
        "⏰ Time Horizon",
        ["Short Term (1-3 years)", "Medium Term (3-5 years)", "Long Term (5+ years)"],
        index=2,
        help="How long do you plan to invest?"
    )
    
    st.markdown("---")
    
    # Capital input with visual feedback
    capital = st.number_input(
        "💰 Initial Capital (₹)", 
        min_value=10000, 
        max_value=10000000,
        value=100000,
        step=10000,
        help="Your starting investment amount"
    )
    
    # Show capital category
    if capital < 50000:
        st.caption("🌱 Beginner Investor")
    elif capital < 500000:
        st.caption("💼 Growing Portfolio")
    else:
        st.caption("🏆 Serious Investor")
    
    # Monthly investment
    monthly_investment = st.number_input(
        "📅 Monthly SIP (₹)", 
        min_value=0, 
        max_value=100000,
        value=5000,
        step=1000,
        help="Regular monthly SIP amount"
    )
    
    # Calculate total investment over time
    total_1y = capital + (monthly_investment * 12)
    total_5y = capital + (monthly_investment * 60)
    
    with st.expander("📊 Investment Summary"):
        st.metric("1 Year Total", f"₹{total_1y:,}")
        st.metric("5 Year Total", f"₹{total_5y:,}")
    
    st.markdown("---")
    
    # Risk appetite with enhanced visual
    st.markdown("### 🎯 Risk Profile")
    risk_appetite = st.select_slider(
        "Select your risk tolerance",
        options=['Low', 'Medium', 'High'],
        value='Medium',
        help="Low = 8% returns | Medium = 12% | High = 15%"
    )
    
    # Enhanced risk indicator
    risk_info = {
        'Low': {'color': '🟢', 'desc': 'Safe & Stable', 'return': '8-10%', 'volatility': 'Low'},
        'Medium': {'color': '🟡', 'desc': 'Balanced Growth', 'return': '10-14%', 'volatility': 'Moderate'},
        'High': {'color': '🔴', 'desc': 'Maximum Growth', 'return': '14-18%', 'volatility': 'High'}
    }
    
    info = risk_info[risk_appetite]
    st.info(f"{info['color']} **{risk_appetite} Risk**\n\n"
            f"📈 Expected Return: {info['return']}\n\n"
            f"📊 Volatility: {info['volatility']}\n\n"
            f"💡 {info['desc']}")
    
    st.markdown("---")
    
    # Investment preferences with icons
    st.markdown("### 🎯 Asset Preferences")
    
    col_pref1, col_pref2 = st.columns(2)
    with col_pref1:
        mutual_funds = st.checkbox("💰 Mutual Funds", value=True)
        stocks = st.checkbox("📈 Stocks", value=True)
    
    with col_pref2:
        debt_funds = st.checkbox("🏦 Debt Funds", value=True)
        bonds = st.checkbox("📋 Bonds", value=False)
    
    # Tax Saving Option (NEW FEATURE)
    tax_saving = st.checkbox("💸 Include Tax Saving (ELSS)", value=False, 
                            help="Include tax saving mutual funds under Section 80C")
    
    # Show selected preferences
    selected_count = sum([mutual_funds, stocks, debt_funds, bonds])
    if selected_count > 0:
        st.success(f"✅ {selected_count} asset class{'es' if selected_count > 1 else ''} selected")
    else:
        st.error("⚠️ Select at least one asset class")
    
    st.markdown("---")
    
    # Generate portfolio button
    generate_btn = st.button(
        "🚀 Generate Portfolio", 
        type="primary", 
        use_container_width=True,
        disabled=(selected_count == 0)
    )
    
    # Portfolio comparison feature (NEW)
    if len(st.session_state.portfolio_history) > 1:
        if st.button("📊 Compare Portfolios", use_container_width=True):
            st.session_state.comparison_mode = True
    
    # Export options (NEW)
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    # Quick stats if portfolio exists
    if st.session_state.portfolio_generated and st.session_state.current_portfolio:
        portfolio = st.session_state.current_portfolio
        
        st.markdown("#### 💎 Portfolio Value")
        
        total_5y = portfolio['projected_returns']['5_year']['total_value']
        total_invested_5y = capital + (monthly_investment * 12 * 5)
        roi_5y = ((total_5y - total_invested_5y) / total_invested_5y * 100) if total_invested_5y > 0 else 0
        
        st.metric("5Y Projected", f"₹{total_5y:,.0f}", f"+{roi_5y:.1f}%")
        
        gains_5y = portfolio['projected_returns']['5_year']['gains']
        st.metric("5Y Gains", f"₹{gains_5y:,.0f}")

# Main content area
col1, col2 = st.columns([1.8, 1.2], gap="large")

with col1:
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Chat section header
    chat_header_col1, chat_header_col2 = st.columns([3, 1])
    with chat_header_col1:
        st.subheader("💬 Chat with CodeNCash AI")
        st.caption("Ask anything about investments, mutual funds, stocks, or financial planning")
    
    with chat_header_col2:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Enhanced suggested questions
    if len(st.session_state.messages) == 0:
        st.markdown("**💡 Quick Start Questions:**")
        
        suggestions = [
            ("🎯", "What are the best mutual funds for beginners?"),
            ("💰", "How does SIP investment work in India?"),
            ("📊", "Difference between debt and equity funds"),
            ("🏆", "Best retirement planning strategy"),
            ("💸", "Tax saving investment options in India"),
            ("📈", "How to build a diversified portfolio")
        ]
        
        # Create 2 columns for suggestions
        for i in range(0, len(suggestions), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(suggestions):
                    icon, text = suggestions[i + j]
                    with col:
                        display_text = text if len(text) <= 35 else text[:32] + "..."
                        if st.button(f"{icon} {display_text}", key=f"suggest_{i+j}", use_container_width=True):
                            st.session_state.messages.append({"role": "user", "content": text})
                            
                            context = ""
                            if st.session_state.current_portfolio:
                                context = f"User profile: {risk_appetite} risk, ₹{capital} capital, Goal: {investment_goal}"
                            
                            response = chat_handler.get_response(text, context)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.rerun()
    
    # Chat container
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("💬 Ask me anything about investments..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤔 Analyzing..."):
                    context = f"User profile: {risk_appetite} risk, ₹{capital} capital, {time_horizon}, Goal: {investment_goal}"
                    if st.session_state.current_portfolio:
                        context += f"\nCurrent portfolio generated with {selected_count} asset classes"
                    
                    response = chat_handler.get_response(prompt, context)
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    st.subheader("📊 Portfolio Dashboard")
    
    # Generate portfolio
    if generate_btn:
        preferences = {
            "mutual_funds": mutual_funds,
            "stocks": stocks,
            "debt_funds": debt_funds,
            "bonds": bonds,
            "tax_saving": tax_saving
        }
        
        if not any([mutual_funds, stocks, debt_funds, bonds]):
            st.error("❌ Please select at least one asset class!")
        else:
            # Enhanced progress animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_messages = [
                ("🔍", "Analyzing market conditions...", 20),
                ("📊", "Calculating optimal allocation...", 40),
                ("🎯", "Selecting best instruments...", 60),
                ("💼", "Building your portfolio...", 80),
                ("✨", "Finalizing recommendations...", 100)
            ]
            
            for icon, msg, progress in status_messages:
                status_text.markdown(f"{icon} {msg}")
                progress_bar.progress(progress)
                time.sleep(0.3)
            
            portfolio = portfolio_gen.generate_portfolio(
                capital, monthly_investment, risk_appetite, preferences
            )
            
            # Add metadata
            portfolio['goal'] = investment_goal
            portfolio['time_horizon'] = time_horizon
            portfolio['tax_saving'] = tax_saving
            portfolio['generated_at'] = datetime.now()
            
            progress_bar.empty()
            status_text.empty()
            
            st.session_state.current_portfolio = portfolio
            st.session_state.portfolio_generated = True
            st.session_state.portfolio_history.append(portfolio)
            
            st.success("✅ Portfolio Generated Successfully!")
            st.balloons()
    
    # Display portfolio
    if st.session_state.portfolio_generated and st.session_state.current_portfolio:
        portfolio = st.session_state.current_portfolio
        
        # Investment summary
        st.markdown("#### 💼 Investment Summary")
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("💰 Capital", f"₹{portfolio['total_investment']:,}")
            st.metric("📅 Monthly SIP", f"₹{portfolio['monthly_sip']:,}")
        
        with metric_col2:
            st.metric("🎯 Risk", portfolio['risk_level'])
            one_year_return = portfolio['projected_returns']['1_year']['gains']
            return_pct = (one_year_return / portfolio['total_investment']) * 100
            st.metric("📈 1Y Return", f"{return_pct:.1f}%")
        
        st.markdown("---")
        
        # PDF Download
        from utils.pdf_generator import generate_portfolio_pdf
        
        try:
            pdf_col1, pdf_col2 = st.columns([3, 1])
            
            with pdf_col1:
                pdf_data = generate_portfolio_pdf(portfolio)
                st.download_button(
                    label="📄 Download Portfolio Report",
                    data=pdf_data,
                    file_name=f"CodeNCash_Portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            
            with pdf_col2:
                if st.button("🔄", help="Regenerate", use_container_width=True):
                    st.rerun()
                    
        except Exception as e:
            st.error(f"❌ PDF Error: {str(e)}")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Allocation", "📈 Returns", "💼 Assets", "📋 Summary"])
        
        with tab1:
            fig_pie = visualizer.create_allocation_pie_chart(
                portfolio['allocation'],
                "Asset Allocation Strategy"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            if portfolio['recommendations']:
                fig_dist = visualizer.create_diversification_chart(portfolio['recommendations'])
                st.plotly_chart(fig_dist, use_container_width=True)
        
        with tab2:
            fig_returns = visualizer.create_returns_chart(
                portfolio['projected_returns'],
                portfolio['total_investment'],
                portfolio['monthly_sip']
            )
            st.plotly_chart(fig_returns, use_container_width=True)
            
            fig_gains = visualizer.create_gains_bar_chart(portfolio['projected_returns'])
            st.plotly_chart(fig_gains, use_container_width=True)
        
        with tab3:
            st.markdown("#### 🎯 Recommended Assets")
            
            if portfolio['recommendations']:
                # Stocks
                if 'stocks' in portfolio['recommendations']:
                    with st.expander(f"📈 Stocks (₹{portfolio['recommendations']['stocks']['amount']:,.0f})", expanded=True):
                        stocks_list = portfolio['recommendations']['stocks']['list']
                        enriched_stocks = live_market.enrich_stock_data(stocks_list)
                        
                        for stock in enriched_stocks:
                            cols = st.columns([3, 2, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{stock['symbol']}**")
                                st.caption(f"{stock['name'][:25]} | {stock['sector']}")
                            
                            with cols[1]:
                                if 'live_price' in stock:
                                    st.markdown(f"<span class='live-indicator'></span>₹{stock['live_price']}", unsafe_allow_html=True)
                                    st.caption("Live Price")
                            
                            with cols[2]:
                                if 'change_percent' in stock:
                                    change = stock['change_percent']
                                    color = "🟢" if change >= 0 else "🔴"
                                    st.markdown(f"{color} {change:+.2f}%")
                                    st.caption("Today")
                            
                            st.markdown("---")
                
                # Mutual Funds
                if 'mutual_funds' in portfolio['recommendations']:
                    with st.expander(f"💰 Mutual Funds (₹{portfolio['recommendations']['mutual_funds']['amount']:,.0f})"):
                        mf_list = portfolio['recommendations']['mutual_funds']['list']
                        
                        for mf in mf_list:
                            mf['scheme_code'] = POPULAR_SCHEME_CODES.get(mf['name'])
                        
                        enriched_funds = live_market.enrich_fund_data(mf_list)
                        
                        for mf in enriched_funds:
                            cols = st.columns([3, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{mf['name'][:30]}**")
                                st.caption(f"{mf['category']} | Returns: {mf['returns_3y']}")
                            
                            with cols[1]:
                                if 'current_nav' in mf:
                                    st.markdown(f"NAV: ₹{mf['current_nav']}")
                                    st.caption(f"{mf.get('nav_date', 'N/A')}")
                            
                            st.markdown("---")
                
                # Debt
                if 'debt' in portfolio['recommendations']:
                    with st.expander(f"🏦 Debt (₹{portfolio['recommendations']['debt']['amount']:,.0f})"):
                        for debt in portfolio['recommendations']['debt']['list']:
                            cols = st.columns([3, 2])
                            
                            with cols[0]:
                                st.markdown(f"**{debt['name'][:25]}**")
                                st.caption(f"Type: {debt['type']}")
                            
                            with cols[1]:
                                st.markdown(f"**{debt.get('interest_rate', 'N/A')}**")
                                st.caption("Interest Rate")
                            
                            st.markdown("---")
        
        with tab4:
            st.markdown("#### 📋 Portfolio Summary")
            
            st.markdown(f"""
            - **Investment Goal:** {portfolio.get('goal', 'Wealth Creation')}
            - **Time Horizon:** {portfolio.get('time_horizon', 'Long Term')}
            - **Risk Profile:** {portfolio['risk_level']}
            - **Asset Classes:** {len(portfolio.get('recommendations', {}))}
            - **Tax Saving:** {'Yes' if portfolio.get('tax_saving') else 'No'}
            """)
            
            st.markdown("---")
            st.markdown("**📈 Performance Metrics**")
            
            for period, values in portfolio['projected_returns'].items():
                year = period.replace('_', ' ').title()
                total = values['total_value']
                gains = values['gains']
                roi = (gains / portfolio['total_investment'] * 100) if portfolio['total_investment'] > 0 else 0
                
                with st.expander(f"**{year}** - ROI: {roi:.1f}%"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Value", f"₹{total:,.0f}")
                    col2.metric("Gains", f"₹{gains:,.0f}")
                    col3.metric("ROI", f"{roi:.1f}%")
    
    else:
        # Welcome screen
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 102, 255, 0.2) 0%, rgba(0, 217, 163, 0.2) 100%); 
                    padding: 2rem; border-radius: 20px; text-align: center; margin: 2rem 0;
                    border: 2px solid rgba(0, 217, 163, 0.5);'>
            <h2 style='color: #00D9A3; margin-bottom: 1rem;'>🚀 Ready to Build Your Portfolio?</h2>
            <p style='color: #A0AEC0; font-size: 16px;'>
                Fill in your investment details on the left<br/>
                and click <strong style='color: #0066FF;'>Generate Portfolio</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ✨ What Makes CodeNCash Special")
        
        features = [
            ("🤖", "AI-Powered Analysis", "LLaMA 3.3 70B for intelligent recommendations"),
            ("📊", "Live Market Data", "Real-time prices from NSE, BSE & MFapi"),
            ("🎯", "Personalized Strategy", "Tailored to your risk & goals"),
            ("📈", "Growth Projections", "1, 3 & 5 year forecasts"),
            ("💼", "Diversified Portfolio", "Across equity, debt & hybrid"),
            ("📄", "Professional Reports", "Downloadable PDF with charts")
        ]
        
        for icon, title, desc in features:
            st.markdown(f"""
            <div style='background: rgba(21, 27, 61, 0.8); padding: 1.2rem; border-radius: 12px; 
                        margin-bottom: 0.8rem; border-left: 4px solid #0066FF; backdrop-filter: blur(10px);'>
                <span style='font-size: 28px; float: left; margin-right: 15px;'>{icon}</span>
                <div>
                    <strong style='color: #00D9A3; font-size: 16px;'>{title}</strong><br/>
                    <span style='color: #A0AEC0; font-size: 14px;'>{desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("💼 **CodeNCash** - AI Investment Advisor")
    
with footer_col2:
    st.caption("⚠️ For educational purposes. Consult a certified advisor.")

with footer_col3:
    st.caption(f"🕒 {datetime.now().strftime('%d %b %Y | %H:%M:%S')}")