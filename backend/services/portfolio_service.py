import pandas as pd
from utils.market_data import IndianMarketData

class PortfolioGenerator:
    """Generate investment portfolio based on user preferences"""
    
    def __init__(self):
        self.market_data = IndianMarketData()
    
    def generate_portfolio(self, capital, monthly_investment, risk_appetite, preferences):
        """Generate diversified portfolio based on risk appetite"""
        
        # Asset allocation based on risk
        allocation = self.get_asset_allocation(risk_appetite)
        
        portfolio = {
            "total_investment": capital,
            "monthly_sip": monthly_investment,
            "risk_level": risk_appetite,
            "allocation": allocation,
            "recommendations": {}
        }
        
        # Add stock recommendations if selected
        if preferences.get("stocks"):
            stocks = self.market_data.get_top_stocks(5)
            stock_amount = capital * (allocation["equity"] / 100)
            portfolio["recommendations"]["stocks"] = {
                "amount": stock_amount,
                "list": stocks
            }
        
        # Add mutual fund recommendations if selected
        if preferences.get("mutual_funds"):
            mf_equity = self.market_data.get_mutual_funds("equity")
            mf_amount = capital * (allocation["mutual_funds"] / 100)
            portfolio["recommendations"]["mutual_funds"] = {
                "amount": mf_amount,
                "list": mf_equity[:3]
            }
        
        # Add debt recommendations if selected
        if preferences.get("debt_funds") or preferences.get("bonds"):
            debt = self.market_data.get_debt_options()
            debt_amount = capital * (allocation["debt"] / 100)
            portfolio["recommendations"]["debt"] = {
                "amount": debt_amount,
                "list": debt[:3]
            }
        
        # Calculate projected returns
        portfolio["projected_returns"] = self.calculate_returns(
            capital, monthly_investment, risk_appetite
        )
        
        return portfolio
    
    def get_asset_allocation(self, risk_appetite):
        """Get asset allocation percentages based on risk"""
        allocations = {
            "Low": {
                "equity": 20,
                "mutual_funds": 20,
                "debt": 50,
                "liquid": 10
            },
            "Medium": {
                "equity": 30,
                "mutual_funds": 30,
                "debt": 30,
                "liquid": 10
            },
            "High": {
                "equity": 45,
                "mutual_funds": 35,
                "debt": 15,
                "liquid": 5
            }
        }
        return allocations.get(risk_appetite, allocations["Medium"])
    
    def calculate_returns(self, capital, monthly_investment, risk_appetite):
        """Calculate projected returns over 1, 3, 5 years"""
        # Expected annual returns based on risk
        returns_rate = {
            "Low": 0.08,    # 8% annual return
            "Medium": 0.12, # 12% annual return
            "High": 0.15    # 15% annual return
        }
        
        rate = returns_rate.get(risk_appetite, 0.12)
        
        projections = {}
        for years in [1, 3, 5]:
            # Calculate with compound interest and monthly SIP
            future_value = capital * ((1 + rate) ** years)
            sip_value = monthly_investment * 12 * years * (1 + rate/2)
            total = future_value + sip_value
            
            projections[f"{years}_year"] = {
                "total_value": round(total, 2),
                "gains": round(total - (capital + monthly_investment * 12 * years), 2)
            }
        
        return projections
