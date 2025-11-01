"""
Advanced SIP Calculator with Visualizations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class SIPCalculator:
    """Advanced SIP calculator with multiple scenarios"""
    
    def __init__(self):
        self.months_in_year = 12
    
    def calculate_sip(self, monthly_investment, years, annual_return_rate, step_up_percent=0):
        """
        Calculate SIP returns with optional step-up
        Args:
            monthly_investment: Monthly SIP amount
            years: Investment duration in years
            annual_return_rate: Expected annual return (as percentage)
            step_up_percent: Annual increase in SIP amount (default 0)
        Returns:
            Dict with calculation results and month-by-month data
        """
        monthly_rate = annual_return_rate / 100 / 12
        total_months = years * 12
        
        # Month-by-month calculation
        monthly_data = []
        current_sip = monthly_investment
        total_invested = 0
        current_value = 0
        
        start_date = datetime.now()
        
        for month in range(1, total_months + 1):
            # Apply step-up annually
            if month > 1 and (month - 1) % 12 == 0 and step_up_percent > 0:
                current_sip = current_sip * (1 + step_up_percent / 100)
            
            # Add monthly investment
            total_invested += current_sip
            
            # Calculate current value with interest
            current_value = (current_value + current_sip) * (1 + monthly_rate)
            
            # Calculate date
            current_date = start_date + relativedelta(months=month)
            
            monthly_data.append({
                'month': month,
                'date': current_date.strftime('%b %Y'),
                'sip_amount': round(current_sip, 2),
                'invested': round(total_invested, 2),
                'value': round(current_value, 2),
                'gains': round(current_value - total_invested, 2)
            })
        
        final_value = current_value
        total_gains = final_value - total_invested
        
        return {
            'monthly_investment': monthly_investment,
            'years': years,
            'total_months': total_months,
            'annual_return': annual_return_rate,
            'step_up_percent': step_up_percent,
            'total_invested': round(total_invested, 2),
            'final_value': round(final_value, 2),
            'total_gains': round(total_gains, 2),
            'absolute_return': round((total_gains / total_invested * 100), 2) if total_invested > 0 else 0,
            'monthly_data': monthly_data,
            'yearly_summary': self._create_yearly_summary(monthly_data)
        }
    
    def _create_yearly_summary(self, monthly_data):
        """Create year-wise summary from monthly data"""
        yearly_summary = []
        
        for year in range(1, len(monthly_data) // 12 + 2):
            year_end_month = min(year * 12, len(monthly_data))
            if year_end_month > 0:
                data = monthly_data[year_end_month - 1]
                yearly_summary.append({
                    'year': year,
                    'invested': data['invested'],
                    'value': data['value'],
                    'gains': data['gains']
                })
        
        return yearly_summary
    
    def compare_scenarios(self, monthly_investment, years):
        """Compare different return scenarios"""
        scenarios = {
            'Conservative': 8,
            'Moderate': 12,
            'Aggressive': 15,
            'Very Aggressive': 18
        }
        
        results = {}
        
        for scenario_name, return_rate in scenarios.items():
            result = self.calculate_sip(monthly_investment, years, return_rate)
            results[scenario_name] = {
                'return_rate': return_rate,
                'invested': result['total_invested'],
                'final_value': result['final_value'],
                'gains': result['total_gains'],
                'roi_percent': result['absolute_return']
            }
        
        return results
    
    def calculate_goal_based_sip(self, target_amount, years, annual_return_rate):
        """
        Calculate required monthly SIP to reach a goal
        Args:
            target_amount: Target corpus
            years: Time period
            annual_return_rate: Expected returns
        Returns:
            Required monthly SIP amount
        """
        monthly_rate = annual_return_rate / 100 / 12
        total_months = years * 12
        
        # Using future value of annuity formula: FV = P * [((1 + r)^n - 1) / r]
        # Rearranging: P = FV * r / ((1 + r)^n - 1)
        
        if monthly_rate > 0:
            required_sip = target_amount * monthly_rate / (((1 + monthly_rate) ** total_months) - 1)
        else:
            required_sip = target_amount / total_months
        
        result = self.calculate_sip(required_sip, years, annual_return_rate)
        
        return {
            'target_amount': target_amount,
            'required_monthly_sip': round(required_sip, 2),
            'years': years,
            'annual_return': annual_return_rate,
            'total_invested': result['total_invested'],
            'final_value': result['final_value'],
            'shortfall': round(target_amount - result['final_value'], 2)
        }
    
    def calculate_lumpsum_vs_sip(self, lumpsum_amount, monthly_sip, years, annual_return_rate):
        """Compare lumpsum investment vs SIP"""
        # Lumpsum calculation
        lumpsum_value = lumpsum_amount * ((1 + annual_return_rate / 100) ** years)
        lumpsum_gains = lumpsum_value - lumpsum_amount
        
        # SIP calculation
        sip_result = self.calculate_sip(monthly_sip, years, annual_return_rate)
        
        # Combined (if investing both)
        combined_invested = lumpsum_amount + sip_result['total_invested']
        combined_value = lumpsum_value + sip_result['final_value']
        combined_gains = combined_value - combined_invested
        
        return {
            'lumpsum': {
                'invested': lumpsum_amount,
                'final_value': round(lumpsum_value, 2),
                'gains': round(lumpsum_gains, 2),
                'roi_percent': round((lumpsum_gains / lumpsum_amount * 100), 2)
            },
            'sip': {
                'invested': sip_result['total_invested'],
                'final_value': sip_result['final_value'],
                'gains': sip_result['total_gains'],
                'roi_percent': sip_result['absolute_return']
            },
            'combined': {
                'invested': round(combined_invested, 2),
                'final_value': round(combined_value, 2),
                'gains': round(combined_gains, 2),
                'roi_percent': round((combined_gains / combined_invested * 100), 2)
            },
            'recommendation': 'SIP helps with rupee cost averaging' if sip_result['total_gains'] > lumpsum_gains else 'Lumpsum gives better absolute returns'
        }
    
    def calculate_step_up_benefit(self, monthly_investment, years, annual_return_rate):
        """Compare regular SIP vs step-up SIP"""
        # Regular SIP
        regular = self.calculate_sip(monthly_investment, years, annual_return_rate, 0)
        
        # Step-up scenarios
        step_up_5 = self.calculate_sip(monthly_investment, years, annual_return_rate, 5)
        step_up_10 = self.calculate_sip(monthly_investment, years, annual_return_rate, 10)
        step_up_15 = self.calculate_sip(monthly_investment, years, annual_return_rate, 15)
        
        return {
            'regular': {
                'invested': regular['total_invested'],
                'value': regular['final_value'],
                'gains': regular['total_gains']
            },
            'step_up_5': {
                'invested': step_up_5['total_invested'],
                'value': step_up_5['final_value'],
                'gains': step_up_5['total_gains'],
                'extra_benefit': round(step_up_5['total_gains'] - regular['total_gains'], 2)
            },
            'step_up_10': {
                'invested': step_up_10['total_invested'],
                'value': step_up_10['final_value'],
                'gains': step_up_10['total_gains'],
                'extra_benefit': round(step_up_10['total_gains'] - regular['total_gains'], 2)
            },
            'step_up_15': {
                'invested': step_up_15['total_invested'],
                'value': step_up_15['final_value'],
                'gains': step_up_15['total_gains'],
                'extra_benefit': round(step_up_15['total_gains'] - regular['total_gains'], 2)
            },
            'recommendation': f'A 10% annual step-up can increase your corpus by ₹{step_up_10["total_gains"] - regular["total_gains"]:,.0f}!'
        }
    
    def calculate_delay_impact(self, monthly_investment, years, annual_return_rate):
        """Show impact of delaying investment start"""
        results = {}
        
        for delay_years in [0, 1, 2, 5]:
            actual_years = max(1, years - delay_years)
            result = self.calculate_sip(monthly_investment, actual_years, annual_return_rate)
            
            results[f'start_now' if delay_years == 0 else f'delay_{delay_years}y'] = {
                'delay': delay_years,
                'investment_years': actual_years,
                'invested': result['total_invested'],
                'value': result['final_value'],
                'gains': result['total_gains']
            }
        
        opportunity_cost = results['start_now']['value'] - results.get('delay_5y', {}).get('value', 0)
        
        return {
            'scenarios': results,
            'opportunity_cost_5y': round(opportunity_cost, 2),
            'message': f'Delaying 5 years can cost you ₹{opportunity_cost:,.0f}! Start investing today.'
        }
    
    def calculate_inflation_adjusted_sip(self, monthly_investment, years, annual_return_rate, inflation_rate):
        """Calculate real returns after adjusting for inflation"""
        # Nominal returns
        nominal = self.calculate_sip(monthly_investment, years, annual_return_rate)
        
        # Real return rate (Fisher equation approximation)
        real_return_rate = ((1 + annual_return_rate / 100) / (1 + inflation_rate / 100) - 1) * 100
        
        # Real returns
        real = self.calculate_sip(monthly_investment, years, real_return_rate)
        
        return {
            'nominal_return_rate': annual_return_rate,
            'inflation_rate': inflation_rate,
            'real_return_rate': round(real_return_rate, 2),
            'nominal_value': nominal['final_value'],
            'real_value': real['final_value'],
            'inflation_impact': round(nominal['final_value'] - real['final_value'], 2),
            'purchasing_power': round((real['final_value'] / nominal['final_value'] * 100), 2),
            'message': f'Your ₹{nominal["final_value"]:,.0f} will have purchasing power of ₹{real["final_value"]:,.0f} in today\'s terms'
        }