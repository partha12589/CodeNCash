"""
PDF Portfolio Generator for CodeNCash
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_portfolio_pdf(portfolio_data):
    """
    Generate a PDF report for the portfolio
    
    Args:
        portfolio_data: Dictionary containing portfolio information
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066FF'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#00D9A3'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph("💰 CodeNCash Investment Portfolio", title_style)
    elements.append(title)
    
    # Date
    date_text = Paragraph(f"<i>Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>", 
                         styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Portfolio Overview
    elements.append(Paragraph("Portfolio Overview", heading_style))
    
    overview_data = [
        ['Total Investment', f"₹{portfolio_data['total_investment']:,}"],
        ['Monthly SIP', f"₹{portfolio_data['monthly_sip']:,}"],
        ['Risk Level', portfolio_data['risk_level']],
    ]
    
    overview_table = Table(overview_data, colWidths=[3*inch, 3*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7F9FC')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(overview_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Asset Allocation
    elements.append(Paragraph("Asset Allocation", heading_style))
    
    allocation_data = [['Asset Class', 'Allocation %']]
    for asset, percentage in portfolio_data['allocation'].items():
        allocation_data.append([asset.replace('_', ' ').title(), f"{percentage}%"])
    
    allocation_table = Table(allocation_data, colWidths=[3*inch, 3*inch])
    allocation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066FF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(allocation_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Projected Returns
    elements.append(Paragraph("Projected Returns", heading_style))
    
    returns_data = [['Time Period', 'Total Value', 'Expected Gains']]
    for period, values in portfolio_data['projected_returns'].items():
        period_name = period.replace('_', ' ').title()
        returns_data.append([
            period_name,
            f"₹{values['total_value']:,.0f}",
            f"₹{values['gains']:,.0f}"
        ])
    
    returns_table = Table(returns_data, colWidths=[2*inch, 2*inch, 2*inch])
    returns_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D9A3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(returns_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Investment Recommendations
    if portfolio_data.get('recommendations'):
        elements.append(Paragraph("Investment Recommendations", heading_style))
        
        # Stocks
        if 'stocks' in portfolio_data['recommendations']:
            stock_amount = portfolio_data['recommendations']['stocks']['amount']
            elements.append(Paragraph(f"<b>Stocks (₹{stock_amount:,.0f})</b>", styles['Normal']))
            
            stock_data = [['Symbol', 'Company Name', 'Sector']]
            for stock in portfolio_data['recommendations']['stocks']['list']:
                stock_data.append([
                    stock['symbol'],
                    stock['name'],
                    stock['sector']
                ])
            
            stock_table = Table(stock_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
            stock_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFB800')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(stock_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Mutual Funds
        if 'mutual_funds' in portfolio_data['recommendations']:
            mf_amount = portfolio_data['recommendations']['mutual_funds']['amount']
            elements.append(Paragraph(f"<b>Mutual Funds (₹{mf_amount:,.0f})</b>", styles['Normal']))
            
            mf_data = [['Fund Name', 'Category', '3Y Returns']]
            for fund in portfolio_data['recommendations']['mutual_funds']['list']:
                mf_data.append([
                    fund['name'],
                    fund['category'],
                    fund['returns_3y']
                ])
            
            mf_table = Table(mf_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            mf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFB800')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            elements.append(mf_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Footer/Disclaimer
    elements.append(Spacer(1, 0.5*inch))
    disclaimer = Paragraph(
        "<i>Disclaimer: This portfolio is for educational purposes only. "
        "Please consult a certified financial advisor before making investment decisions. "
        "Past performance does not guarantee future results.</i>",
        styles['Normal']
    )
    elements.append(disclaimer)
    
    footer = Paragraph(
        "<i>Generated by CodeNCash - AI-Powered Investment Advisor</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, textColor=colors.grey)
    )
    elements.append(Spacer(1, 0.2*inch))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf