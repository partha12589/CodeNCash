"""
Interactive visualizations using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List

class PortfolioVisualizations:
    """Create beautiful charts for portfolio data"""
    
    # Color scheme matching the CSS
    COLORS = {
        'primary': '#0066FF',
        'secondary': '#00D9A3',
        'accent': '#FFB800',
        'success': '#10B981',
        'danger': '#EF4444',
        'bg_dark': '#0A0E27',
        'bg_card': '#151B3D',
        'text': '#FFFFFF'
    }
    
    @staticmethod
    def create_allocation_pie_chart(allocation: Dict[str, float], title: str = "Asset Allocation") -> go.Figure:
        """
        Create an interactive pie chart for asset allocation
        Args:
            allocation: Dict with asset types and percentages
            title: Chart title
        Returns:
            Plotly figure
        """
        labels = [k.replace('_', ' ').title() for k in allocation.keys()]
        values = list(allocation.values())
        
        colors = ['#0066FF', '#00D9A3', '#FFB800', '#8B5CF6', '#EF4444']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(
                colors=colors,
                line=dict(color='#151B3D', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{label}</b><br>Allocation: %{percent}<br>Value: ?%{value}%<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='white')),
            paper_bgcolor='#151B3D',
            plot_bgcolor='#151B3D',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_returns_chart(projected_returns: Dict, capital: float, monthly_sip: float) -> go.Figure:
        """
        Create a line chart for projected returns over time
        Args:
            projected_returns: Dict with year projections
            capital: Initial capital
            monthly_sip: Monthly SIP amount
        Returns:
            Plotly figure
        """
        years = []
        total_values = []
        invested_amounts = []
        gains = []
        
        for period, values in sorted(projected_returns.items()):
            year = int(period.split('_')[0])
            years.append(f"{year}Y")
            total_values.append(values['total_value'])
            invested = capital + (monthly_sip * 12 * year)
            invested_amounts.append(invested)
            gains.append(values['gains'])
        
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        # Invested amount
        fig.add_trace(
            go.Scatter(
                x=years,
                y=invested_amounts,
                name="Invested Amount",
                mode='lines+markers',
                line=dict(color='#FFB800', width=3, dash='dash'),
                marker=dict(size=10)
            )
        )
        
        # Total value
        fig.add_trace(
            go.Scatter(
                x=years,
                y=total_values,
                name="Expected Value",
                mode='lines+markers',
                line=dict(color='#00D9A3', width=4),
                marker=dict(size=12),
                fill='tonexty',
                fillcolor='rgba(0, 217, 163, 0.1)'
            )
        )
        
        fig.update_layout(
            title=dict(text="Investment Growth Projection", font=dict(size=20, color='white')),
            xaxis=dict(title="Time Period", color='white', gridcolor='#2D3748'),
            yaxis=dict(title="Amount (?)", color='white', gridcolor='#2D3748'),
            paper_bgcolor='#151B3D',
            plot_bgcolor='#0A0E27',
            font=dict(color='white'),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_gains_bar_chart(projected_returns: Dict) -> go.Figure:
        """
        Create a bar chart showing gains over time
        Args:
            projected_returns: Dict with year projections
        Returns:
            Plotly figure
        """
        years = []
        gains = []
        
        for period, values in sorted(projected_returns.items()):
            year = int(period.split('_')[0])
            years.append(f"{year} Year")
            gains.append(values['gains'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=years,
                y=gains,
                marker=dict(
                    color=gains,
                    colorscale=[[0, '#FFB800'], [0.5, '#00D9A3'], [1, '#0066FF']],
                    line=dict(color='#151B3D', width=2)
                ),
                text=[f"?{g:,.0f}" for g in gains],
                textposition='outside',
                textfont=dict(size=14, color='white'),
                hovertemplate='<b>%{x}</b><br>Gains: ?%{y:,.0f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(text="Expected Gains", font=dict(size=20, color='white')),
            xaxis=dict(title="", color='white', gridcolor='#2D3748'),
            yaxis=dict(title="Gains (?)", color='white', gridcolor='#2D3748'),
            paper_bgcolor='#151B3D',
            plot_bgcolor='#0A0E27',
            font=dict(color='white'),
            height=350
        )
        
        return fig
    
    @staticmethod
    def create_risk_gauge(risk_level: str) -> go.Figure:
        """
        Create a gauge chart for risk level
        Args:
            risk_level: 'Low', 'Medium', or 'High'
        Returns:
            Plotly figure
        """
        risk_values = {'Low': 33, 'Medium': 66, 'High': 100}
        value = risk_values.get(risk_level, 50)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Level: {risk_level}", 'font': {'size': 20, 'color': 'white'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#0066FF"},
                'bgcolor': "#0A0E27",
                'borderwidth': 2,
                'bordercolor': "#2D3748",
                'steps': [
                    {'range': [0, 33], 'color': '#10B981'},
                    {'range': [33, 66], 'color': '#FFB800'},
                    {'range': [66, 100], 'color': '#EF4444'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='#151B3D',
            font={'color': "white"},
            height=300
        )
        
        return fig
    
    @staticmethod
    def create_diversification_chart(recommendations: Dict) -> go.Figure:
        """
        Create a stacked bar chart showing diversification
        Args:
            recommendations: Portfolio recommendations dict
        Returns:
            Plotly figure
        """
        categories = []
        amounts = []
        colors_list = []
        
        color_map = {
            'stocks': '#0066FF',
            'mutual_funds': '#00D9A3',
            'debt': '#FFB800'
        }
        
        for cat, data in recommendations.items():
            cat_name = cat.replace('_', ' ').title()
            categories.append(cat_name)
            amounts.append(data.get('amount', 0))
            colors_list.append(color_map.get(cat, '#8B5CF6'))
        
        fig = go.Figure(data=[
            go.Bar(
                y=categories,
                x=amounts,
                orientation='h',
                marker=dict(
                    color=colors_list,
                    line=dict(color='#151B3D', width=2)
                ),
                text=[f"?{a:,.0f}" for a in amounts],
                textposition='auto',
                textfont=dict(size=14, color='white'),
                hovertemplate='<b>%{y}</b><br>Amount: ?%{x:,.0f}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(text="Investment Distribution", font=dict(size=20, color='white')),
            xaxis=dict(title="Amount (?)", color='white', gridcolor='#2D3748'),
            yaxis=dict(title="", color='white'),
            paper_bgcolor='#151B3D',
            plot_bgcolor='#0A0E27',
            font=dict(color='white'),
            height=300
        )
        
        return fig
