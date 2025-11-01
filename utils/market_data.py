import requests
import pandas as pd
from datetime import datetime

class IndianMarketData:
    """Fetch data from Indian stock markets and mutual funds"""
    
    def __init__(self):
        self.nse_api = "https://latest-stock-price.p.rapidapi.com/any"
        self.mf_api = "https://api.mfapi.in"
    
    def get_top_stocks(self, limit=10):
        """Get top Indian stocks recommendations based on market cap"""
        # Top blue-chip stocks in India
        top_stocks = [
            {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "Energy"},
            {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "IT"},
            {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "Banking"},
            {"symbol": "INFY", "name": "Infosys", "sector": "IT"},
            {"symbol": "ICICIBANK", "name": "ICICI Bank", "sector": "Banking"},
            {"symbol": "HINDUNILVR", "name": "Hindustan Unilever", "sector": "FMCG"},
            {"symbol": "ITC", "name": "ITC Limited", "sector": "FMCG"},
            {"symbol": "SBIN", "name": "State Bank of India", "sector": "Banking"},
            {"symbol": "BHARTIARTL", "name": "Bharti Airtel", "sector": "Telecom"},
            {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank", "sector": "Banking"}
        ]
        return top_stocks[:limit]
    
    def get_mutual_funds(self, category="equity"):
        """Get top performing mutual funds with scheme codes"""
        mutual_funds = {
            "equity": [
                {"name": "SBI Bluechip Fund", "category": "Large Cap", "returns_3y": "15.2%", "scheme_code": "119551"},
                {"name": "ICICI Prudential Bluechip Fund", "category": "Large Cap", "returns_3y": "14.8%", "scheme_code": "120503"},
                {"name": "Axis Bluechip Fund", "category": "Large Cap", "returns_3y": "16.1%", "scheme_code": "120505"},
                {"name": "Mirae Asset Large Cap Fund", "category": "Large Cap", "returns_3y": "15.5%", "scheme_code": "119598"},
                {"name": "Parag Parikh Flexi Cap Fund", "category": "Flexi Cap", "returns_3y": "18.2%", "scheme_code": "122639"}
            ],
            "debt": [
                {"name": "HDFC Corporate Bond Fund", "category": "Corporate Bond", "returns_3y": "7.2%", "scheme_code": "119533"},
                {"name": "ICICI Prudential Corporate Bond Fund", "category": "Corporate Bond", "returns_3y": "6.9%", "scheme_code": "120504"},
                {"name": "Axis Banking & PSU Debt Fund", "category": "Banking & PSU", "returns_3y": "7.5%", "scheme_code": "120506"}
            ]
        }
        return mutual_funds.get(category, mutual_funds["equity"])
    
    def get_debt_options(self):
        """Get debt fund and FD options"""
        debt_options = [
            {"name": "SBI Fixed Deposit", "type": "Bank FD", "interest_rate": "7.0%", "tenure": "1-5 years"},
            {"name": "HDFC Bank Fixed Deposit", "type": "Bank FD", "interest_rate": "7.1%", "tenure": "1-5 years"},
            {"name": "ICICI Bank Fixed Deposit", "type": "Bank FD", "interest_rate": "7.0%", "tenure": "1-5 years"},
            {"name": "Government Bonds", "type": "Bonds", "interest_rate": "7.3%", "tenure": "5-10 years"}
        ]
        return debt_options
