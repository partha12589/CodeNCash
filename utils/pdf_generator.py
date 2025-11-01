from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

class PortfolioPDFGenerator:
    """Generate professional PDF reports for investment portfolios"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Heading style
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        # Info style
        self.info_style = ParagraphStyle(
            'CustomInfo',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
    
    def generate_pdf(self, portfolio_data):
        """Generate PDF from portfolio data and return as bytes"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        elements = []
        
        # Add title
        elements.append(Paragraph("Investment Portfolio Report", self.title_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add generation date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        elements.append(Paragraph(date_text, self.info_style))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Portfolio Summary Section
        elements.append(Paragraph("Portfolio Summary", self.heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Investment', f"?{portfolio_data['total_investment']:,}"],
            ['Monthly SIP', f"?{portfolio_data['monthly_sip']:,}"],
            ['Risk Level', portfolio_data['risk_level']],
        ]
        summary_table = self.create_table(summary_data, col_widths=[3*inch, 3*inch])
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Asset Allocation Section
        elements.append(Paragraph("Asset Allocation", self.heading_style))
        allocation_data = [['Asset Type', 'Allocation %']]
        for asset_type, percentage in portfolio_data['allocation'].items():
            allocation_data.append([asset_type.replace('_', ' ').title(), f"{percentage}%"])
        allocation_table = self.create_table(allocation_data, col_widths=[3*inch, 3*inch])
        elements.append(allocation_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Projected Returns Section
        elements.append(Paragraph("Projected Returns", self.heading_style))
        returns_data = [['Period', 'Total Value', 'Expected Gains']]
        for period, values in portfolio_data['projected_returns'].items():
            period_name = period.replace("_", " ").title()
            returns_data.append([
                period_name,
                f"?{values['total_value']:,.0f}",
                f"?{values['gains']:,.0f}"
            ])
        returns_table = self.create_table(returns_data, col_widths=[2*inch, 2*inch, 2*inch])
        elements.append(returns_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Investment Recommendations Section
        if portfolio_data.get('recommendations'):
            elements.append(Paragraph("Investment Recommendations", self.heading_style))
            
            # Stocks
            if 'stocks' in portfolio_data['recommendations']:
                stocks_info = portfolio_data['recommendations']['stocks']
                elements.append(Paragraph(
                    f"<b>Stocks</b> (Allocation: ?{stocks_info['amount']:,.0f})",
                    self.normal_style
                ))
                stock_data = [['Symbol', 'Company Name', 'Sector']]
                for stock in stocks_info['list']:
                    stock_data.append([
                        stock['symbol'],
                        stock['name'],
                        stock['sector']
                    ])
                stock_table = self.create_table(stock_data, col_widths=[1.5*inch, 3*inch, 1.5*inch])
                elements.append(stock_table)
                elements.append(Spacer(1, 0.2 * inch))
            
            # Mutual Funds
            if 'mutual_funds' in portfolio_data['recommendations']:
                mf_info = portfolio_data['recommendations']['mutual_funds']
                elements.append(Paragraph(
                    f"<b>Mutual Funds</b> (Allocation: ?{mf_info['amount']:,.0f})",
                    self.normal_style
                ))
                mf_data = [['Fund Name', 'Category', '3Y Returns']]
                for mf in mf_info['list']:
                    mf_data.append([
                        mf['name'],
                        mf['category'],
                        mf['returns_3y']
                    ])
                mf_table = self.create_table(mf_data, col_widths=[3*inch, 1.5*inch, 1.5*inch])
                elements.append(mf_table)
                elements.append(Spacer(1, 0.2 * inch))
            
            # Debt Options
            if 'debt' in portfolio_data['recommendations']:
                debt_info = portfolio_data['recommendations']['debt']
                elements.append(Paragraph(
                    f"<b>Debt Options</b> (Allocation: ?{debt_info['amount']:,.0f})",
                    self.normal_style
                ))
                debt_data = [['Name', 'Type', 'Interest Rate']]
                for debt in debt_info['list']:
                    debt_data.append([
                        debt['name'],
                        debt['type'],
                        debt.get('interest_rate', 'N/A')
                    ])
                debt_table = self.create_table(debt_data, col_widths=[2.5*inch, 2*inch, 1.5*inch])
                elements.append(debt_table)
                elements.append(Spacer(1, 0.2 * inch))
        
        # Add disclaimer
        elements.append(Spacer(1, 0.5 * inch))
        disclaimer = """
        <b>Disclaimer:</b> This report is for informational purposes only and should not be 
        considered as financial advice. Past performance is not indicative of future results. 
        Please consult with a certified financial advisor before making any investment decisions.
        """
        elements.append(Paragraph(disclaimer, self.info_style))
        
        # Footer
        footer_text = "Generated by Finbot - Your Personal Investment Advisor"
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(footer_text, self.info_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def create_table(self, data, col_widths=None):
        """Create a styled table"""
        table = Table(data, colWidths=col_widths)
        
        # Add style to table
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
        ]))
        
        return table
