"""
Tax Optimizer for Indian Investors
Helps optimize tax savings under various sections
"""

class TaxOptimizer:
    """Calculate and optimize tax savings for Indian investors"""
    
    # Tax slabs for FY 2024-25 (New Regime)
    NEW_REGIME_SLABS = [
        (300000, 0),      # Up to 3L - 0%
        (700000, 0.05),   # 3L to 7L - 5%
        (1000000, 0.10),  # 7L to 10L - 10%
        (1200000, 0.15),  # 10L to 12L - 15%
        (1500000, 0.20),  # 12L to 15L - 20%
        (float('inf'), 0.30)  # Above 15L - 30%
    ]
    
    # Old Regime slabs
    OLD_REGIME_SLABS = [
        (250000, 0),      # Up to 2.5L - 0%
        (500000, 0.05),   # 2.5L to 5L - 5%
        (1000000, 0.20),  # 5L to 10L - 20%
        (float('inf'), 0.30)  # Above 10L - 30%
    ]
    
    def __init__(self):
        self.section_80c_limit = 150000
        self.section_80ccd_1b_limit = 50000  # Additional NPS
        self.section_80d_limit = 25000  # Health insurance (self)
        self.section_80d_parents_limit = 50000  # Parents (senior citizens)
        self.section_80g_limit = 0.10  # 10% of gross income for donations
        self.section_24b_limit = 200000  # Home loan interest
        self.hra_exemption = True
        self.standard_deduction = 50000
    
    def calculate_tax(self, income, regime='new', deductions=None):
        """
        Calculate tax based on income and regime
        Args:
            income: Annual gross income
            regime: 'new' or 'old'
            deductions: Dict of deductions for old regime
        Returns:
            Dict with tax calculation details
        """
        if regime == 'new':
            return self._calculate_new_regime_tax(income)
        else:
            return self._calculate_old_regime_tax(income, deductions or {})
    
    def _calculate_new_regime_tax(self, income):
        """Calculate tax under new regime"""
        taxable_income = income - self.standard_deduction
        tax = 0
        prev_limit = 0
        breakdown = []
        
        for limit, rate in self.NEW_REGIME_SLABS:
            if taxable_income > prev_limit:
                taxable_in_slab = min(taxable_income, limit) - prev_limit
                tax_in_slab = taxable_in_slab * rate
                tax += tax_in_slab
                
                if taxable_in_slab > 0:
                    breakdown.append({
                        'slab': f"₹{prev_limit:,} - ₹{limit:,}" if limit != float('inf') else f"Above ₹{prev_limit:,}",
                        'amount': taxable_in_slab,
                        'rate': f"{rate*100:.0f}%",
                        'tax': tax_in_slab
                    })
                
                prev_limit = limit
                if taxable_income <= limit:
                    break
        
        # Add cess
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            'regime': 'New Regime',
            'gross_income': income,
            'standard_deduction': self.standard_deduction,
            'taxable_income': taxable_income,
            'tax_before_cess': tax,
            'cess': cess,
            'total_tax': total_tax,
            'effective_rate': (total_tax / income * 100) if income > 0 else 0,
            'breakdown': breakdown
        }
    
    def _calculate_old_regime_tax(self, income, deductions):
        """Calculate tax under old regime with deductions"""
        # Calculate total deductions
        section_80c = min(deductions.get('80c', 0), self.section_80c_limit)
        section_80ccd_1b = min(deductions.get('80ccd_1b', 0), self.section_80ccd_1b_limit)
        section_80d = min(deductions.get('80d', 0), self.section_80d_limit)
        section_80d_parents = min(deductions.get('80d_parents', 0), self.section_80d_parents_limit)
        section_80g = min(deductions.get('80g', 0), income * self.section_80g_limit)
        section_24b = min(deductions.get('24b', 0), self.section_24b_limit)
        hra_exemption = deductions.get('hra', 0)
        
        total_deductions = (section_80c + section_80ccd_1b + section_80d + 
                          section_80d_parents + section_80g + section_24b + 
                          hra_exemption + self.standard_deduction)
        
        taxable_income = max(0, income - total_deductions)
        
        # Calculate tax
        tax = 0
        prev_limit = 0
        breakdown = []
        
        for limit, rate in self.OLD_REGIME_SLABS:
            if taxable_income > prev_limit:
                taxable_in_slab = min(taxable_income, limit) - prev_limit
                tax_in_slab = taxable_in_slab * rate
                tax += tax_in_slab
                
                if taxable_in_slab > 0:
                    breakdown.append({
                        'slab': f"₹{prev_limit:,} - ₹{limit:,}" if limit != float('inf') else f"Above ₹{prev_limit:,}",
                        'amount': taxable_in_slab,
                        'rate': f"{rate*100:.0f}%",
                        'tax': tax_in_slab
                    })
                
                prev_limit = limit
                if taxable_income <= limit:
                    break
        
        # Add cess
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            'regime': 'Old Regime',
            'gross_income': income,
            'deductions': {
                'Section 80C': section_80c,
                'Section 80CCD(1B) - NPS': section_80ccd_1b,
                'Section 80D - Health': section_80d,
                'Section 80D - Parents': section_80d_parents,
                'Section 80G - Donations': section_80g,
                'Section 24B - Home Loan': section_24b,
                'HRA Exemption': hra_exemption,
                'Standard Deduction': self.standard_deduction
            },
            'total_deductions': total_deductions,
            'taxable_income': taxable_income,
            'tax_before_cess': tax,
            'cess': cess,
            'total_tax': total_tax,
            'effective_rate': (total_tax / income * 100) if income > 0 else 0,
            'breakdown': breakdown
        }
    
    def compare_regimes(self, income, deductions):
        """Compare both tax regimes"""
        new_regime = self.calculate_tax(income, 'new')
        old_regime = self.calculate_tax(income, 'old', deductions)
        
        savings = new_regime['total_tax'] - old_regime['total_tax']
        better_regime = 'Old Regime' if savings > 0 else 'New Regime'
        
        return {
            'new_regime': new_regime,
            'old_regime': old_regime,
            'savings': abs(savings),
            'better_regime': better_regime,
            'recommendation': self._get_recommendation(income, deductions, savings)
        }
    
    def _get_recommendation(self, income, deductions, savings):
        """Get personalized recommendation"""
        total_deductions = sum(deductions.values())
        
        if savings > 0:  # Old regime is better
            if total_deductions < 200000:
                return f"Old Regime saves you ₹{abs(savings):,.0f}! Consider maximizing 80C deductions."
            else:
                return f"Old Regime is optimal for you, saving ₹{abs(savings):,.0f}!"
        else:  # New regime is better
            return f"New Regime saves you ₹{abs(savings):,.0f}! Simpler with no deduction hassles."
    
    def suggest_investments_for_80c(self, current_investment=0):
        """Suggest 80C investment options"""
        remaining = self.section_80c_limit - current_investment
        
        if remaining <= 0:
            return {
                'status': 'optimized',
                'message': '✅ Section 80C limit fully utilized!',
                'suggestions': []
            }
        
        suggestions = [
            {
                'option': 'ELSS Mutual Funds',
                'amount': min(remaining, 50000),
                'benefit': 'Tax saving + Equity returns',
                'lock_in': '3 years',
                'priority': 'High'
            },
            {
                'option': 'PPF (Public Provident Fund)',
                'amount': min(remaining, 150000),
                'benefit': 'Safe returns ~7.1%',
                'lock_in': '15 years',
                'priority': 'High'
            },
            {
                'option': 'EPF (Employee Provident Fund)',
                'amount': min(remaining, 100000),
                'benefit': 'Safe, employer matching',
                'lock_in': 'Till retirement',
                'priority': 'Medium'
            },
            {
                'option': 'NSC (National Savings Certificate)',
                'amount': min(remaining, 100000),
                'benefit': 'Fixed returns ~7%',
                'lock_in': '5 years',
                'priority': 'Medium'
            },
            {
                'option': 'Tax Saving FD',
                'amount': min(remaining, 150000),
                'benefit': 'Fixed returns ~6-7%',
                'lock_in': '5 years',
                'priority': 'Low'
            }
        ]
        
        return {
            'status': 'pending',
            'remaining': remaining,
            'potential_savings': remaining * 0.30,  # Assuming 30% tax bracket
            'message': f'💰 Invest ₹{remaining:,} more to save up to ₹{remaining * 0.30:,.0f} in taxes!',
            'suggestions': suggestions
        }
    
    def calculate_nps_benefit(self, contribution):
        """Calculate additional NPS benefit under 80CCD(1B)"""
        eligible = min(contribution, self.section_80ccd_1b_limit)
        tax_saved = eligible * 0.30  # Assuming 30% bracket
        
        return {
            'contribution': contribution,
            'eligible_deduction': eligible,
            'tax_saved': tax_saved,
            'recommendation': 'Maximize NPS for extra ₹50,000 deduction beyond 80C!' if eligible < self.section_80ccd_1b_limit else 'NPS limit optimized!'
        }
    
    def calculate_home_loan_benefit(self, interest_paid, principal_paid):
        """Calculate home loan tax benefits"""
        # Interest deduction under 24B
        interest_deduction = min(interest_paid, self.section_24b_limit)
        
        # Principal deduction under 80C
        principal_deduction = principal_paid  # Will be capped at 80C limit
        
        total_benefit = interest_deduction + min(principal_deduction, self.section_80c_limit)
        tax_saved = total_benefit * 0.30  # Assuming 30% bracket
        
        return {
            'interest_paid': interest_paid,
            'interest_deduction': interest_deduction,
            'principal_paid': principal_paid,
            'principal_deduction': min(principal_deduction, self.section_80c_limit),
            'total_benefit': total_benefit,
            'tax_saved': tax_saved,
            'note': 'Principal repayment counts towards 80C limit'
        }