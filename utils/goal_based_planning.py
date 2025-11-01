"""
Goal-Based Financial Planning Module
"""

from datetime import datetime
from dateutil.relativedelta import relativedelta

class GoalBasedPlanner:
    """Calculate investment requirements for specific life goals"""
    
    def __init__(self):
        self.inflation_rate = 6  # Default inflation rate for India
        self.education_inflation = 10  # Higher for education
        self.healthcare_inflation = 12  # Higher for healthcare
    
    def retirement_planning(self, current_age, retirement_age, monthly_expenses, 
                           life_expectancy=85, existing_corpus=0, inflation_rate=None):
        """
        Calculate retirement corpus requirement
        Args:
            current_age: Current age
            retirement_age: Planned retirement age
            monthly_expenses: Current monthly expenses
            life_expectancy: Expected life expectancy
            existing_corpus: Current retirement savings
            inflation_rate: Custom inflation rate (default 6%)
        Returns:
            Dict with retirement planning details
        """
        inflation = inflation_rate or self.inflation_rate
        years_to_retirement = retirement_age - current_age
        retirement_years = life_expectancy - retirement_age
        
        # Calculate future monthly expenses at retirement
        future_monthly_expenses = monthly_expenses * ((1 + inflation / 100) ** years_to_retirement)
        
        # Calculate required corpus (using annuity formula)
        # Assuming 8% post-retirement returns
        post_retirement_return = 8
        real_return = ((1 + post_retirement_return / 100) / (1 + inflation / 100) - 1) * 100
        monthly_real_return = real_return / 100 / 12
        
        if monthly_real_return > 0:
            required_corpus = future_monthly_expenses * (
                (1 - (1 + monthly_real_return) ** (-retirement_years * 12)) / monthly_real_return
            )
        else:
            required_corpus = future_monthly_expenses * retirement_years * 12
        
        # Calculate shortfall
        shortfall = max(0, required_corpus - existing_corpus)
        
        # Calculate required monthly SIP
        if years_to_retirement > 0:
            # Assuming 12% returns during accumulation phase
            monthly_rate = 12 / 100 / 12
            total_months = years_to_retirement * 12
            
            if monthly_rate > 0 and shortfall > 0:
                required_sip = shortfall * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
            else:
                required_sip = shortfall / total_months if total_months > 0 else 0
        else:
            required_sip = 0
        
        return {
            'goal': 'Retirement Planning',
            'current_age': current_age,
            'retirement_age': retirement_age,
            'years_to_retirement': years_to_retirement,
            'life_expectancy': life_expectancy,
            'retirement_duration': retirement_years,
            'current_monthly_expenses': monthly_expenses,
            'future_monthly_expenses': round(future_monthly_expenses, 2),
            'required_corpus': round(required_corpus, 2),
            'existing_corpus': existing_corpus,
            'shortfall': round(shortfall, 2),
            'required_monthly_sip': round(required_sip, 2),
            'inflation_rate': inflation,
            'recommendation': self._get_retirement_recommendation(current_age, retirement_age, required_sip)
        }
    
    def child_education_planning(self, child_age, education_start_age, 
                                course_cost_today, existing_savings=0):
        """
        Calculate corpus needed for child's education
        Args:
            child_age: Current age of child
            education_start_age: Age when education starts (e.g., 18 for college)
            course_cost_today: Current cost of education
            existing_savings: Current education savings
        Returns:
            Dict with education planning details
        """
        years_to_goal = education_start_age - child_age
        
        if years_to_goal <= 0:
            return {
                'error': 'Education start age must be greater than current age',
                'goal': 'Child Education'
            }
        
        # Future cost with education inflation
        future_cost = course_cost_today * ((1 + self.education_inflation / 100) ** years_to_goal)
        
        # Calculate shortfall
        shortfall = max(0, future_cost - existing_savings)
        
        # Calculate required monthly SIP (assuming 12% returns)
        monthly_rate = 12 / 100 / 12
        total_months = years_to_goal * 12
        
        if monthly_rate > 0 and shortfall > 0:
            required_sip = shortfall * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
        else:
            required_sip = shortfall / total_months if total_months > 0 else 0
        
        # Alternative: Lumpsum investment
        if years_to_goal > 0:
            required_lumpsum = shortfall / ((1 + 12 / 100) ** years_to_goal)
        else:
            required_lumpsum = shortfall
        
        return {
            'goal': 'Child Education Planning',
            'child_current_age': child_age,
            'education_start_age': education_start_age,
            'years_to_goal': years_to_goal,
            'course_cost_today': course_cost_today,
            'future_course_cost': round(future_cost, 2),
            'education_inflation_rate': self.education_inflation,
            'existing_savings': existing_savings,
            'shortfall': round(shortfall, 2),
            'required_monthly_sip': round(required_sip, 2),
            'required_lumpsum': round(required_lumpsum, 2),
            'recommendation': f'Start SIP of ₹{required_sip:,.0f}/month or invest ₹{required_lumpsum:,.0f} lumpsum today'
        }
    
    def home_purchase_planning(self, target_home_price, down_payment_percent, 
                              years_to_purchase, existing_savings=0):
        """
        Calculate down payment corpus for home purchase
        Args:
            target_home_price: Expected home price (today's value)
            down_payment_percent: Down payment % (typically 20%)
            years_to_purchase: Years to purchase
            existing_savings: Current savings
        Returns:
            Dict with home purchase planning details
        """
        # Future home price with real estate inflation (8%)
        real_estate_inflation = 8
        future_home_price = target_home_price * ((1 + real_estate_inflation / 100) ** years_to_purchase)
        
        # Required down payment
        down_payment_amount = future_home_price * (down_payment_percent / 100)
        
        # Shortfall
        shortfall = max(0, down_payment_amount - existing_savings)
        
        # Calculate required monthly SIP (assuming 12% returns)
        monthly_rate = 12 / 100 / 12
        total_months = years_to_purchase * 12
        
        if monthly_rate > 0 and shortfall > 0:
            required_sip = shortfall * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
        else:
            required_sip = shortfall / total_months if total_months > 0 else 0
        
        # Loan calculation
        loan_amount = future_home_price - down_payment_amount
        
        # EMI calculation (20 year loan at 8.5% interest)
        loan_tenure_years = 20
        loan_interest_rate = 8.5
        monthly_loan_rate = loan_interest_rate / 100 / 12
        loan_months = loan_tenure_years * 12
        
        if monthly_loan_rate > 0:
            emi = loan_amount * monthly_loan_rate * ((1 + monthly_loan_rate) ** loan_months) / (
                ((1 + monthly_loan_rate) ** loan_months) - 1
            )
        else:
            emi = loan_amount / loan_months
        
        return {
            'goal': 'Home Purchase Planning',
            'target_home_price_today': target_home_price,
            'future_home_price': round(future_home_price, 2),
            'years_to_purchase': years_to_purchase,
            'down_payment_percent': down_payment_percent,
            'down_payment_required': round(down_payment_amount, 2),
            'existing_savings': existing_savings,
            'shortfall': round(shortfall, 2),
            'required_monthly_sip': round(required_sip, 2),
            'loan_amount': round(loan_amount, 2),
            'estimated_emi': round(emi, 2),
            'loan_tenure_years': loan_tenure_years,
            'loan_interest_rate': loan_interest_rate,
            'recommendation': f'Save ₹{required_sip:,.0f}/month for down payment. Expected EMI: ₹{emi:,.0f}/month'
        }
    
    def emergency_fund_planning(self, monthly_expenses, months_coverage=6, 
                               existing_emergency_fund=0):
        """
        Calculate emergency fund requirement
        Args:
            monthly_expenses: Current monthly expenses
            months_coverage: Number of months to cover (default 6)
            existing_emergency_fund: Current emergency savings
        Returns:
            Dict with emergency fund details
        """
        required_corpus = monthly_expenses * months_coverage
        shortfall = max(0, required_corpus - existing_emergency_fund)
        
        # Suggest building emergency fund in 12 months
        months_to_build = 12
        required_monthly_saving = shortfall / months_to_build if shortfall > 0 else 0
        
        # Recommendations for emergency fund placement
        allocation = {
            'Savings Account': {'percent': 30, 'amount': required_corpus * 0.30, 'liquidity': 'Instant'},
            'Liquid Funds': {'percent': 50, 'amount': required_corpus * 0.50, 'liquidity': '1-2 days'},
            'Short-term FD': {'percent': 20, 'amount': required_corpus * 0.20, 'liquidity': '1 week'}
        }
        
        return {
            'goal': 'Emergency Fund',
            'monthly_expenses': monthly_expenses,
            'months_coverage': months_coverage,
            'required_corpus': round(required_corpus, 2),
            'existing_fund': existing_emergency_fund,
            'shortfall': round(shortfall, 2),
            'months_to_build': months_to_build,
            'required_monthly_saving': round(required_monthly_saving, 2),
            'allocation': allocation,
            'recommendation': f'Build ₹{required_corpus:,.0f} emergency fund by saving ₹{required_monthly_saving:,.0f}/month',
            'status': 'Adequate' if shortfall == 0 else 'Needs Attention'
        }
    
    def wedding_planning(self, target_wedding_cost, years_to_wedding, existing_savings=0):
        """
        Calculate corpus needed for wedding
        Args:
            target_wedding_cost: Expected wedding cost (today's value)
            years_to_wedding: Years to wedding
            existing_savings: Current savings
        Returns:
            Dict with wedding planning details
        """
        # Wedding costs inflate faster (10%)
        wedding_inflation = 10
        future_wedding_cost = target_wedding_cost * ((1 + wedding_inflation / 100) ** years_to_wedding)
        
        shortfall = max(0, future_wedding_cost - existing_savings)
        
        # Calculate required monthly SIP (assuming 12% returns)
        if years_to_wedding > 0:
            monthly_rate = 12 / 100 / 12
            total_months = years_to_wedding * 12
            
            if monthly_rate > 0 and shortfall > 0:
                required_sip = shortfall * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
            else:
                required_sip = shortfall / total_months
        else:
            required_sip = 0
        
        return {
            'goal': 'Wedding Planning',
            'target_cost_today': target_wedding_cost,
            'future_cost': round(future_wedding_cost, 2),
            'years_to_wedding': years_to_wedding,
            'existing_savings': existing_savings,
            'shortfall': round(shortfall, 2),
            'required_monthly_sip': round(required_sip, 2),
            'wedding_inflation_rate': wedding_inflation,
            'recommendation': f'Start SIP of ₹{required_sip:,.0f}/month to save ₹{future_wedding_cost:,.0f}'
        }
    
    def vacation_planning(self, vacation_cost, years_to_vacation, existing_savings=0):
        """
        Calculate corpus for dream vacation
        Args:
            vacation_cost: Expected vacation cost (today's value)
            years_to_vacation: Years to vacation
            existing_savings: Current savings
        Returns:
            Dict with vacation planning details
        """
        # Travel costs inflate at 8%
        travel_inflation = 8
        future_vacation_cost = vacation_cost * ((1 + travel_inflation / 100) ** years_to_vacation)
        
        shortfall = max(0, future_vacation_cost - existing_savings)
        
        # Calculate required monthly saving
        if years_to_vacation > 0:
            # For short-term goals, use debt funds (8% returns)
            monthly_rate = 8 / 100 / 12
            total_months = years_to_vacation * 12
            
            if monthly_rate > 0 and shortfall > 0:
                required_monthly_saving = shortfall * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
            else:
                required_monthly_saving = shortfall / total_months
        else:
            required_monthly_saving = 0
        
        return {
            'goal': 'Vacation Planning',
            'vacation_cost_today': vacation_cost,
            'future_cost': round(future_vacation_cost, 2),
            'years_to_vacation': years_to_vacation,
            'existing_savings': existing_savings,
            'shortfall': round(shortfall, 2),
            'required_monthly_saving': round(required_monthly_saving, 2),
            'travel_inflation_rate': travel_inflation,
            'recommendation': f'Save ₹{required_monthly_saving:,.0f}/month in debt funds for your dream vacation'
        }
    
    def _get_retirement_recommendation(self, current_age, retirement_age, required_sip):
        """Generate personalized retirement recommendation"""
        years_to_retirement = retirement_age - current_age
        
        if years_to_retirement > 30:
            return f"Excellent! Starting early gives you {years_to_retirement} years. Consider aggressive equity allocation."
        elif years_to_retirement > 20:
            return f"Good timing! {years_to_retirement} years allows for balanced portfolio with equity focus."
        elif years_to_retirement > 10:
            return f"Start immediately! {years_to_retirement} years requires disciplined SIP of ₹{required_sip:,.0f}/month."
        else:
            return f"Critical! Only {years_to_retirement} years left. Consider increasing SIP significantly and maximizing equity exposure."
    
    def multi_goal_planner(self, goals):
        """
        Plan for multiple goals simultaneously
        Args:
            goals: List of goal dicts with 'name', 'amount', 'years', 'priority'
        Returns:
            Dict with prioritized investment plan
        """
        # Sort goals by priority (1 = highest) and years
        sorted_goals = sorted(goals, key=lambda x: (x.get('priority', 999), x['years']))
        
        total_required_sip = 0
        goal_plans = []
        
        for goal in sorted_goals:
            name = goal['name']
            amount = goal['amount']
            years = goal['years']
            priority = goal.get('priority', 'Medium')
            
            # Calculate required SIP for this goal
            if years > 0:
                monthly_rate = 12 / 100 / 12
                total_months = years * 12
                
                if monthly_rate > 0:
                    required_sip = amount * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
                else:
                    required_sip = amount / total_months
            else:
                required_sip = 0
            
            total_required_sip += required_sip
            
            goal_plans.append({
                'goal': name,
                'target_amount': amount,
                'years': years,
                'priority': priority,
                'required_monthly_sip': round(required_sip, 2)
            })
        
        return {
            'total_goals': len(goals),
            'total_required_monthly_sip': round(total_required_sip, 2),
            'goals': goal_plans,
            'recommendation': f'Total monthly investment needed: ₹{total_required_sip:,.0f}. Focus on high-priority goals first.'
        }