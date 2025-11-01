"""
Enhanced PDF Portfolio Generator for Finbot
Includes charts, better styling, and comprehensive portfolio details
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


def create_pie_chart(allocation_data):
    """Create a pie chart for asset allocation"""
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#151B3D')
    
    labels = [k.replace('_', ' ').title() for k in allocation_data.keys()]
    sizes = list(allocation_data.values())
    colors_list = ['#0066FF', '#00D9A3', '#FFB800', '#8B5CF6', '#EF4444']
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors_list,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'color': 'white', 'fontsize': 11, 'weight': 'bold'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    ax.set_facecolor('#151B3D')
    plt.title('Asset Allocation', color='white', fontsize=14, weight='bold', pad=20)
    
    # Save to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#151B3D')
    buf.seek(0)
    plt.close()
    
    return buf


def create_returns_chart(projected_returns, capital, monthly_sip):
    """Create a line chart for projected returns"""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor='#151B3D')
    
    years = []
    total_values = []
    invested_amounts = []
    
    for period, values in sorted(projected_returns.items()):
        year = int(period.split('_')[0])
        years.append(f"{year}Y")
        total_values.append(values['total_value'])
        invested = capital + (monthly_sip * 12 * year)
        invested_amounts.append(invested)
    
    ax.plot(years, invested_amounts, marker='o', linewidth=3, 
            color='#FFB800', label='Invested Amount', linestyle='--', markersize=8)
    ax.plot(years, total_values, marker='o', linewidth=3, 
            color='#00D9A3', label='Expected Value', markersize=10)
    
    ax.fill_between(range(len(years)), invested_amounts, total_values, 
                     alpha=0.2, color='#00D9A3')
    
    ax.set_facecolor('#0A0E27')
    ax.set_xlabel('Time Period', color='white', fontsize=12, weight='bold')
    ax.set_ylabel('Amount (₹)', color='white', fontsize=12, weight='bold')
    ax.set_title('Investment Growth Projection', color='white', fontsize=14, weight='bold', pad=15)
    ax.tick_params(colors='white', labelsize=10)
    ax.grid(True, alpha=0.2, color='#2D3748')
    ax.legend(loc='upper left', framealpha=0.9, facecolor='#151B3D', 
             edgecolor='white', labelcolor='white')
    
    # Format y-axis to show currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/1000:.0f}K'))
    
    fig.patch.set_facecolor('#151B3D')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#151B3D')
    buf.seek(0)
    plt.close()
    
    return buf


def generate_portfolio_pdf(portfolio_data):
    """
    Generate a comprehensive PDF report for the portfolio
    
    Args:
        portfolio_data: Dictionary containing portfolio information
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=50, 
        leftMargin=50,
        topMargin=50, 
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#0066FF'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#A0AEC0'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#00D9A3'),
        spaceAfter=15,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#0066FF'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # Header Section
    title = Paragraph("🤖 Finbot Investment Portfolio", title_style)
    elements.append(title)
    
    subtitle = Paragraph(
        f"AI-Powered Investment Strategy | Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    # Executive Summary Box
    elements.append(Paragraph("Executive Summary", heading_style))
    
    summary_data = [
        ['Initial Investment', f"₹{portfolio_data['total_investment']:,}"],
        ['Monthly SIP', f"₹{portfolio_data['monthly_sip']:,}"],
        ['Risk Profile', portfolio_data['risk_level']],
        ['Investment Horizon', '1-5 Years'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7F9FC')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Asset Allocation Section
    elements.append(Paragraph("Asset Allocation Strategy", heading_style))
    
    allocation_data = [['Asset Class', 'Allocation (%)', 'Amount (₹)']]
    for asset, percentage in portfolio_data['allocation'].items():
        amount = (portfolio_data['total_investment'] * percentage) / 100
        allocation_data.append([
            asset.replace('_', ' ').title(), 
            f"{percentage}%",
            f"₹{amount:,.0f}"
        ])
    
    allocation_table = Table(allocation_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    allocation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066FF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7FAFC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    
    elements.append(allocation_table)
    
    # Add pie chart
    try:
        pie_chart_buf = create_pie_chart(portfolio_data['allocation'])
        pie_img = Image(pie_chart_buf, width=4*inch, height=4*inch)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(pie_img)
    except Exception as e:
        elements.append(Paragraph(f"<i>Chart generation unavailable</i>", styles['Normal']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Projected Returns Section
    elements.append(Paragraph("Projected Returns Analysis", heading_style))
    
    returns_data = [['Time Period', 'Total Value', 'Total Invested', 'Expected Gains', 'ROI %']]
    for period, values in sorted(portfolio_data['projected_returns'].items()):
        year = int(period.split('_')[0])
        invested = portfolio_data['total_investment'] + (portfolio_data['monthly_sip'] * 12 * year)
        roi = ((values['gains'] / invested) * 100) if invested > 0 else 0
        
        returns_data.append([
            f"{year} Year{'s' if year > 1 else ''}",
            f"₹{values['total_value']:,.0f}",
            f"₹{invested:,.0f}",
            f"₹{values['gains']:,.0f}",
            f"{roi:.1f}%"
        ])
    
    returns_table = Table(returns_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    returns_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D9A3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7FAFC')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')])
    ]))
    
    elements.append(returns_table)
    
    # Add returns chart
    try:
        returns_chart_buf = create_returns_chart(
            portfolio_data['projected_returns'],
            portfolio_data['total_investment'],
            portfolio_data['monthly_sip']
        )
        returns_img = Image(returns_chart_buf, width=6*inch, height=3.5*inch)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(returns_img)
    except Exception as e:
        elements.append(Paragraph(f"<i>Chart generation unavailable</i>", styles['Normal']))
    
    elements.append(PageBreak())
    
    # Investment Recommendations Section
    if portfolio_data.get('recommendations'):
        elements.append(Paragraph("Investment Recommendations", heading_style))
        
        # Stocks Section
        if 'stocks' in portfolio_data['recommendations']:
            stock_amount = portfolio_data['recommendations']['stocks']['amount']
            elements.append(Paragraph(f"Equity Stocks (₹{stock_amount:,.0f})", subheading_style))
            
            stock_data = [['Symbol', 'Company Name', 'Sector', 'Suggested Allocation']]
            stock_list = portfolio_data['recommendations']['stocks']['list']
            allocation_per_stock = stock_amount / len(stock_list) if stock_list else 0
            
            for stock in stock_list:
                stock_data.append([
                    stock['symbol'],
                    stock['name'][:25],
                    stock['sector'],
                    f"₹{allocation_per_stock:,.0f}"
                ])
            
            stock_table = Table(stock_data, colWidths=[1*inch, 2.5*inch, 1.5*inch, 1.5*inch])
            stock_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFB800')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFBEB')])
            ]))
            
            elements.append(stock_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Mutual Funds Section
        if 'mutual_funds' in portfolio_data['recommendations']:
            mf_amount = portfolio_data['recommendations']['mutual_funds']['amount']
            elements.append(Paragraph(f"Mutual Funds (₹{mf_amount:,.0f})", subheading_style))
            
            mf_data = [['Fund Name', 'Category', '3Y Returns', 'Suggested SIP']]
            mf_list = portfolio_data['recommendations']['mutual_funds']['list']
            sip_per_fund = (portfolio_data['monthly_sip'] * 0.4) / len(mf_list) if mf_list else 0
            
            for fund in mf_list:
                mf_data.append([
                    fund['name'][:30],
                    fund['category'],
                    fund['returns_3y'],
                    f"₹{sip_per_fund:,.0f}/mo"
                ])
            
            mf_table = Table(mf_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1.5*inch])
            mf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066FF')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EFF6FF')])
            ]))
            
            elements.append(mf_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Debt Options Section
        if 'debt' in portfolio_data['recommendations']:
            debt_amount = portfolio_data['recommendations']['debt']['amount']
            elements.append(Paragraph(f"Debt Instruments (₹{debt_amount:,.0f})", subheading_style))
            
            debt_data = [['Instrument', 'Type', 'Interest Rate', 'Suggested Amount']]
            debt_list = portfolio_data['recommendations']['debt']['list']
            allocation_per_debt = debt_amount / len(debt_list) if debt_list else 0
            
            for debt in debt_list:
                debt_data.append([
                    debt['name'][:25],
                    debt['type'],
                    debt.get('interest_rate', 'N/A'),
                    f"₹{allocation_per_debt:,.0f}"
                ])
            
            debt_table = Table(debt_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            debt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')])
            ]))
            
            elements.append(debt_table)
    
    # Key Investment Principles
    elements.append(Spacer(1, 0.4*inch))
    elements.append(Paragraph("Key Investment Principles", heading_style))
    
    principles = [
        "<b>Diversification:</b> Don't put all eggs in one basket. Spread across asset classes.",
        "<b>Regular Monitoring:</b> Review portfolio quarterly and rebalance if needed.",
        "<b>Long-term Focus:</b> Stay invested for the recommended time horizon.",
        "<b>SIP Discipline:</b> Continue monthly investments regardless of market conditions.",
        "<b>Risk Management:</b> Align investments with your risk tolerance and goals."
    ]
    
    for principle in principles:
        elements.append(Paragraph(f"• {principle}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
    
    # Disclaimer
    elements.append(Spacer(1, 0.5*inch))
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#718096'),
        alignment=TA_JUSTIFY,
        borderWidth=1,
        borderColor=colors.HexColor('#CBD5E0'),
        borderPadding=10,
        backColor=colors.HexColor('#F7FAFC')
    )
    
    disclaimer = Paragraph(
        "<b>Important Disclaimer:</b> This portfolio report is generated by an AI-powered advisory system "
        "for educational and informational purposes only. It should not be considered as professional "
        "financial advice. Past performance does not guarantee future results. Investments in securities "
        "markets are subject to market risks. Please read all scheme-related documents carefully and/or "
        "consult with a certified financial advisor before making any investment decisions. The creators "
        "of this system are not liable for any financial losses incurred based on this report.",
        disclaimer_style
    )
    elements.append(disclaimer)
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4A5568'),
        alignment=TA_CENTER,
        spaceAfter=5
    )
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
    elements.append(Paragraph(
        "🤖 <b>Generated by Finbot</b> - AI-Powered Investment Advisor",
        footer_style
    ))
    elements.append(Paragraph(
        f"Report ID: FIN-{datetime.now().strftime('%Y%m%d%H%M%S')} | www.finbot.ai",
        ParagraphStyle('FooterSmall', parent=footer_style, fontSize=8)
    ))
    
    # Build PDF
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf