import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioGenerator
from utils.chat_handler import ChatHandler
from utils.market_data import IndianMarketData
from utils.live_market_data import LiveMarketData, POPULAR_SCHEME_CODES
from utils.visualizations import PortfolioVisualizations
from utils.tax_optimizer import TaxOptimizer
from utils.goal_based_planning import GoalBasedPlanner
from datetime import datetime
import time
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

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

# Check for logo
logo_path = Path("logo.png")
logo_exists = logo_path.exists()

# Initialize session state
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
if 'current_portfolio' not in st.session_state:
    st.session_state.current_portfolio = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Portfolio"
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = ""

# Initialize handlers
portfolio_gen = PortfolioGenerator()
chat_handler = ChatHandler()
market_data = IndianMarketData()
live_market = LiveMarketData()
visualizer = PortfolioVisualizations()
tax_optimizer = TaxOptimizer()
goal_planner = GoalBasedPlanner()

# Header with enhanced styling
st.markdown('<div class="main-header fade-in">', unsafe_allow_html=True)
header_cols = st.columns([0.5, 2, 1.5]) if logo_exists else st.columns([2, 1.5])

if logo_exists:
    with header_cols[0]:
        st.image(str(logo_path), width=80)
    title_col = header_cols[1]
    market_col = header_cols[2]
else:
    title_col = header_cols[0]
    market_col = header_cols[1]

with title_col:
    st.markdown('<h1 class="gradient-text" style="margin:0;">💰 CodeNCash</h1>', unsafe_allow_html=True)
    st.markdown("*AI-Powered Investment Advisor for India*")
    st.caption("🤖 Powered by LLaMA 3.3 70B | 📊 Live Market Data")

with market_col:
    indices = live_market.get_market_indices()
    if indices:
        idx_col1, idx_col2 = st.columns(2)
        with idx_col1:
            if 'nifty' in indices:
                nifty = indices['nifty']
                st.metric("NIFTY 50", f"₹{nifty['value']:,.2f}", 
                         f"{'🟢' if nifty['change'] >= 0 else '🔴'} {nifty['change']:.2f}%")
        with idx_col2:
            if 'sensex' in indices:
                sensex = indices['sensex']
                st.metric("SENSEX", f"₹{sensex['value']:,.2f}",
                         f"{'🟢' if sensex['change'] >= 0 else '🔴'} {sensex['change']:.2f}%")

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Navigation with better styling
st.markdown("---")
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
nav_cols = st.columns(4)
pages = ["💼 Portfolio", "💸 Tax Optimizer", "🎯 Goal Planner", "💬 AI Chat"]

for idx, (col, page) in enumerate(zip(nav_cols, pages)):
    with col:
        page_name = page.split()[1]
        if st.button(page, use_container_width=True, 
                    type="primary" if st.session_state.current_page == page_name else "secondary",
                    key=f"nav_{page_name}"):
            st.session_state.current_page = page_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== PORTFOLIO GENERATOR PAGE ====================
if st.session_state.current_page == "Portfolio":
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 2], gap="large")
    
    with col1:
        st.markdown("### 📊 Investment Profile")
        st.markdown("*Build your personalized portfolio*")
        st.markdown("")
        
        # Investment Goal
        investment_goal = st.selectbox(
            "🎯 Investment Goal",
            ["Wealth Creation", "Retirement Planning", "Child Education", "Tax Saving", "Emergency Fund"],
            help="Select your primary investment objective",
            key="investment_goal_select"
        )
        
        # Time Horizon
        time_horizon = st.selectbox(
            "⏰ Investment Horizon",
            ["Short Term (1-3 years)", "Medium Term (3-5 years)", "Long Term (5+ years)"],
            index=2,
            help="Your investment time period",
            key="time_horizon_select"
        )
        
        st.markdown("---")
        
        # Capital input with enhanced styling
        capital = st.number_input(
            "💰 Initial Capital (₹)", 
            min_value=10000, 
            max_value=10000000,
            value=100000,
            step=10000,
            help="Your starting investment amount",
            key="capital_input"
        )
        
        # Show capital category with enhanced UI
        if capital < 50000:
            st.info("🌱 **Beginner Investor** - Great start to your journey!")
        elif capital < 500000:
            st.success("💼 **Growing Portfolio** - Building wealth steadily!")
        else:
            st.success("🏆 **Serious Investor** - Excellent capital base!")
        
        # Monthly investment
        monthly_investment = st.number_input(
            "📅 Monthly SIP (₹)", 
            min_value=0, 
            max_value=100000,
            value=5000,
            step=1000,
            help="Regular monthly SIP amount",
            key="monthly_sip_input"
        )
        
        # Enhanced projection
        if monthly_investment > 0:
            total_1y = capital + (monthly_investment * 12)
            total_5y = capital + (monthly_investment * 60)
            
            with st.expander("📊 Investment Projection", expanded=True):
                proj_col1, proj_col2 = st.columns(2)
                proj_col1.metric("1 Year Total", f"₹{total_1y:,}")
                proj_col2.metric("5 Year Total", f"₹{total_5y:,}")
        
        st.markdown("---")
        
        # Risk appetite with enhanced visual
        st.markdown("### 🎯 Risk Profile")
        risk_appetite = st.select_slider(
            "Select your risk tolerance",
            options=['Low', 'Medium', 'High'],
            value='Medium',
            help="Low = 8% returns | Medium = 12% | High = 15%",
            key="risk_appetite_slider"
        )
        
        # Enhanced risk info cards
        risk_info = {
            'Low': {'color': '🟢', 'desc': 'Safe & Stable', 'return': '8-10%', 'volatility': 'Low', 'suitable': 'Conservative investors, near retirement'},
            'Medium': {'color': '🟡', 'desc': 'Balanced Growth', 'return': '10-14%', 'volatility': 'Moderate', 'suitable': 'Balanced investors, 5-10 year horizon'},
            'High': {'color': '🔴', 'desc': 'Maximum Growth', 'return': '14-18%', 'volatility': 'High', 'suitable': 'Aggressive investors, 10+ year horizon'}
        }
        
        info = risk_info[risk_appetite]
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(0, 217, 163, 0.1) 100%);
                    padding: 1.5rem; border-radius: 15px; border-left: 4px solid #0066FF; margin: 1rem 0;'>
            <h3 style='color: #00D9A3; margin: 0;'>{info['color']} {risk_appetite} Risk Profile</h3>
            <p style='color: #A0AEC0; margin: 0.5rem 0;'>📈 <strong>Expected Returns:</strong> {info['return']}</p>
            <p style='color: #A0AEC0; margin: 0.5rem 0;'>📊 <strong>Volatility:</strong> {info['volatility']}</p>
            <p style='color: #A0AEC0; margin: 0.5rem 0;'>💡 <strong>{info['desc']}</strong></p>
            <p style='color: #718096; font-size: 0.9em; margin: 0.5rem 0;'>✅ Suitable for: {info['suitable']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Asset preferences with enhanced styling
        st.markdown("### 🎯 Asset Preferences")
        st.caption("Select the asset classes you want to invest in")
        
        col_a, col_b = st.columns(2)
        with col_a:
            mutual_funds = st.checkbox("💰 Mutual Funds", True, key="cb_mf")
            stocks = st.checkbox("📈 Stocks", True, key="cb_stocks")
        with col_b:
            debt_funds = st.checkbox("🏦 Debt Funds", True, key="cb_debt")
            bonds = st.checkbox("📋 Bonds", False, key="cb_bonds")
        
        selected_count = sum([mutual_funds, stocks, debt_funds, bonds])
        
        if selected_count > 0:
            st.success(f"✅ {selected_count} asset class{'es' if selected_count > 1 else ''} selected")
        else:
            st.error("⚠️ Please select at least one asset class")
        
        st.markdown("---")
        
        # Enhanced generate button
        if st.button("🚀 Generate My Portfolio", type="primary", use_container_width=True, 
                    disabled=(selected_count == 0), key="generate_portfolio_btn"):
            preferences = {
                "mutual_funds": mutual_funds,
                "stocks": stocks,
                "debt_funds": debt_funds,
                "bonds": bonds
            }
            
            if any(preferences.values()):
                # Enhanced progress with animations
                progress_container = st.empty()
                status_container = st.empty()
                
                progress_steps = [
                    ("🔍", "Analyzing market conditions...", 20),
                    ("🧠", "AI processing your profile...", 40),
                    ("📊", "Calculating optimal allocation...", 60),
                    ("🎯", "Selecting best instruments...", 80),
                    ("✨", "Finalizing recommendations...", 100)
                ]
                
                for icon, msg, progress in progress_steps:
                    with progress_container:
                        st.progress(progress / 100)
                    with status_container:
                        st.info(f"{icon} {msg}")
                    time.sleep(0.4)
                
                # Generate portfolio
                portfolio = portfolio_gen.generate_portfolio(
                    capital, monthly_investment, risk_appetite, preferences
                )
                
                # Add metadata
                portfolio['goal'] = investment_goal
                portfolio['time_horizon'] = time_horizon
                portfolio['generated_at'] = datetime.now()
                
                st.session_state.current_portfolio = portfolio
                st.session_state.portfolio_generated = True
                
                # Update chat context
                st.session_state.chat_context = (
                    f"User has generated a portfolio with the following details:\n"
                    f"- Investment Goal: {investment_goal}\n"
                    f"- Time Horizon: {time_horizon}\n"
                    f"- Initial Capital: ₹{capital:,}\n"
                    f"- Monthly SIP: ₹{monthly_investment:,}\n"
                    f"- Risk Profile: {risk_appetite}\n"
                    f"- Asset Classes: {', '.join([k.replace('_', ' ').title() for k, v in preferences.items() if v])}\n"
                    f"- Expected 5Y Returns: ₹{portfolio['projected_returns']['5_year']['total_value']:,.0f}"
                )
                
                progress_container.empty()
                status_container.empty()
                
                st.success("✅ Portfolio Generated Successfully!")
                st.balloons()
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Please select at least one asset class")
    
    with col2:
        st.markdown("### 📈 Your Investment Portfolio")
        
        if st.session_state.portfolio_generated and st.session_state.current_portfolio:
            portfolio = st.session_state.current_portfolio
            
            # Enhanced metrics section
            st.markdown("#### 💼 Portfolio Summary")
            m1, m2, m3, m4 = st.columns(4)
            
            with m1:
                st.metric("💰 Initial Capital", f"₹{portfolio['total_investment']:,}")
            with m2:
                st.metric("📅 Monthly SIP", f"₹{portfolio['monthly_sip']:,}")
            with m3:
                st.metric("🎯 Risk Level", portfolio['risk_level'])
            with m4:
                one_yr = portfolio['projected_returns']['1_year']['gains']
                return_pct = (one_yr / portfolio['total_investment'] * 100) if portfolio['total_investment'] > 0 else 0
                st.metric("📈 1Y Return", f"{return_pct:.1f}%")
            
            st.markdown("---")
            
            # Quick actions
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                # PDF Download
                from utils.pdf_generator import generate_portfolio_pdf
                try:
                    pdf_data = generate_portfolio_pdf(portfolio)
                    st.download_button(
                        "📄 Download Report",
                        pdf_data,
                        f"CodeNCash_Portfolio_{datetime.now().strftime('%Y%m%d')}.pdf",
                        "application/pdf",
                        use_container_width=True,
                        key="download_pdf_btn"
                    )
                except Exception as e:
                    st.error(f"PDF generation error: {str(e)}")
            
            with action_col2:
                if st.button("🔄 Generate New", use_container_width=True, key="regenerate_btn"):
                    st.session_state.portfolio_generated = False
                    st.session_state.current_portfolio = None
                    st.rerun()
            
            st.markdown("---")
            
            # Enhanced tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Allocation", "📈 Returns", "💼 Holdings", "📋 Analysis"])
            
            with tab1:
                st.markdown("#### Asset Allocation Strategy")
                fig_pie = visualizer.create_allocation_pie_chart(portfolio['allocation'], "Your Asset Mix")
                st.plotly_chart(fig_pie, use_container_width=True)
                
                if portfolio.get('recommendations'):
                    st.markdown("#### Investment Distribution")
                    fig_dist = visualizer.create_diversification_chart(portfolio['recommendations'])
                    st.plotly_chart(fig_dist, use_container_width=True)
            
            with tab2:
                st.markdown("#### Growth Projection")
                fig_returns = visualizer.create_returns_chart(
                    portfolio['projected_returns'],
                    portfolio['total_investment'],
                    portfolio['monthly_sip']
                )
                st.plotly_chart(fig_returns, use_container_width=True)
                
                st.markdown("#### Expected Gains")
                fig_gains = visualizer.create_gains_bar_chart(portfolio['projected_returns'])
                st.plotly_chart(fig_gains, use_container_width=True)
            
            with tab3:
                st.markdown("#### 🎯 Recommended Investments")
                
                # Stocks
                if 'stocks' in portfolio.get('recommendations', {}):
                    stock_data = portfolio['recommendations']['stocks']
                    with st.expander(f"📈 Equity Stocks - ₹{stock_data['amount']:,.0f}", expanded=True):
                        st.caption(f"Invest in {len(stock_data['list'])} top blue-chip stocks")
                        
                        for idx, stock in enumerate(stock_data['list'][:5], 1):
                            allocation = stock_data['amount'] / len(stock_data['list'])
                            
                            st.markdown(f"""
                            <div style='background: rgba(21, 27, 61, 0.6); padding: 1rem; border-radius: 10px; 
                                        margin: 0.5rem 0; border-left: 3px solid #0066FF;'>
                                <strong style='color: #00D9A3; font-size: 1.1em;'>{idx}. {stock['symbol']}</strong>
                                <br/>
                                <span style='color: #A0AEC0;'>{stock['name'][:30]} | {stock['sector']}</span>
                                <br/>
                                <span style='color: #FFB800; font-weight: bold;'>Suggested: ₹{allocation:,.0f}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Mutual Funds
                if 'mutual_funds' in portfolio.get('recommendations', {}):
                    mf_data = portfolio['recommendations']['mutual_funds']
                    with st.expander(f"💰 Mutual Funds - ₹{mf_data['amount']:,.0f}"):
                        st.caption(f"Diversified equity mutual funds")
                        
                        for idx, mf in enumerate(mf_data['list'][:3], 1):
                            sip_per_fund = (portfolio['monthly_sip'] * 0.4) / len(mf_data['list'])
                            
                            st.markdown(f"""
                            <div style='background: rgba(21, 27, 61, 0.6); padding: 1rem; border-radius: 10px; 
                                        margin: 0.5rem 0; border-left: 3px solid #00D9A3;'>
                                <strong style='color: #00D9A3; font-size: 1.1em;'>{idx}. {mf['name'][:35]}</strong>
                                <br/>
                                <span style='color: #A0AEC0;'>{mf['category']} | 3Y Returns: {mf['returns_3y']}</span>
                                <br/>
                                <span style='color: #FFB800; font-weight: bold;'>Monthly SIP: ₹{sip_per_fund:,.0f}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Debt
                if 'debt' in portfolio.get('recommendations', {}):
                    debt_data = portfolio['recommendations']['debt']
                    with st.expander(f"🏦 Debt Instruments - ₹{debt_data['amount']:,.0f}"):
                        st.caption("Safe and stable fixed-income investments")
                        
                        for idx, debt in enumerate(debt_data['list'][:3], 1):
                            allocation = debt_data['amount'] / len(debt_data['list'])
                            
                            st.markdown(f"""
                            <div style='background: rgba(21, 27, 61, 0.6); padding: 1rem; border-radius: 10px; 
                                        margin: 0.5rem 0; border-left: 3px solid #10B981;'>
                                <strong style='color: #10B981; font-size: 1.1em;'>{idx}. {debt['name'][:30]}</strong>
                                <br/>
                                <span style='color: #A0AEC0;'>{debt['type']} | Interest: {debt.get('interest_rate', 'N/A')}</span>
                                <br/>
                                <span style='color: #FFB800; font-weight: bold;'>Suggested: ₹{allocation:,.0f}</span>
                            </div>
                            """, unsafe_allow_html=True)
            
            with tab4:
                st.markdown("#### 📋 Detailed Analysis")
                
                st.markdown(f"""
                **Investment Overview:**
                - 🎯 Goal: {portfolio.get('goal', 'Wealth Creation')}
                - ⏰ Time Horizon: {portfolio.get('time_horizon', 'Long Term')}
                - 🎲 Risk Profile: {portfolio['risk_level']}
                - 📊 Asset Classes: {len(portfolio.get('recommendations', {}))}
                - 📅 Generated: {portfolio.get('generated_at', datetime.now()).strftime('%d %b %Y, %I:%M %p')}
                """)
                
                st.markdown("---")
                st.markdown("**📈 Performance Projections**")
                
                for period, values in sorted(portfolio['projected_returns'].items()):
                    year = period.replace('_', ' ').title()
                    total = values['total_value']
                    gains = values['gains']
                    invested = portfolio['total_investment'] + (portfolio['monthly_sip'] * 12 * int(period.split('_')[0]))
                    roi = (gains / invested * 100) if invested > 0 else 0
                    
                    with st.expander(f"**{year}** - Expected ROI: {roi:.1f}%"):
                        perf_col1, perf_col2, perf_col3 = st.columns(3)
                        perf_col1.metric("Total Value", f"₹{total:,.0f}")
                        perf_col2.metric("Total Gains", f"₹{gains:,.0f}")
                        perf_col3.metric("ROI", f"{roi:.1f}%")
                        
                        st.caption(f"Total Invested: ₹{invested:,.0f}")
        
        else:
            # Enhanced welcome screen
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(0, 102, 255, 0.15) 0%, rgba(0, 217, 163, 0.15) 100%); 
                        padding: 3rem 2rem; border-radius: 20px; text-align: center; margin: 2rem 0;
                        border: 2px solid rgba(0, 217, 163, 0.4); backdrop-filter: blur(10px);'>
                <h2 style='color: #00D9A3; margin-bottom: 1.5rem; font-size: 2em;'>
                    🚀 Ready to Build Your Wealth?
                </h2>
                <p style='color: #A0AEC0; font-size: 1.1em; line-height: 1.6;'>
                    Fill in your investment preferences on the left sidebar<br/>
                    and click <strong style='color: #0066FF;'>Generate My Portfolio</strong><br/>
                    to get AI-powered investment recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### ✨ What Makes CodeNCash Special")
            
            features = [
                ("🤖", "AI-Powered Analysis", "Advanced LLaMA 3.3 70B model for intelligent recommendations"),
                ("📊", "Live Market Data", "Real-time prices from NSE, BSE & Mutual Fund API"),
                ("🎯", "Personalized Strategy", "Tailored to your risk profile and financial goals"),
                ("📈", "Growth Projections", "Detailed 1, 3 & 5 year performance forecasts"),
                ("💼", "Diversified Portfolio", "Balanced allocation across equity, debt & hybrid funds"),
                ("📄", "Professional Reports", "Downloadable PDF with detailed charts and analysis"),
                ("💬", "AI Chat Support", "24/7 investment advisor chatbot with portfolio context"),
                ("🔒", "Secure & Private", "Your data never leaves your browser")
            ]
            
            feat_col1, feat_col2 = st.columns(2)
            
            for idx, (icon, title, desc) in enumerate(features):
                col = feat_col1 if idx % 2 == 0 else feat_col2
                with col:
                    st.markdown(f"""
                    <div style='background: rgba(21, 27, 61, 0.8); padding: 1.2rem; border-radius: 12px; 
                                margin-bottom: 1rem; border-left: 4px solid #0066FF; backdrop-filter: blur(10px);
                                transition: all 0.3s ease;'>
                        <span style='font-size: 2em; margin-right: 0.5rem;'>{icon}</span>
                        <strong style='color: #00D9A3; font-size: 1.1em;'>{title}</strong>
                        <br/>
                        <span style='color: #A0AEC0; font-size: 0.95em;'>{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAX OPTIMIZER PAGE ====================
elif st.session_state.current_page == "Tax":
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    st.markdown("### 💸 Tax Optimizer")
    st.caption("Optimize your tax savings under Indian tax laws")
    
    tax_tab1, tax_tab2, tax_tab3 = st.tabs(["🧮 Tax Calculator", "💡 80C Planner", "🏠 Home Loan Benefits"])
    
    with tax_tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Your Income Details")
            annual_income = st.number_input(
                "Annual Gross Income (₹)",
                0, 10000000, 1000000, 50000,
                key="tax_annual_income"
            )
            
            st.markdown("#### Deductions (Old Regime)")
            deductions = {}
            deductions['80c'] = st.number_input("Section 80C (max ₹1.5L)", 0, 150000, 0, 10000, key="ded_80c")
            deductions['80ccd_1b'] = st.number_input("NPS - 80CCD(1B) (max ₹50k)", 0, 50000, 0, 10000, key="ded_nps")
            deductions['80d'] = st.number_input("Health Insurance - 80D", 0, 25000, 0, 5000, key="ded_80d")
            deductions['80d_parents'] = st.number_input("Parents Insurance", 0, 50000, 0, 5000, key="ded_parents")
            deductions['24b'] = st.number_input("Home Loan Interest", 0, 200000, 0, 10000, key="ded_24b")
            deductions['hra'] = st.number_input("HRA Exemption", 0, 500000, 0, 10000, key="ded_hra")
            
            if st.button("Compare Regimes", type="primary", use_container_width=True, key="compare_tax_btn"):
                comparison = tax_optimizer.compare_regimes(annual_income, deductions)
                st.session_state.tax_comparison = comparison
        
        with col2:
            if 'tax_comparison' in st.session_state:
                comp = st.session_state.tax_comparison
                
                st.markdown("#### 📊 Tax Comparison Results")
                
                # Metrics
                col_new, col_old = st.columns(2)
                with col_new:
                    st.metric("New Regime Tax", f"₹{comp['new_regime']['total_tax']:,.0f}",
                             help="Simplified regime with lower rates, no deductions")
                    st.caption(f"Effective Rate: {comp['new_regime']['effective_rate']:.1f}%")
                
                with col_old:
                    st.metric("Old Regime Tax", f"₹{comp['old_regime']['total_tax']:,.0f}",
                             help="Traditional regime with deductions")
                    st.caption(f"Effective Rate: {comp['old_regime']['effective_rate']:.1f}%")
                
                # Recommendation
                if comp['better_regime'] == 'Old Regime':
                    st.success(f"✅ {comp['recommendation']}")
                else:
                    st.info(f"💡 {comp['recommendation']}")
                
                # Visualization
                fig = go.Figure(data=[
                    go.Bar(name='New Regime', x=['Tax Amount'], y=[comp['new_regime']['total_tax']],
                          marker_color='#0066FF'),
                    go.Bar(name='Old Regime', x=['Tax Amount'], y=[comp['old_regime']['total_tax']],
                          marker_color='#00D9A3')
                ])
                fig.update_layout(
                    title="Tax Comparison",
                    yaxis_title="Tax Amount (₹)",
                    paper_bgcolor='#151B3D',
                    plot_bgcolor='#0A0E27',
                    font=dict(color='white'),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tax_tab2:
        st.markdown("#### Section 80C Investment Planner")
        st.caption("Maximize your tax savings up to ₹1.5 Lakh")
        
        current_80c = st.number_input(
            "Current 80C Investments (₹)",
            0, 150000, 0, 10000,
            key="current_80c_input"
        )
        
        suggestions = tax_optimizer.suggest_investments_for_80c(current_80c)
        
        if suggestions['status'] == 'optimized':
            st.success(suggestions['message'])
        else:
            st.warning(suggestions['message'])
            st.info(f"💰 Potential Tax Savings: ₹{suggestions['potential_savings']:,.0f}")
            
            st.markdown("#### 📌 Recommended Investment Options")
            
            for suggestion in suggestions['suggestions']:
                priority_color = {
                    'High': '#10B981',
                    'Medium': '#FFB800',
                    'Low': '#A0AEC0'
                }.get(suggestion['priority'], '#A0AEC0')
                
                with st.expander(f"{suggestion['option']} - {suggestion['priority']} Priority"):
                    st.markdown(f"""
                    <div style='background: rgba(21, 27, 61, 0.6); padding: 1rem; border-radius: 10px;'>
                        <strong style='color: {priority_color};'>Suggested Amount: ₹{suggestion['amount']:,.0f}</strong>
                        <br/><br/>
                        <span style='color: #00D9A3;'>✅ Benefit:</span> {suggestion['benefit']}
                        <br/>
                        <span style='color: #FFB800;'>🔒 Lock-in:</span> {suggestion['lock_in']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tax_tab3:
        st.markdown("#### Home Loan Tax Benefits Calculator")
        st.caption("Calculate deductions under Section 24B and 80C")
        
        col1, col2 = st.columns(2)
        with col1:
            interest_paid = st.number_input(
                "Annual Interest Paid (₹)",
                0, 500000, 0, 10000,
                key="home_loan_interest"
            )
            principal_paid = st.number_input(
                "Annual Principal Repaid (₹)",
                0, 500000, 0, 10000,
                key="home_loan_principal"
            )
        
        with col2:
            if st.button("Calculate Benefits", type="primary", key="calc_home_loan_btn"):
                benefits = tax_optimizer.calculate_home_loan_benefit(interest_paid, principal_paid)
                
                st.success(f"**Total Tax Benefit:** ₹{benefits['total_benefit']:,.0f}")
                st.info(f"**Tax Saved (30% bracket):** ₹{benefits['tax_saved']:,.0f}")
                
                st.markdown("**📊 Breakdown:**")
                st.write(f"- Interest Deduction (Sec 24B): ₹{benefits['interest_deduction']:,.0f}")
                st.write(f"- Principal Deduction (Sec 80C): ₹{benefits['principal_deduction']:,.0f}")
                st.caption(f"ℹ️ {benefits['note']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== GOAL PLANNER PAGE ====================
elif st.session_state.current_page == "Goal":
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    st.markdown("### 🎯 Goal-Based Financial Planning")
    st.caption("Plan for life's important milestones")
    
    goal_type = st.selectbox(
        "Select Your Financial Goal",
        ["Retirement", "Child Education", "Home Purchase", "Emergency Fund", "Wedding", "Vacation"],
        key="goal_type_select"
    )
    
    st.markdown("---")
    
    if goal_type == "Retirement":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Retirement Planning")
            current_age = st.number_input("Current Age", 20, 60, 30, key="ret_current_age")
            retirement_age = st.number_input("Retirement Age", 40, 75, 60, key="ret_retirement_age")
            monthly_expenses = st.number_input("Monthly Expenses (₹)", 10000, 500000, 50000, 5000, key="ret_expenses")
            existing_corpus = st.number_input("Existing Retirement Fund (₹)", 0, 10000000, 0, 100000, key="ret_corpus")
            
            if st.button("Calculate Retirement Plan", type="primary", use_container_width=True, key="calc_retirement_btn"):
                result = goal_planner.retirement_planning(
                    current_age, retirement_age, monthly_expenses, 85, existing_corpus
                )
                st.session_state.retirement_plan = result
        
        with col2:
            if 'retirement_plan' in st.session_state:
                plan = st.session_state.retirement_plan
                
                st.markdown("#### 🏖️ Your Retirement Plan")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Required Corpus", f"₹{plan['required_corpus']/10000000:.2f}Cr")
                m2.metric("Monthly SIP Needed", f"₹{plan['required_monthly_sip']:,.0f}")
                m3.metric("Years to Retire", plan['years_to_retirement'])
                
                st.info(f"💡 {plan['recommendation']}")
                
                with st.expander("📋 Detailed Breakdown", expanded=True):
                    st.markdown(f"""
                    - **Current Age:** {plan['current_age']} years
                    - **Retirement Age:** {plan['retirement_age']} years
                    - **Current Monthly Expenses:** ₹{plan['current_monthly_expenses']:,.0f}
                    - **Future Monthly Expenses:** ₹{plan['future_monthly_expenses']:,.0f}
                    - **Retirement Duration:** {plan['retirement_duration']} years
                    - **Inflation Rate:** {plan['inflation_rate']}%
                    - **Shortfall to Cover:** ₹{plan['shortfall']:,.0f}
                    """)
    
    elif goal_type == "Child Education":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Child Education Planning")
            child_age = st.number_input("Child's Current Age", 0, 18, 5, key="edu_child_age")
            edu_start_age = st.number_input("Education Start Age", 15, 25, 18, key="edu_start_age")
            course_cost = st.number_input("Course Cost Today (₹)", 100000, 10000000, 2000000, 100000, key="edu_cost")
            edu_savings = st.number_input("Existing Education Fund (₹)", 0, 5000000, 0, 50000, key="edu_savings")
            
            if st.button("Calculate Education Plan", type="primary", use_container_width=True, key="calc_edu_btn"):
                result = goal_planner.child_education_planning(
                    child_age, edu_start_age, course_cost, edu_savings
                )
                st.session_state.education_plan = result
        
        with col2:
            if 'education_plan' in st.session_state:
                plan = st.session_state.education_plan
                
                if 'error' not in plan:
                    st.markdown("#### 🎓 Education Funding Plan")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Future Cost", f"₹{plan['future_course_cost']/100000:.2f}L")
                    m2.metric("Required SIP", f"₹{plan['required_monthly_sip']:,.0f}/mo")
                    m3.metric("Years to Goal", plan['years_to_goal'])
                    
                    st.success(f"💡 {plan['recommendation']}")
                    
                    with st.expander("📋 Plan Details"):
                        st.write(f"- Course Cost Today: ₹{plan['course_cost_today']:,.0f}")
                        st.write(f"- Education Inflation: {plan['education_inflation_rate']}%")
                        st.write(f"- Alternative: Invest ₹{plan['required_lumpsum']:,.0f} today")
                else:
                    st.error(plan['error'])
    
    elif goal_type == "Emergency Fund":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Emergency Fund Planning")
            monthly_exp = st.number_input("Monthly Expenses (₹)", 10000, 200000, 50000, 5000, key="emerg_expenses")
            coverage = st.slider("Months of Coverage", 3, 12, 6, key="emerg_coverage")
            existing_fund = st.number_input("Existing Emergency Fund (₹)", 0, 1000000, 0, 10000, key="emerg_fund")
            
            if st.button("Calculate Emergency Fund", type="primary", use_container_width=True, key="calc_emerg_btn"):
                result = goal_planner.emergency_fund_planning(monthly_exp, coverage, existing_fund)
                st.session_state.emergency_plan = result
        
        with col2:
            if 'emergency_plan' in st.session_state:
                plan = st.session_state.emergency_plan
                
                st.markdown("#### 🛡️ Emergency Fund Plan")
                
                status_color = "success" if plan['status'] == 'Adequate' else "warning"
                getattr(st, status_color)(f"**Status:** {plan['status']}")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Required Fund", f"₹{plan['required_corpus']:,.0f}")
                m2.metric("Monthly Saving", f"₹{plan['required_monthly_saving']:,.0f}")
                m3.metric("Months to Build", plan['months_to_build'])
                
                st.info(f"💡 {plan['recommendation']}")
                
                st.markdown("**💰 Recommended Allocation:**")
                for option, details in plan['allocation'].items():
                    st.markdown(f"""
                    <div style='background: rgba(21, 27, 61, 0.6); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;'>
                        <strong style='color: #00D9A3;'>{option}</strong>: ₹{details['amount']:,.0f} ({details['percent']}%)
                        <br/>
                        <span style='color: #A0AEC0; font-size: 0.9em;'>Liquidity: {details['liquidity']}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== AI CHAT PAGE ====================
else:  # AI Chat
    st.markdown('<div class="slide-up">', unsafe_allow_html=True)
    st.markdown("### 💬 AI Investment Advisor")
    st.caption("Chat with CodeNCash AI - Your personal investment assistant powered by LLaMA 3.3 70B")
    
    # Show portfolio context if available
    if st.session_state.portfolio_generated:
        with st.expander("📊 Current Portfolio Context", expanded=False):
            portfolio = st.session_state.current_portfolio
            st.markdown(f"""
            **Your Portfolio Summary:**
            - 💰 Capital: ₹{portfolio['total_investment']:,}
            - 📅 Monthly SIP: ₹{portfolio['monthly_sip']:,}
            - 🎯 Risk: {portfolio['risk_level']}
            - 📈 5Y Projection: ₹{portfolio['projected_returns']['5_year']['total_value']:,.0f}
            
            *The AI has full context of your portfolio and can answer specific questions about it.*
            """)
    
    st.markdown("---")
    
    # Suggested questions based on context
    if len(st.session_state.messages) == 0:
        st.markdown("**💡 Quick Start Questions:**")
        
        if st.session_state.portfolio_generated:
            suggestions = [
                ("📊", "Analyze my current portfolio"),
                ("🎯", "How can I improve my portfolio?"),
                ("💰", "Should I increase my SIP amount?"),
                ("📈", "What are the risks in my portfolio?"),
                ("💸", "Tax-saving opportunities for me?"),
                ("🔄", "When should I rebalance?")
            ]
        else:
            suggestions = [
                ("🎯", "What are the best mutual funds for beginners?"),
                ("💰", "How does SIP investment work in India?"),
                ("📊", "Difference between debt and equity funds"),
                ("🏆", "Best retirement planning strategy"),
                ("💸", "Tax saving investment options in India"),
                ("📈", "How to build a diversified portfolio")
            ]
        
        # Create suggestion buttons in a grid
        cols = st.columns(3)
        for idx, (icon, text) in enumerate(suggestions):
            with cols[idx % 3]:
                if st.button(f"{icon} {text}", key=f"suggest_{idx}", use_container_width=True):
                    # Add to messages
                    st.session_state.messages.append({"role": "user", "content": text})
                    
                    # Get response with context
                    with st.spinner("🤔 Thinking..."):
                        response = chat_handler.get_response(text, st.session_state.chat_context)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        st.markdown("---")
    
    # Chat container with enhanced styling
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        if len(st.session_state.messages) == 0:
            st.markdown("""
            <div style='text-align: center; padding: 3rem 2rem; color: #A0AEC0;'>
                <h3 style='color: #00D9A3;'>👋 Welcome to CodeNCash AI!</h3>
                <p>I'm your personal investment advisor. Ask me anything about:</p>
                <p>💰 Investments • 📊 Portfolio Strategy • 💸 Tax Planning • 🎯 Financial Goals</p>
                <br/>
                <p style='font-size: 0.9em;'>Start by typing a question below or click a suggested question above.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                    st.markdown(message["content"])
    
    # Chat input with enhanced placeholder
    placeholder = "💬 Ask me about investments, your portfolio, tax planning, or financial goals..."
    
    if prompt := st.chat_input(placeholder):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message immediately
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤔 Analyzing your query..."):
                    # Build enhanced context
                    context = st.session_state.chat_context
                    
                    # Add recent conversation context
                    if len(st.session_state.messages) > 2:
                        recent_context = "\n\nRecent conversation:\n"
                        for msg in st.session_state.messages[-4:-1]:  # Last 2 exchanges
                            role = "User" if msg["role"] == "user" else "Assistant"
                            recent_context += f"{role}: {msg['content'][:100]}...\n"
                        context += recent_context
                    
                    response = chat_handler.get_response(prompt, context)
                
                st.markdown(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Enhanced action buttons
    st.markdown("---")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔄 Clear Chat History", use_container_width=True, key="clear_chat_btn"):
            st.session_state.messages = []
            st.success("Chat cleared!")
            time.sleep(0.5)
            st.rerun()
    
    with action_col2:
        if st.session_state.portfolio_generated:
            if st.button("📊 View My Portfolio", use_container_width=True, key="view_portfolio_btn"):
                st.session_state.current_page = "Portfolio"
                st.rerun()
    
    with action_col3:
        if len(st.session_state.messages) > 0:
            # Export chat history
            chat_export = "\n\n".join([
                f"{'You' if msg['role'] == 'user' else 'CodeNCash AI'}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.download_button(
                "💾 Export Chat",
                chat_export,
                f"CodeNCash_Chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True,
                key="export_chat_btn"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
footer_cols = st.columns([2, 2, 1])

with footer_cols[0]:
    st.markdown("**💼 CodeNCash** - AI Investment Advisor")
    st.caption("Powered by LLaMA 3.3 70B • Live Market Data")

with footer_cols[1]:
    st.markdown("⚠️ **Disclaimer**")
    st.caption("For educational purposes. Consult certified financial advisors for personalized advice.")

with footer_cols[2]:
    st.markdown(f"**🕒 {datetime.now().strftime('%d %b %Y')}**")
    st.caption(f"{datetime.now().strftime('%I:%M %p')}")

st.markdown('</div>', unsafe_allow_html=True)

# Add custom JavaScript for smooth scrolling (optional)
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
});
</script>
""", unsafe_allow_html=True)
        