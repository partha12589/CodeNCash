"""
Live Market Data Integration
Fetches real-time data from Yahoo Finance and MFapi
"""

import yfinance as yf
import requests
from typing import Dict, List, Optional
import streamlit as st
from datetime import datetime

class LiveMarketData:
    """Fetch live market data from various sources"""
    
    def __init__(self):
        self.mf_api_base = "https://api.mfapi.in"
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_price(_self, symbol: str) -> Optional[Dict]:
        """
        Get live stock price from NSE
        Args:
            symbol: Stock symbol (e.g., 'TCS', 'RELIANCE')
        Returns:
            Dict with price, change, name
        """
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            info = ticker.info
            history = ticker.history(period="1d")
            
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                prev_close = info.get('previousClose', current_price)
                change_pct = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
                
                return {
                    "symbol": symbol,
                    "name": info.get('longName', symbol),
                    "price": round(current_price, 2),
                    "change_percent": round(change_pct, 2),
                    "currency": "INR",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
        except Exception as e:
            st.warning(f"Could not fetch live data for {symbol}: {str(e)}")
            return None
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour (NAV updates once daily)
    def get_mutual_fund_nav(_self, scheme_code: str) -> Optional[Dict]:
        """
        Get mutual fund NAV from MFapi
        Args:
            scheme_code: Scheme code from AMFI
        Returns:
            Dict with NAV, date, fund name
        """
        try:
            url = f"{_self.mf_api_base}/mf/{scheme_code}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                latest = data['data'][0] if data.get('data') else None
                
                if latest:
                    return {
                        "fund_name": data['meta']['scheme_name'],
                        "nav": float(latest['nav']),
                        "date": latest['date'],
                        "scheme_code": scheme_code
                    }
        except Exception as e:
            st.warning(f"Could not fetch NAV for scheme {scheme_code}: {str(e)}")
            return None
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_market_indices(_self) -> Dict:
        """
        Get Nifty 50 and Sensex indices
        Returns:
            Dict with index values and changes
        """
        try:
            nifty = yf.Ticker("^NSEI")
            sensex = yf.Ticker("^BSESN")
            
            nifty_hist = nifty.history(period="2d")
            sensex_hist = sensex.history(period="2d")
            
            result = {}
            
            if len(nifty_hist) >= 2:
                nifty_current = nifty_hist['Close'].iloc[-1]
                nifty_prev = nifty_hist['Close'].iloc[-2]
                nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
                
                result['nifty'] = {
                    "value": round(nifty_current, 2),
                    "change": round(nifty_change, 2)
                }
            
            if len(sensex_hist) >= 2:
                sensex_current = sensex_hist['Close'].iloc[-1]
                sensex_prev = sensex_hist['Close'].iloc[-2]
                sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
                
                result['sensex'] = {
                    "value": round(sensex_current, 2),
                    "change": round(sensex_change, 2)
                }
            
            return result
        except Exception as e:
            st.warning(f"Could not fetch market indices: {str(e)}")
            return {}
    
    def enrich_stock_data(self, stocks: List[Dict]) -> List[Dict]:
        """
        Enrich stock list with live prices
        Args:
            stocks: List of stock dicts with 'symbol' key
        Returns:
            Enhanced list with live data
        """
        enriched = []
        for stock in stocks:
            symbol = stock.get('symbol')
            live_data = self.get_stock_price(symbol) if symbol else None
            
            enriched_stock = stock.copy()
            if live_data:
                enriched_stock['live_price'] = live_data['price']
                enriched_stock['change_percent'] = live_data['change_percent']
                enriched_stock['timestamp'] = live_data['timestamp']
            
            enriched.append(enriched_stock)
        
        return enriched
    
    def enrich_fund_data(self, funds: List[Dict]) -> List[Dict]:
        """
        Enrich mutual fund list with live NAV
        Args:
            funds: List of fund dicts with 'scheme_code' key
        Returns:
            Enhanced list with live NAV
        """
        enriched = []
        for fund in funds:
            scheme_code = fund.get('scheme_code')
            nav_data = self.get_mutual_fund_nav(scheme_code) if scheme_code else None
            
            enriched_fund = fund.copy()
            if nav_data:
                enriched_fund['current_nav'] = nav_data['nav']
                enriched_fund['nav_date'] = nav_data['date']
            
            enriched.append(enriched_fund)
        
        return enriched


# Scheme codes for popular Indian mutual funds
POPULAR_SCHEME_CODES = {
    "SBI Bluechip Fund": "119551",
    "ICICI Prudential Bluechip Fund": "120503",
    "Axis Bluechip Fund": "120505",
    "Mirae Asset Large Cap Fund": "119598",
    "Parag Parikh Flexi Cap Fund": "122639",
    "HDFC Corporate Bond Fund": "119533",
    "ICICI Prudential Corporate Bond Fund": "120504",
    "Axis Banking & PSU Debt Fund": "120506"
}
