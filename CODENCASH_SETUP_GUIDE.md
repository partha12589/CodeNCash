# ?? CodeNCash - Setup Guide

## Welcome to CodeNCash!

**Your AI-Powered Investment Advisor for Indian Markets**

---

## ?? New Project Structure

```
/workspace/
??? backend/                    # Backend services
?   ??? api/
?   ?   ??? __init__.py
?   ?   ??? routes.py          # FastAPI routes (optional)
?   ??? services/
?   ?   ??? portfolio_service.py
?   ?   ??? chat_service.py
?   ?   ??? live_market_service.py
?   ?   ??? market_data_service.py
?   ?   ??? visualization_service.py
?   ??? __init__.py
?
??? frontend/                   # Frontend application
?   ??? assets/
?   ?   ??? codencash_logo.py
?   ??? codencash_app.py       # Main Streamlit app ?
?   ??? pages/                  # Additional pages
?
??? style.css                   # Custom CSS styling
??? .env                        # Environment variables
?
??? requirements-frontend.txt   # Frontend dependencies
??? requirements-backend.txt    # Backend dependencies
?
??? start_frontend.sh          # Quick start script ?
??? start_backend.sh           # API server script
```

---

## ?? Quick Start (Recommended)

### Option 1: Streamlit Frontend Only (Fastest)

```bash
# 1. Install dependencies
pip install -r requirements-frontend.txt

# 2. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 3. Run the app (ONE COMMAND!)
./start_frontend.sh

# OR manually:
cd frontend
streamlit run codencash_app.py
```

**Open:** `http://localhost:8501`

---

### Option 2: With Backend API (Optional)

Terminal 1 (Backend):
```bash
pip install -r requirements-backend.txt
./start_backend.sh
```

Terminal 2 (Frontend):
```bash
pip install -r requirements-frontend.txt
./start_frontend.sh
```

**Frontend:** `http://localhost:8501`
**Backend API:** `http://localhost:8000`
**API Docs:** `http://localhost:8000/docs`

---

## ?? What's New - CodeNCash Rebrand

### ? Enhanced Features:

1. **Better Portfolio Display**
   - ? Fixed layout issues
   - ? Expandable sections (better than tabs)
   - ? Cleaner metric cards
   - ? More responsive design

2. **CodeNCash Branding**
   - ? New logo and color scheme
   - ? Professional gradient header
   - ? Improved typography
   - ? Better visual hierarchy

3. **More Interactive UI**
   - ? Welcome cards with CTAs
   - ? Better chat suggestions
   - ? Improved loading states
   - ? Live market data in header

4. **Better Organization**
   - ? Separate backend/frontend folders
   - ? Modular service architecture
   - ? FastAPI backend ready
   - ? Easy to scale

---

## ?? Features Overview

### ?? Portfolio Generation
- Risk-based asset allocation
- Personalized recommendations
- Live market data integration
- Interactive visualizations

### ?? AI Chat Advisor
- Context-aware responses
- Suggested questions
- Portfolio-specific advice
- Powered by Groq (Llama 3.3)

### ?? Live Market Data
- NSE/BSE stock prices
- Mutual fund NAVs
- Market indices (Nifty, Sensex)
- Real-time updates

### ?? Visualizations
- Interactive pie charts
- Growth projection graphs
- Returns analysis
- Distribution charts

---

## ?? UI Improvements

### Before (Old Finbot):
- Basic tabs
- Simple layout
- Standard metrics
- Generic branding

### After (CodeNCash):
- ? Expandable sections (mobile-friendly)
- ? Gradient cards
- ? Enhanced metrics with context
- ? Professional branding
- ? Welcome screens
- ? Better spacing and hierarchy

---

## ?? Configuration

### Required: .env File

Create `.env` in project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key: https://console.groq.com

---

## ?? How to Use

### Step 1: Fill the Form (Sidebar)
- **Initial Investment:** Your starting capital
- **Monthly SIP:** Regular monthly investment
- **Risk Appetite:** Low/Medium/High
- **Investment Types:** Select your preferences

### Step 2: Generate Portfolio
Click **"?? Generate My Portfolio"** button

### Step 3: Explore Results
- **Asset Allocation:** See your portfolio mix
- **Growth Projections:** View expected returns
- **Recommendations:** Get specific investments with live prices

### Step 4: Chat with AI
Ask questions about investing, your portfolio, or market trends

---

## ?? Demo Tips

### For Best Results:
1. Use recommended inputs:
   - Capital: ?5,00,000
   - Monthly SIP: ?10,000
   - Risk: Medium
   - Select all investment types

2. Highlight these features:
   - Live Nifty/Sensex in header
   - Interactive charts (hover to explore)
   - Live stock prices with ?? indicators
   - AI chat with context awareness

3. Show the flow:
   - Fill form ? Generate ? View charts ? Ask AI questions

---

## ?? Troubleshooting

### "Cannot see charts"
- Charts are in expandable sections, not tabs
- Click "?? Asset Allocation" to expand
- Make sure portfolio is generated first

### "Import errors"
```bash
# Make sure you're in the right directory
cd frontend
streamlit run codencash_app.py
```

### "Live data not loading"
- Check internet connection
- Verify API access to Yahoo Finance
- Data is cached for 5 minutes

### "Groq API error"
- Check .env file exists
- Verify GROQ_API_KEY is correct
- UI still works without AI responses

---

## ?? Quick Commands

### Install & Run (One-liner):
```bash
pip install -r requirements-frontend.txt && cd frontend && streamlit run codencash_app.py
```

### With fresh install:
```bash
./start_frontend.sh --install
```

### Check dependencies:
```bash
python3 -c "import streamlit, plotly, yfinance; print('? Ready!')"
```

### Test backend API:
```bash
./start_backend.sh --install
# Then visit: http://localhost:8000/docs
```

---

## ?? Documentation

- **QUICK_DEMO_CARD.md** - 60-second pitch
- **DEMO_GUIDE.md** - Full demo script
- **ROUND_2_COMPLETE.md** - Feature summary
- **CODENCASH_SETUP_GUIDE.md** - This file

---

## ?? Key Improvements Summary

### Layout Fixes:
- ? Portfolio displays properly in expandable sections
- ? Better mobile responsiveness
- ? Clearer visual hierarchy
- ? Fixed metric alignment

### Interactivity:
- ? Welcome cards with CTAs
- ? Animated transitions
- ? Better loading states
- ? More engaging UI elements

### Branding:
- ? CodeNCash logo and colors
- ? Professional gradients
- ? Consistent design language
- ? Better typography

### Structure:
- ? Clean backend/frontend separation
- ? Modular services
- ? Easy to maintain
- ? Ready for scaling

---

## ?? Next Steps

1. ? Run the app: `./start_frontend.sh`
2. ? Test all features
3. ? Review QUICK_DEMO_CARD.md for pitch
4. ? Practice your demo
5. ? Win Round 2! ??

---

## ?? Pro Tips

- Charts are now in **expandable sections** (not tabs) - easier to see!
- Click to expand any section
- Hover over charts for details
- Try the AI chat suggestions
- Check live market data in header

---

**CodeNCash** - Making investing accessible through AI ?

*Powered by Groq, Yahoo Finance, and MFapi*
