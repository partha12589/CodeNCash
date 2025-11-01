# 🤖 Finbot: AI-Powered Investment Advisor

Your personal AI assistant for building the perfect Indian investment portfolio.

## 🎉 Round 1 Status: SELECTED!

We've successfully completed Round 1 and been selected to move forward!

---

## 📋 Current Features (MVP)

- 💬 **AI Chatbot**: Powered by Groq API (Llama 3.3) for investment advice
- 📊 **Portfolio Generation**: Personalized portfolios based on risk appetite
- 📈 **Market Coverage**: Indian stocks (NSE/BSE), mutual funds, debt funds, bonds
- 💰 **Investment Planning**: Capital and SIP-based recommendations
- 📉 **Return Projections**: 1-year, 3-year, and 5-year projections
- 🎯 **Risk-Based Allocation**: Low, Medium, High risk portfolios

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd workspace
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application
```bash
streamlit run app.py
```

5. Open your browser and navigate to `http://localhost:8501`

---

## 🎯 Development Roadmap

### ✅ Round 1: MVP (COMPLETED)
- Basic portfolio generation
- AI chatbot integration
- Risk-based asset allocation
- Simple UI with Streamlit

### 🎨 Round 2: Frontend Excellence (IN PROGRESS)
**Goal**: Make it beautiful and engaging

**Timeline**: 4 weeks

**Focus Areas**:
- Modern, professional UI design
- Interactive data visualizations
- Enhanced chat interface
- Mobile-responsive layout
- Smooth animations and transitions

**📄 Detailed Plan**: See [ROUND_2_PLAN.md](./ROUND_2_PLAN.md)

### 🚀 Final Round: Production Platform (PLANNED)
**Goal**: Comprehensive fintech platform

**Timeline**: 4.5-6 months

**Key Features**:
- Real-time NSE/BSE market data
- User authentication & saved portfolios
- ML-powered portfolio optimization
- Live portfolio tracking
- Broker integrations (Zerodha, Upstox)
- Mobile app
- Premium subscription model
- Advanced analytics

**📄 Detailed Plan**: See [FINAL_ROUND_PLAN.md](./FINAL_ROUND_PLAN.md)

**🗺️ Quick Reference**: See [DEVELOPMENT_ROADMAP.md](./DEVELOPMENT_ROADMAP.md)

---

## 🛠️ Tech Stack

### Current (Round 1)
- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: Groq API (Llama 3.3 70B)
- **Market Data**: Static data + yfinance
- **Data Processing**: Pandas, NumPy

### Planned (Final Round)
- **Frontend**: React.js + Next.js
- **Backend**: FastAPI
- **Database**: PostgreSQL, Redis, TimescaleDB
- **AI/ML**: LangChain, scikit-learn, TensorFlow
- **Infrastructure**: Docker, Kubernetes, AWS/GCP

---

## 📁 Project Structure

```
workspace/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── ROUND_2_PLAN.md            # Detailed Round 2 plan
├── FINAL_ROUND_PLAN.md        # Detailed Final Round plan
├── DEVELOPMENT_ROADMAP.md     # Quick reference guide
└── utils/
    ├── chat_handler.py        # AI chatbot logic
    ├── market_data.py         # Market data fetching
    └── portfolio.py           # Portfolio generation
```

---

## 🎨 Screenshots

### Chat Interface
Talk to Finbot about investments, ask questions, get personalized advice.

### Portfolio Generation
Input your capital, risk appetite, and preferences to generate a customized portfolio.

### Recommendations
Get specific stock, mutual fund, and debt fund recommendations tailored to your profile.

---

## 🤝 Contributing

We're currently in development mode. Contributions will be welcome after Round 2!

---

## 📜 License

This project is part of a competitive development program. All rights reserved.

---

## 📞 Contact

For questions or feedback, please reach out to the development team.

---

## ⚠️ Disclaimer

Finbot provides educational investment information and suggestions based on Indian markets (NSE/BSE). This is not financial advice. Always consult with a certified financial advisor before making investment decisions. Past performance does not guarantee future results.

---

## 🙏 Acknowledgments

- Groq for providing AI API access
- Streamlit for the amazing framework
- Indian financial market data providers
- All beta testers and early users

---

**Made with ❤️ for Indian investors**
