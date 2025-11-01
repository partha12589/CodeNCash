import os
from groq import Groq
from dotenv import load_dotenv
import base64
from PIL import Image
import io
import pandas as pd
from pathlib import Path

load_dotenv()

class EnhancedChatHandler:
    """Enhanced chat handler with file and image processing"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.3-70b-versatile"
        else:
            self.client = None
        
        self.conversation_history = []
    
    def get_response(self, user_message, context="", files=None, images=None):
        """
        Get AI response with optional file/image context
        Args:
            user_message: User's text message
            context: Additional context (portfolio data, user profile)
            files: List of uploaded files (CSV, Excel, PDF)
            images: List of uploaded images
        Returns:
            AI response
        """
        if not self.client:
            return "Please add your GROQ_API_KEY to the .env file to enable AI responses."
        
        system_prompt = """You are CodeNCash AI, an expert Indian investment advisor and financial planner. 
        You help users with:
        - Investment advice for Indian markets (NSE/BSE)
        - Mutual funds, stocks, debt funds, bonds
        - Tax planning under Indian tax laws (80C, 80D, etc.)
        - Retirement planning, child education, goal-based planning
        - SIP calculations and portfolio analysis
        - Reading and analyzing financial documents, statements, and portfolios
        
        Provide clear, practical, and actionable advice tailored to Indian investors.
        Be concise, friendly, and use emojis appropriately.
        When analyzing documents or images, extract all relevant financial information."""
        
        # Build message with file/image context
        enhanced_message = user_message
        
        # Process uploaded files
        if files:
            file_context = self._process_files(files)
            if file_context:
                enhanced_message += f"\n\n[File Context]\n{file_context}"
        
        # Process uploaded images
        if images:
            image_context = self._process_images(images)
            if image_context:
                enhanced_message += f"\n\n[Image Context]\n{image_context}"
        
        try:
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history (last 5 messages for context)
            if self.conversation_history:
                messages.extend(self.conversation_history[-10:])
            
            # Add context if provided
            if context:
                messages.append({"role": "assistant", "content": f"[User Profile] {context}"})
            
            # Add current message
            messages.append({"role": "user", "content": enhanced_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Keep only last 10 messages
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_response
        
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def _process_files(self, files):
        """Process uploaded files (CSV, Excel, PDF, TXT)"""
        file_context = []
        
        for uploaded_file in files:
            try:
                file_extension = Path(uploaded_file.name).suffix.lower()
                
                if file_extension == '.csv':
                    context = self._process_csv(uploaded_file)
                    file_context.append(context)
                
                elif file_extension in ['.xlsx', '.xls']:
                    context = self._process_excel(uploaded_file)
                    file_context.append(context)
                
                elif file_extension == '.txt':
                    context = self._process_text(uploaded_file)
                    file_context.append(context)
                
                elif file_extension == '.pdf':
                    context = f"PDF file '{uploaded_file.name}' uploaded. Contains financial documents."
                    file_context.append(context)
            
            except Exception as e:
                file_context.append(f"Error processing {uploaded_file.name}: {str(e)}")
        
        return "\n\n".join(file_context) if file_context else None
    
    def _process_csv(self, file):
        """Process CSV file"""
        try:
            df = pd.read_csv(file)
            
            summary = f"CSV File: {file.name}\n"
            summary += f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
            summary += f"Columns: {', '.join(df.columns.tolist())}\n\n"
            
            # Check if it's a portfolio/investment file
            portfolio_keywords = ['stock', 'fund', 'investment', 'quantity', 'price', 'value', 'amount']
            is_portfolio = any(keyword in ' '.join(df.columns).lower() for keyword in portfolio_keywords)
            
            if is_portfolio:
                summary += "This appears to be a portfolio/investment file.\n"
                
                # Try to calculate totals
                value_columns = [col for col in df.columns if 'value' in col.lower() or 'amount' in col.lower()]
                if value_columns:
                    for col in value_columns:
                        try:
                            total = df[col].sum()
                            summary += f"Total {col}: ₹{total:,.2f}\n"
                        except:
                            pass
            
            # Show first few rows
            summary += f"\nFirst few entries:\n{df.head(5).to_string()}"
            
            return summary
        
        except Exception as e:
            return f"Error reading CSV: {str(e)}"
    
    def _process_excel(self, file):
        """Process Excel file"""
        try:
            df = pd.read_excel(file)
            
            summary = f"Excel File: {file.name}\n"
            summary += f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
            summary += f"Columns: {', '.join(df.columns.tolist())}\n\n"
            
            # Check for portfolio data
            portfolio_keywords = ['stock', 'fund', 'investment', 'quantity', 'price', 'value']
            is_portfolio = any(keyword in ' '.join(df.columns).lower() for keyword in portfolio_keywords)
            
            if is_portfolio:
                summary += "This appears to be a portfolio/investment file.\n"
                
                value_columns = [col for col in df.columns if 'value' in col.lower() or 'amount' in col.lower()]
                if value_columns:
                    for col in value_columns:
                        try:
                            total = df[col].sum()
                            summary += f"Total {col}: ₹{total:,.2f}\n"
                        except:
                            pass
            
            summary += f"\nFirst few entries:\n{df.head(5).to_string()}"
            
            return summary
        
        except Exception as e:
            return f"Error reading Excel: {str(e)}"
    
    def _process_text(self, file):
        """Process text file"""
        try:
            content = file.read().decode('utf-8')
            
            summary = f"Text File: {file.name}\n"
            summary += f"Length: {len(content)} characters\n\n"
            
            # Show content (truncated if too long)
            if len(content) > 1000:
                summary += f"Content (first 1000 chars):\n{content[:1000]}..."
            else:
                summary += f"Content:\n{content}"
            
            return summary
        
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def _process_images(self, images):
        """Process uploaded images"""
        image_context = []
        
        for uploaded_image in images:
            try:
                # Open image
                image = Image.open(uploaded_image)
                
                # Get basic info
                width, height = image.size
                format_name = image.format
                
                context = f"Image: {uploaded_image.name}\n"
                context += f"Size: {width}x{height}, Format: {format_name}\n"
                context += "This appears to be a financial document/screenshot. "
                context += "Please analyze the visible text, numbers, and data for investment insights."
                
                image_context.append(context)
            
            except Exception as e:
                image_context.append(f"Error processing image {uploaded_image.name}: {str(e)}")
        
        return "\n\n".join(image_context) if image_context else None
    
    def analyze_portfolio_file(self, file):
        """
        Specialized analysis for portfolio files
        Args:
            file: Uploaded CSV/Excel file with portfolio data
        Returns:
            Dict with portfolio analysis
        """
        try:
            file_extension = Path(file.name).suffix.lower()
            
            if file_extension == '.csv':
                df = pd.read_csv(file)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file)
            else:
                return {'error': 'Unsupported file format. Please upload CSV or Excel.'}
            
            analysis = {
                'file_name': file.name,
                'total_holdings': len(df),
                'columns': df.columns.tolist()
            }
            
            # Try to identify key columns
            quantity_col = None
            value_col = None
            name_col = None
            
            for col in df.columns:
                col_lower = col.lower()
                if 'quantity' in col_lower or 'units' in col_lower:
                    quantity_col = col
                if 'value' in col_lower or 'amount' in col_lower or 'current' in col_lower:
                    value_col = col
                if 'name' in col_lower or 'stock' in col_lower or 'fund' in col_lower:
                    name_col = col
            
            # Calculate totals
            if value_col:
                try:
                    total_value = df[value_col].sum()
                    analysis['total_portfolio_value'] = round(total_value, 2)
                    
                    # Top holdings
                    top_holdings = df.nlargest(5, value_col)[[name_col, value_col]] if name_col else df.nlargest(5, value_col)
                    analysis['top_holdings'] = top_holdings.to_dict('records')
                except:
                    pass
            
            return analysis
        
        except Exception as e:
            return {'error': f'Error analyzing portfolio: {str(e)}'}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []