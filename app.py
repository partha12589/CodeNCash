import streamlit as st
import pandas as pd
from utils.portfolio import PortfolioGenerator
from utils.enhanced_chat_handler import EnhancedChatHandler
from utils.market_data import IndianMarketData
from utils.live_market_data import LiveMarketData, POPULAR_SCHEME_CODES
from utils.visualizations import PortfolioVisualizations
from utils.tax_optimizer import TaxOptimizer
from utils.sip_calculator import SIPCalculator
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
    st.session_state.current_page = "Portfolio Generator"

# Initialize handlers
portfolio_gen = PortfolioGenerator()
chat_handler = EnhancedChatHandler()
market_data = IndianMarketData()
live_market = LiveMarketData()
visualizer = PortfolioVisualizations()
tax_optimizer = TaxOptimizer()
sip_calculator = SIPCalculator()
goal_planner = GoalBasedPlanner()

# Header
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

# Navigation
st.markdown("---")
nav_cols = st.columns(5)
pages = ["💼 Portfolio", "💹 SIP Calculator", "💸 Tax Optimizer", "🎯 Goal Planner", "💬 AI Chat"]

for idx, (col, page) in enumerate(zip(nav_cols, pages)):
    with col:
        if st.button(page, use_container_width=True, 
                    type="primary" if st.session_state.current_page == page.split()[1] else "secondary"):
            st.session_state.current_page = page.split()[1]
            st.rerun()

st.markdown("---")

# ==================== PORTFOLIO GENERATOR PAGE ====================
if st.session_state.current_page == "Portfolio":
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("📊 Investment Profile")
        
        # Investment inputs
        capital = st.number_input("💰 Initial Capital (₹)", min_value=10000, value=100000, step=10000)
        monthly_investment = st.number_input("📅 Monthly SIP (₹)", min_value=0, value=5000, step=1000)
        
        st.markdown("---")
        
        risk_appetite = st.select_slider("🎯 Risk Profile", 
                                         options=['Low', 'Medium', 'High'], value='Medium')
        
        risk_info = {
            'Low': ('🟢', 'Safe & Stable', '8-10%'),
            'Medium': ('🟡', 'Balanced Growth', '10-14%'),
            'High': ('🔴', 'Maximum Growth', '14-18%')
        }
        info = risk_info[risk_appetite]
        st.info(f"{info[0]} **{risk_appetite} Risk**\n\n📈 Expected: {info[2]}\n\n💡 {info[1]}")
        
        st.markdown("---")
        
        st.markdown("### Asset Preferences")
        col_a, col_b = st.columns(2)
        with col_a:
            mutual_funds = st.checkbox("💰 Mutual Funds", True)
            stocks = st.checkbox("📈 Stocks", True)
        with col_b:
            debt_funds = st.checkbox("🏦 Debt", True)
            bonds = st.checkbox("📋 Bonds", False)
        
        if st.button("🚀 Generate Portfolio", type="primary", use_container_width=True):
            preferences = {
                "mutual_funds": mutual_funds, "stocks": stocks,
                "debt_funds": debt_funds, "bonds": bonds
            }
            
            if any(preferences.values()):
                with st.spinner("Generating portfolio..."):
                    portfolio = portfolio_gen.generate_portfolio(
                        capital, monthly_investment, risk_appetite, preferences
                    )
                    st.session_state.current_portfolio = portfolio
                    st.session_state.portfolio_generated = True
                st.success("✅ Portfolio Generated!")
                st.balloons()
            else:
                st.error("Select at least one asset class")
    
    with col2:
        st.subheader("📈 Your Portfolio")
        
        if st.session_state.portfolio_generated:
            portfolio = st.session_state.current_portfolio
            
            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 Capital", f"₹{portfolio['total_investment']:,}")
            m2.metric("📅 Monthly SIP", f"₹{portfolio['monthly_sip']:,}")
            m3.metric("🎯 Risk", portfolio['risk_level'])
            one_yr = portfolio['projected_returns']['1_year']['gains']
            m4.metric("📈 1Y Return", f"{(one_yr/portfolio['total_investment']*100):.1f}%")
            
            st.markdown("---")
            
            # PDF Download
            from utils.pdf_generator import generate_portfolio_pdf
            try:
                pdf_data = generate_portfolio_pdf(portfolio)
                st.download_button("📄 Download Report", pdf_data,
                                  f"CodeNCash_{datetime.now().strftime('%Y%m%d')}.pdf",
                                  "application/pdf", use_container_width=True)
            except:
                pass
            
            # Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Allocation", "📈 Returns", "💼 Assets"])
            
            with tab1:
                fig_pie = visualizer.create_allocation_pie_chart(portfolio['allocation'], "Asset Allocation")
                st.plotly_chart(fig_pie, use_container_width=True)
                
                if portfolio['recommendations']:
                    fig_dist = visualizer.create_diversification_chart(portfolio['recommendations'])
                    st.plotly_chart(fig_dist, use_container_width=True)
            
            with tab2:
                fig_returns = visualizer.create_returns_chart(
                    portfolio['projected_returns'], portfolio['total_investment'], portfolio['monthly_sip']
                )
                st.plotly_chart(fig_returns, use_container_width=True)
                
                fig_gains = visualizer.create_gains_bar_chart(portfolio['projected_returns'])
                st.plotly_chart(fig_gains, use_container_width=True)
            
            with tab3:
                if 'stocks' in portfolio['recommendations']:
                    with st.expander(f"📈 Stocks (₹{portfolio['recommendations']['stocks']['amount']:,.0f})", True):
                        for stock in portfolio['recommendations']['stocks']['list'][:5]:
                            cols = st.columns([3, 2])
                            cols[0].markdown(f"**{stock['symbol']}** - {stock['name'][:25]}")
                            cols[1].caption(stock['sector'])
                            st.markdown("---")
                
                if 'mutual_funds' in portfolio['recommendations']:
                    with st.expander(f"💰 Mutual Funds (₹{portfolio['recommendations']['mutual_funds']['amount']:,.0f})"):
                        for mf in portfolio['recommendations']['mutual_funds']['list'][:3]:
                            st.markdown(f"**{mf['name']}**")
                            st.caption(f"{mf['category']} | Returns: {mf['returns_3y']}")
                            st.markdown("---")
        else:
            st.info("👈 Configure your profile and generate portfolio")

# ==================== SIP CALCULATOR PAGE ====================
elif st.session_state.current_page == "SIP":
    st.subheader("💹 Advanced SIP Calculator")
    
    calc_tab1, calc_tab2, calc_tab3 = st.tabs(["📊 Basic SIP", "🎯 Goal-Based", "📈 Scenarios"])
    
    with calc_tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Calculator")
            sip_amount = st.number_input("Monthly SIP (₹)", 1000, 100000, 10000, 1000)
            years = st.slider("Investment Period (Years)", 1, 30, 10)
            returns = st.slider("Expected Returns (%)", 5, 20, 12)
            step_up = st.slider("Annual Step-up (%)", 0, 20, 0)
            
            if st.button("Calculate SIP", type="primary", use_container_width=True):
                result = sip_calculator.calculate_sip(sip_amount, years, returns, step_up)
                
                st.success(f"**Final Value:** ₹{result['final_value']:,.0f}")
                st.info(f"**Total Invested:** ₹{result['total_invested']:,.0f}")
                st.success(f"**Total Gains:** ₹{result['total_gains']:,.0f}")
                st.metric("ROI", f"{result['absolute_return']:.1f}%")
        
        with col2:
            if 'result' in locals():
                st.markdown("#### Growth Visualization")
                
                # Create growth chart
                df = pd.DataFrame(result['monthly_data'])
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['month'], y=df['invested'], 
                                        name='Invested', mode='lines', fill='tozeroy'))
                fig.add_trace(go.Scatter(x=df['month'], y=df['value'],
                                        name='Value', mode='lines', fill='tonexty'))
                fig.update_layout(title="SIP Growth Over Time", xaxis_title="Months",
                                 yaxis_title="Amount (₹)", height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Yearly summary
                st.markdown("#### Year-wise Summary")
                yearly_df = pd.DataFrame(result['yearly_summary'])
                st.dataframe(yearly_df, use_container_width=True)
    
    with calc_tab2:
        st.markdown("#### Goal-Based SIP Calculator")
        
        col1, col2 = st.columns(2)
        with col1:
            target = st.number_input("Target Amount (₹)", 100000, 10000000, 1000000, 100000)
            goal_years = st.slider("Time to Goal (Years)", 1, 30, 10)
            goal_returns = st.slider("Expected Returns (%)", 5, 20, 12)
        
        with col2:
            if st.button("Calculate Required SIP", type="primary"):
                goal_result = sip_calculator.calculate_goal_based_sip(target, goal_years, goal_returns)
                
                st.success(f"### ₹{goal_result['required_monthly_sip']:,.0f}/month")
                st.info(f"**Total Investment:** ₹{goal_result['total_invested']:,.0f}")
                st.caption(f"To reach ₹{target:,.0f} in {goal_years} years")
    
    with calc_tab3:
        st.markdown("#### Compare Scenarios")
        
        scenario_sip = st.number_input("Monthly SIP for Comparison (₹)", 1000, 100000, 10000, 1000)
        scenario_years = st.slider("Years for Comparison", 1, 30, 10)
        
        if st.button("Compare Scenarios", type="primary"):
            scenarios = sip_calculator.compare_scenarios(scenario_sip, scenario_years)
            
            # Create comparison chart
            scenario_df = pd.DataFrame([
                {'Scenario': k, 'Value': v['final_value'], 'Returns': v['return_rate']}
                for k, v in scenarios.items()
            ])
            
            fig = px.bar(scenario_df, x='Scenario', y='Value', color='Returns',
                        title="Scenario Comparison", text='Value')
            fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Details table
            st.dataframe(pd.DataFrame(scenarios).T, use_container_width=True)

# ==================== TAX OPTIMIZER PAGE ====================
elif st.session_state.current_page == "Tax":
    st.subheader("💸 Tax Optimizer")
    
    tax_tab1, tax_tab2, tax_tab3 = st.tabs(["🧮 Calculator", "💡 80C Planner", "🏠 Home Loan"])
    
    with tax_tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Your Income")
            annual_income = st.number_input("Annual Gross Income (₹)", 0, 10000000, 1000000, 50000)
            
            st.markdown("#### Deductions (Old Regime)")
            deductions = {}
            deductions['80c'] = st.number_input("Section 80C (max ₹1.5L)", 0, 150000, 0, 10000)
            deductions['80ccd_1b'] = st.number_input("NPS - 80CCD(1B) (max ₹50k)", 0, 50000, 0, 10000)
            deductions['80d'] = st.number_input("Health Insurance - 80D", 0, 25000, 0, 5000)
            deductions['80d_parents'] = st.number_input("Parents Insurance (Sr. Citizen)", 0, 50000, 0, 5000)
            deductions['24b'] = st.number_input("Home Loan Interest", 0, 200000, 0, 10000)
            deductions['hra'] = st.number_input("HRA Exemption", 0, 500000, 0, 10000)
            
            if st.button("Compare Tax Regimes", type="primary", use_container_width=True):
                comparison = tax_optimizer.compare_regimes(annual_income, deductions)
                
                st.session_state.tax_comparison = comparison
        
        with col2:
            if 'tax_comparison' in st.session_state:
                comp = st.session_state.tax_comparison
                
                st.markdown("#### Tax Comparison")
                
                # Metrics
                col_new, col_old = st.columns(2)
                with col_new:
                    st.metric("New Regime Tax", f"₹{comp['new_regime']['total_tax']:,.0f}")
                    st.caption(f"Effective Rate: {comp['new_regime']['effective_rate']:.1f}%")
                
                with col_old:
                    st.metric("Old Regime Tax", f"₹{comp['old_regime']['total_tax']:,.0f}")
                    st.caption(f"Effective Rate: {comp['old_regime']['effective_rate']:.1f}%")
                
                # Recommendation
                if comp['better_regime'] == 'Old Regime':
                    st.success(f"✅ {comp['recommendation']}")
                else:
                    st.info(f"💡 {comp['recommendation']}")
                
                # Visualization
                fig = go.Figure(data=[
                    go.Bar(name='New Regime', x=['Tax'], y=[comp['new_regime']['total_tax']]),
                    go.Bar(name='Old Regime', x=['Tax'], y=[comp['old_regime']['total_tax']])
                ])
                fig.update_layout(title="Tax Comparison", yaxis_title="Tax Amount (₹)")
                st.plotly_chart(fig, use_container_width=True)
    
    with tax_tab2:
        st.markdown("#### Section 80C Investment Planner")
        
        current_80c = st.number_input("Current 80C Investments (₹)", 0, 150000, 0, 10000)
        
        suggestions = tax_optimizer.suggest_investments_for_80c(current_80c)
        
        if suggestions['status'] == 'optimized':
            st.success(suggestions['message'])
        else:
            st.warning(suggestions['message'])
            st.info(f"Potential Tax Savings: ₹{suggestions['potential_savings']:,.0f}")
            
            st.markdown("#### Recommended Options")
            for suggestion in suggestions['suggestions']:
                with st.expander(f"{suggestion['option']} - Priority: {suggestion['priority']}"):
                    st.write(f"**Suggested Amount:** ₹{suggestion['amount']:,.0f}")
                    st.write(f"**Benefit:** {suggestion['benefit']}")
                    st.write(f"**Lock-in Period:** {suggestion['lock_in']}")
    
    with tax_tab3:
        st.markdown("#### Home Loan Tax Benefits")
        
        col1, col2 = st.columns(2)
        with col1:
            interest_paid = st.number_input("Interest Paid (Annual)", 0, 500000, 0, 10000)
            principal_paid = st.number_input("Principal Repaid (Annual)", 0, 500000, 0, 10000)
        
        with col2:
            if st.button("Calculate Benefits", type="primary"):
                benefits = tax_optimizer.calculate_home_loan_benefit(interest_paid, principal_paid)
                
                st.success(f"**Total Tax Benefit:** ₹{benefits['total_benefit']:,.0f}")
                st.info(f"**Tax Saved:** ₹{benefits['tax_saved']:,.0f}")
                
                st.markdown("**Breakdown:**")
                st.write(f"- Interest Deduction (24B): ₹{benefits['interest_deduction']:,.0f}")
                st.write(f"- Principal Deduction (80C): ₹{benefits['principal_deduction']:,.0f}")
                st.caption(benefits['note'])

# ==================== GOAL PLANNER PAGE ====================
elif st.session_state.current_page == "Goal":
    st.subheader("🎯 Goal-Based Financial Planning")
    
    goal_type = st.selectbox("Select Goal", 
                            ["Retirement", "Child Education", "Home Purchase", 
                             "Emergency Fund", "Wedding", "Vacation"])
    
    st.markdown("---")
    
    if goal_type == "Retirement":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            current_age = st.number_input("Current Age", 20, 60, 30)
            retirement_age = st.number_input("Retirement Age", 40, 75, 60)
            monthly_expenses = st.number_input("Current Monthly Expenses (₹)", 10000, 500000, 50000)
            existing_corpus = st.number_input("Existing Retirement Fund (₹)", 0, 10000000, 0)
            
            if st.button("Plan Retirement", type="primary", use_container_width=True):
                result = goal_planner.retirement_planning(
                    current_age, retirement_age, monthly_expenses, 85, existing_corpus
                )
                st.session_state.retirement_plan = result
        
        with col2:
            if 'retirement_plan' in st.session_state:
                plan = st.session_state.retirement_plan
                
                st.markdown("#### Retirement Plan")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Required Corpus", f"₹{plan['required_corpus']/10000000:.2f}Cr")
                m2.metric("Monthly SIP", f"₹{plan['required_monthly_sip']:,.0f}")
                m3.metric("Years to Go", plan['years_to_retirement'])
                
                st.info(plan['recommendation'])
                
                # Breakdown
                st.markdown("**Details:**")
                st.write(f"- Current Monthly Expenses: ₹{plan['current_monthly_expenses']:,.0f}")
                st.write(f"- Future Monthly Expenses: ₹{plan['future_monthly_expenses']:,.0f}")
                st.write(f"- Retirement Duration: {plan['retirement_duration']} years")
                st.write(f"- Shortfall to Cover: ₹{plan['shortfall']:,.0f}")
    
    elif goal_type == "Child Education":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            child_age = st.number_input("Child's Current Age", 0, 18, 5)
            edu_start_age = st.number_input("Education Start Age", 15, 25, 18)
            course_cost = st.number_input("Course Cost Today (₹)", 100000, 10000000, 2000000)
            edu_savings = st.number_input("Existing Education Fund (₹)", 0, 5000000, 0)
            
            if st.button("Plan Education", type="primary", use_container_width=True):
                result = goal_planner.child_education_planning(
                    child_age, edu_start_age, course_cost, edu_savings
                )
                st.session_state.education_plan = result
        
        with col2:
            if 'education_plan' in st.session_state:
                plan = st.session_state.education_plan
                
                if 'error' not in plan:
                    st.markdown("#### Education Plan")
                    
                    m1, m2 = st.columns(2)
                    m1.metric("Future Cost", f"₹{plan['future_course_cost']/100000:.2f}L")
                    m2.metric("Required SIP", f"₹{plan['required_monthly_sip']:,.0f}")
                    
                    st.info(plan['recommendation'])
                    
                    st.write(f"**Years to Goal:** {plan['years_to_goal']}")
                    st.write(f"**Education Inflation:** {plan['education_inflation_rate']}%")
                    st.write(f"**Alternative: Invest ₹{plan['required_lumpsum']:,.0f} today**")
    
    elif goal_type == "Emergency Fund":
        col1, col2 = st.columns([1, 2])
        
        with col1:
            monthly_exp = st.number_input("Monthly Expenses (₹)", 10000, 200000, 50000)
            coverage = st.slider("Months of Coverage", 3, 12, 6)
            existing_fund = st.number_input("Existing Emergency Fund (₹)", 0, 1000000, 0)
            
            if st.button("Plan Emergency Fund", type="primary", use_container_width=True):
                result = goal_planner.emergency_fund_planning(monthly_exp, coverage, existing_fund)
                st.session_state.emergency_plan = result
        
        with col2:
            if 'emergency_plan' in st.session_state:
                plan = st.session_state.emergency_plan
                
                st.markdown("#### Emergency Fund Plan")
                
                status_color = "success" if plan['status'] == 'Adequate' else "warning"
                getattr(st, status_color)(f"Status: {plan['status']}")
                
                m1, m2 = st.columns(2)
                m1.metric("Required Fund", f"₹{plan['required_corpus']:,.0f}")
                m2.metric("Monthly Saving", f"₹{plan['required_monthly_saving']:,.0f}")
                
                st.info(plan['recommendation'])
                
                st.markdown("**Recommended Allocation:**")
                for option, details in plan['allocation'].items():
                    st.write(f"- {option}: ₹{details['amount']:,.0f} ({details['percent']}%)")
                    st.caption(f"Liquidity: {details['liquidity']}")

# ==================== AI CHAT PAGE ====================
else:  # AI Chat
    st.subheader("💬 AI Investment Advisor")
    
    # File upload section
    with st.expander("📎 Upload Files/Images", expanded=False):
        uploaded_files = st.file_uploader(
            "Upload portfolio files (CSV, Excel, PDF, TXT)",
            type=['csv', 'xlsx', 'xls', 'pdf', 'txt'],
            accept_multiple_files=True
        )
        
        uploaded_images = st.file_uploader(
            "Upload investment screenshots/documents",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )
        
        if uploaded_files or uploaded_images:
            st.success(f"✅ {len(uploaded_files or [])} files + {len(uploaded_images or [])} images uploaded")
    
    # Chat container
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about investments, upload files for analysis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤔 Analyzing..."):
                    context = ""
                    if st.session_state.portfolio_generated:
                        portfolio = st.session_state.current_portfolio
                        context = f"User portfolio: {portfolio['risk_level']} risk, ₹{portfolio['total_investment']} capital"
                    
                    # Get response with file context
                    response = chat_handler.get_response(
                        prompt, context,
                        files=uploaded_files if 'uploaded_files' in locals() else None,
                        images=uploaded_images if 'uploaded_images' in locals() else None
                    )
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Clear chat button
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        chat_handler.clear_history()
        st.rerun()

# Footer
st.markdown("---")
footer_cols = st.columns(3)
footer_cols[0].caption("💼 **CodeNCash** - AI Investment Advisor")
footer_cols[1].caption("⚠️ For educational purposes. Consult certified advisors.")
footer_cols[2].caption(f"🕒 {datetime.now().strftime('%d %b %Y | %H:%M')}")