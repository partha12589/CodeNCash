"""
FastAPI Routes for CodeNCash Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.portfolio_service import PortfolioGenerator
from services.chat_service import ChatHandler
from services.live_market_service import LiveMarketData

app = FastAPI(title="CodeNCash API", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
portfolio_service = PortfolioGenerator()
chat_service = ChatHandler()
market_service = LiveMarketData()


# Request Models
class PortfolioRequest(BaseModel):
    capital: float
    monthly_investment: float
    risk_appetite: str
    preferences: Dict[str, bool]


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""


# Routes
@app.get("/")
async def root():
    return {
        "app": "CodeNCash API",
        "version": "2.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/portfolio/generate")
async def generate_portfolio(request: PortfolioRequest):
    """Generate personalized portfolio"""
    try:
        portfolio = portfolio_service.generate_portfolio(
            request.capital,
            request.monthly_investment,
            request.risk_appetite,
            request.preferences
        )
        return {"success": True, "portfolio": portfolio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Get AI response"""
    try:
        response = chat_service.get_response(
            request.message,
            request.context
        )
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/indices")
async def get_market_indices():
    """Get live market indices"""
    try:
        indices = market_service.get_market_indices()
        return {"success": True, "data": indices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/stock/{symbol}")
async def get_stock_price(symbol: str):
    """Get live stock price"""
    try:
        data = market_service.get_stock_price(symbol)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market/fund/{scheme_code}")
async def get_fund_nav(scheme_code: str):
    """Get mutual fund NAV"""
    try:
        data = market_service.get_mutual_fund_nav(scheme_code)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
