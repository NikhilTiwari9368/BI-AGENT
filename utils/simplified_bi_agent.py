import google.generativeai as genai
import pandas as pd
import json
from typing import List, Dict, Any, Optional

class SimplifiedBIAgent:
    """
    Simplified Business Intelligence Agent powered by Gemini AI only
    Removes CrewAI dependency to avoid onnxruntime issues
    """
    
    def __init__(self, api_key: str):
        """Initialize the BI Agent with Gemini API only"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
        self.api_key = api_key
    
    def extract_data_from_document(self, content, filename: str) -> Optional[str]:
        """Extract structured data from PDF or text documents"""
        try:
            if filename.endswith('.pdf'):
                text_content = str(content)[:5000]  # Limit content size
            else:
                text_content = content[:5000]
            
            prompt = f"""
            Analyze this document content and extract any structured data, financial metrics, 
            or business information that could be useful for business intelligence analysis.
            
            Focus on:
            - Financial figures (revenue, profit, expenses, ratios)
            - Performance metrics and KPIs
            - Time-series data and trends
            - Key business indicators
            - Operational metrics
            - Market data and comparisons
            
            Document content:
            {text_content}
            
            Please provide a structured summary of the key data points found, 
            formatted for business analysis. Include specific numbers and metrics where available.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Error extracting data from document: {e}")
            return None
    
    def generate_comprehensive_analysis(self, df: pd.DataFrame, goals: List[str]) -> str:
        """Generate comprehensive business analysis using Gemini AI"""
        
        try:
            data_summary = self._get_data_summary(df)
            goals_text = "\n".join([f"- {goal}" for goal in goals])
            
            prompt = f"""
            As a senior business intelligence analyst, provide a comprehensive analysis of this dataset.
            
            Data Summary:
            {data_summary}
            
            Analysis Goals:
            {goals_text}
            
            Please provide a detailed business intelligence report with:
            
            ## Executive Summary
            - Key findings and insights (3-4 bullet points)
            - Critical business metrics and their implications
            - Overall assessment of business performance
            
            ## Detailed Analysis
            - Data quality and completeness assessment
            - Statistical insights and patterns discovered
            - Trend analysis and seasonal patterns
            - Outliers and anomalies identification
            
            ## Financial Performance (if applicable)
            - Revenue and profitability analysis
            - Cost structure and expense analysis
            - Growth trends and year-over-year comparisons
            - Key financial ratios and their interpretation
            
            ## Business Insights
            - Market position and competitive analysis
            - Operational efficiency insights
            - Customer or product performance patterns
            - Risk factors and opportunities identified
            
            ## Recommendations
            - Top 3-5 actionable business recommendations
            - Strategic initiatives to consider
            - Areas requiring immediate attention
            - Long-term strategic considerations
            
            ## Risk Assessment
            - Potential risks identified in the data
            - Mitigation strategies
            - Early warning indicators to monitor
            
            Format your response in clear markdown with headers and bullet points.
            Focus on business value and actionable insights that executives can use for decision-making.
            Use specific numbers and percentages from the data to support your analysis.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating comprehensive analysis: {str(e)}"
    
    def answer_question(self, df: pd.DataFrame, question: str) -> str:
        """Answer specific questions about the data using Gemini"""
        
        try:
            data_summary = self._get_data_summary(df)
            financial_metrics = self._calculate_financial_metrics(df)
            
            prompt = f"""
            You are a senior business analyst with expertise in financial analysis, operations, and strategy.
            Answer this question about the dataset with detailed analysis and insights.
            
            Question: {question}
            
            Dataset Information:
            {data_summary}
            
            Financial Metrics Analysis:
            {financial_metrics}
            
            Please provide:
            1. **Direct Answer** - Clear, specific response to the question
            2. **Supporting Analysis** - Data calculations and evidence
            3. **Context & Interpretation** - What this means for the business
            4. **Business Implications** - How this impacts operations/strategy
            5. **Recommendations** - Suggested actions based on findings
            6. **Additional Insights** - Related observations that add value
            
            Use specific numbers, percentages, and calculations from the data.
            Explain your reasoning and show your work where applicable.
            Focus on business value and actionable insights.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def get_next_step_suggestions(self, completed_goals: List[str]) -> str:
        """Suggest next steps based on completed analysis"""
        try:
            goals_text = "\n".join([f"- {goal}" for goal in completed_goals])
            
            prompt = f"""
            Based on the following completed business intelligence analysis goals:
            
            {goals_text}
            
            Suggest 7-10 logical next steps or follow-up analyses that would provide additional business value:
            
            Consider suggesting:
            - **Deeper Analytics**: More detailed analysis of interesting findings
            - **Predictive Analytics**: Forecasting and trend projection opportunities
            - **Comparative Analysis**: Benchmarking against industry standards or competitors
            - **Operational Improvements**: Process optimization based on data insights
            - **Strategic Initiatives**: Long-term planning based on discovered patterns
            - **Risk Management**: Analysis of potential threats or vulnerabilities
            - **Performance Monitoring**: KPIs and metrics to track going forward
            - **Data Enhancement**: Additional data sources that could provide value
            - **Stakeholder Analysis**: Specific analysis for different business units
            - **ROI Analysis**: Investment and return optimization opportunities
            
            Format as a numbered list with brief explanations of business value for each suggestion.
            Prioritize suggestions by potential business impact.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return "Unable to generate suggestions at this time."
    
    def generate_financial_deep_dive(self, df: pd.DataFrame) -> str:
        """Generate specialized financial analysis"""
        
        try:
            data_summary = self._get_data_summary(df)
            financial_metrics = self._calculate_financial_metrics(df)
            
            prompt = f"""
            Perform a comprehensive financial deep-dive analysis as a senior financial analyst:
            
            {data_summary}
            
            Current Financial Metrics:
            {financial_metrics}
            
            Provide detailed analysis on:
            
            ## Revenue Analysis
            - Revenue trends and growth patterns
            - Revenue diversification and concentration
            - Seasonal revenue patterns
            - Revenue per unit/customer analysis
            
            ## Profitability Analysis
            - Gross, operating, and net profit margins
            - Profit trend analysis and sustainability
            - Cost of goods sold analysis
            - Operating leverage analysis
            
            ## Expense Management
            - Expense structure breakdown
            - Fixed vs variable cost analysis
            - Expense growth rates vs revenue growth
            - Cost efficiency metrics
            
            ## Financial Health Indicators
            - Liquidity analysis and cash flow patterns
            - Leverage and debt analysis
            - Working capital management
            - Financial stability indicators
            
            ## Performance Ratios
            - Return on Assets (ROA)
            - Return on Equity (ROE)
            - Return on Investment (ROI)
            - Asset turnover ratios
            - Efficiency ratios
            
            ## Growth Analysis
            - Historical growth rates (revenue, profit, assets)
            - Compound Annual Growth Rate (CAGR)
            - Growth sustainability analysis
            - Market share and competitive position
            
            ## Risk Assessment
            - Financial risk factors identified
            - Volatility and stability analysis
            - Credit risk indicators
            - Market risk exposure
            
            ## Valuation Insights
            - Key valuation metrics
            - Peer comparison opportunities
            - Value drivers identification
            - Investment attractiveness
            
            Provide specific calculations and business interpretations for each section.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error in financial analysis: {str(e)}"
    
    def _get_data_summary(self, df: pd.DataFrame) -> str:
        """Generate a comprehensive data summary"""
        summary = f"""
        Dataset Overview:
        - Rows: {len(df):,}
        - Columns: {len(df.columns)}
        - Column Names: {', '.join(df.columns.tolist())}
        
        Data Types:
        {df.dtypes.to_string()}
        
        Missing Values Summary:
        {df.isnull().sum().to_string()}
        
        Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
        """
        
        # Numerical summary
        if len(df.select_dtypes(include=['number']).columns) > 0:
            summary += f"""
        
        Numerical Columns Statistical Summary:
        {df.describe().round(2).to_string()}
        """
        
        # Categorical summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary += "\n\nCategorical Columns Summary:"
            for col in categorical_cols[:3]:  # Limit to first 3
                unique_count = df[col].nunique()
                top_values = df[col].value_counts().head(3)
                summary += f"\n{col}: {unique_count} unique values, Top 3: {top_values.to_dict()}"
        
        # Sample data
        summary += f"""
        
        Sample Data (First 3 rows):
        {df.head(3).to_string()}
        """
        
        return summary
    
    def _calculate_financial_metrics(self, df: pd.DataFrame) -> str:
        """Calculate comprehensive financial metrics if relevant columns exist"""
        metrics = []
        
        # Common financial column patterns
        revenue_cols = [col for col in df.columns if any(term in col.lower() for term in 
                       ['revenue', 'sales', 'income', 'turnover', 'receipts'])]
        profit_cols = [col for col in df.columns if any(term in col.lower() for term in 
                      ['profit', 'earnings', 'net_income', 'ebitda', 'operating_income'])]
        expense_cols = [col for col in df.columns if any(term in col.lower() for term in 
                       ['expense', 'cost', 'expenditure', 'spending', 'cogs'])]
        asset_cols = [col for col in df.columns if any(term in col.lower() for term in 
                     ['asset', 'capital', 'investment', 'property'])]
        equity_cols = [col for col in df.columns if any(term in col.lower() for term in 
                      ['equity', 'shareholder', 'retained_earnings'])]
        
        try:
            # Revenue analysis
            if revenue_cols:
                for col in revenue_cols:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        total_revenue = df[col].sum()
                        avg_revenue = df[col].mean()
                        revenue_growth = self._calculate_growth_rate(df, col)
                        
                        metrics.append(f"Revenue Analysis ({col}):")
                        metrics.append(f"  - Total Revenue: ${total_revenue:,.2f}")
                        metrics.append(f"  - Average Revenue: ${avg_revenue:,.2f}")
                        if revenue_growth is not None:
                            metrics.append(f"  - Growth Rate: {revenue_growth:.2f}%")
            
            # Profit analysis
            if profit_cols:
                for col in profit_cols:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        total_profit = df[col].sum()
                        avg_profit = df[col].mean()
                        profit_growth = self._calculate_growth_rate(df, col)
                        
                        metrics.append(f"\nProfit Analysis ({col}):")
                        metrics.append(f"  - Total Profit: ${total_profit:,.2f}")
                        metrics.append(f"  - Average Profit: ${avg_profit:,.2f}")
                        if profit_growth is not None:
                            metrics.append(f"  - Growth Rate: {profit_growth:.2f}%")
            
            # Calculate financial ratios
            if revenue_cols and profit_cols:
                metrics.append("\nFinancial Ratios:")
                for rev_col in revenue_cols:
                    for prof_col in profit_cols:
                        if (pd.api.types.is_numeric_dtype(df[rev_col]) and 
                            pd.api.types.is_numeric_dtype(df[prof_col])):
                            total_revenue = df[rev_col].sum()
                            total_profit = df[prof_col].sum()
                            
                            if total_revenue > 0:
                                profit_margin = (total_profit / total_revenue) * 100
                                metrics.append(f"  - Profit Margin ({prof_col}/{rev_col}): {profit_margin:.2f}%")
            
            # Return ratios
            if profit_cols and asset_cols:
                metrics.append("\nReturn Ratios:")
                for prof_col in profit_cols:
                    for asset_col in asset_cols:
                        if (pd.api.types.is_numeric_dtype(df[prof_col]) and 
                            pd.api.types.is_numeric_dtype(df[asset_col])):
                            total_profit = df[prof_col].sum()
                            total_assets = df[asset_col].sum()
                            
                            if total_assets > 0:
                                roa = (total_profit / total_assets) * 100
                                metrics.append(f"  - ROA ({prof_col}/{asset_col}): {roa:.2f}%")
            
            # Additional efficiency metrics
            if len(df.select_dtypes(include=['number']).columns) > 1:
                numeric_cols = df.select_dtypes(include=['number']).columns
                correlations = df[numeric_cols].corr()
                
                # Find strong correlations
                strong_corrs = []
                for i, col1 in enumerate(numeric_cols):
                    for j, col2 in enumerate(numeric_cols):
                        if i < j and abs(correlations.iloc[i, j]) > 0.7:
                            strong_corrs.append(f"{col1} & {col2}: {correlations.iloc[i, j]:.3f}")
                
                if strong_corrs:
                    metrics.append("\nStrong Correlations (|r| > 0.7):")
                    for corr in strong_corrs[:5]:  # Limit to top 5
                        metrics.append(f"  - {corr}")
        
        except Exception as e:
            metrics.append(f"Error calculating financial metrics: {str(e)}")
        
        return "\n".join(metrics) if metrics else "No financial metrics could be calculated from available data"
    
    def _calculate_growth_rate(self, df: pd.DataFrame, column: str) -> Optional[float]:
        """Calculate growth rate for a column if time data is available"""
        try:
            # Look for date columns
            date_cols = df.select_dtypes(include=['datetime64']).columns
            if len(date_cols) == 0:
                # Try to find columns that might be dates
                for col in df.columns:
                    if any(term in col.lower() for term in ['date', 'time', 'year', 'month']):
                        try:
                            df[col] = pd.to_datetime(df[col])
                            date_cols = [col]
                            break
                        except:
                            continue
            
            if len(date_cols) > 0 and len(df) > 1:
                df_sorted = df.sort_values(date_cols[0])
                first_value = df_sorted[column].iloc[0]
                last_value = df_sorted[column].iloc[-1]
                
                if first_value > 0:
                    growth_rate = ((last_value - first_value) / first_value) * 100
                    return growth_rate
            
            return None
            
        except Exception:
            return None
    
    def generate_executive_summary(self, df: pd.DataFrame) -> str:
        """Generate an executive summary of the dataset"""
        try:
            data_summary = self._get_data_summary(df)
            financial_metrics = self._calculate_financial_metrics(df)
            
            prompt = f"""
            Create a concise executive summary for this business dataset suitable for C-level executives.
            
            Dataset Information:
            {data_summary}
            
            Financial Analysis:
            {financial_metrics}
            
            The executive summary should include:
            
            ## Key Performance Highlights
            - Top 3-4 most important business metrics and their current status
            - Notable achievements or concerning trends
            
            ## Financial Performance Overview
            - Revenue and profitability summary
            - Key financial ratios and their implications
            - Year-over-year or period-over-period changes
            
            ## Strategic Insights
            - Most significant business insights discovered
            - Competitive position indicators
            - Market opportunities or threats identified
            
            ## Critical Action Items
            - Top 3 immediate priorities requiring executive attention
            - Strategic initiatives to consider
            - Risk mitigation requirements
            
            ## Bottom Line Impact
            - Overall business health assessment
            - Financial outlook based on current trends
            - Recommended strategic direction
            
            Keep the summary under 300 words, focusing on business impact and executive-level decisions.
            Use specific numbers and percentages where possible.
            Write in a clear, professional tone suitable for board presentations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating executive summary: {str(e)}"
