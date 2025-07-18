import google.generativeai as genai
import pandas as pd
import json

def get_chart_summary(prompt, api_key):
    """Get a summary or analysis from Gemini AI"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

def get_data_analysis(df, api_key):
    """Get comprehensive data analysis from Gemini"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Prepare data summary
    data_preview = df.head(5).to_string()
    data_info = f"""
    Dataset Info:
    - Shape: {df.shape}
    - Columns: {', '.join(df.columns)}
    - Data Types: {df.dtypes.to_dict()}
    
    Sample Data:
    {data_preview}
    
    Statistical Summary:
    {df.describe().to_string() if len(df.select_dtypes(include=['number']).columns) > 0 else 'No numerical columns'}
    """
    
    prompt = f"""
    Analyze this dataset and provide insights:
    
    {data_info}
    
    Please provide:
    1. Key observations about the data structure
    2. Notable patterns or trends
    3. Data quality assessment
    4. Potential areas for deeper analysis
    5. Business insights if applicable
    
    Keep the analysis concise but comprehensive.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def get_insights(df, analysis_goals, api_key):
    """Generate specific insights based on analysis goals"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    data_summary = f"""
    Dataset Summary:
    - Rows: {len(df)}
    - Columns: {', '.join(df.columns)}
    - Sample: {df.head(3).to_string()}
    """
    
    goals_text = '\n'.join([f"- {goal}" for goal in analysis_goals])
    
    prompt = f"""
    Based on this dataset and the analysis goals, provide specific insights:
    
    {data_summary}
    
    Analysis Goals:
    {goals_text}
    
    For each goal, provide:
    1. Relevant findings from the data
    2. Supporting calculations or observations
    3. Business implications
    4. Recommendations
    
    Format your response with clear sections for each goal.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def get_financial_analysis(df, api_key):
    """Generate financial analysis and ratios"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Identify potential financial columns
    financial_keywords = ['revenue', 'profit', 'sales', 'income', 'expense', 'cost', 
                         'asset', 'liability', 'equity', 'cash', 'debt']
    
    financial_cols = []
    for col in df.columns:
        if any(keyword in col.lower() for keyword in financial_keywords):
            financial_cols.append(col)
    
    data_info = f"""
    Dataset shape: {df.shape}
    Potential financial columns: {financial_cols}
    
    Sample data:
    {df.head(3).to_string()}
    
    Statistical summary of numerical columns:
    {df.select_dtypes(include=['number']).describe().to_string()}
    """
    
    prompt = f"""
    Perform a financial analysis on this dataset:
    
    {data_info}
    
    Please analyze:
    1. Revenue and profitability trends
    2. Key financial ratios (if calculable)
    3. Growth rates and patterns
    4. Financial health indicators
    5. Year-over-year comparisons (if time data exists)
    6. Cost structure analysis
    7. Return on investment metrics
    
    Provide specific calculations and business interpretations.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def get_chart_recommendations(df, api_key):
    """Get chart recommendations from Gemini AI"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    sample = df.head(10).to_markdown(index=False)

    prompt = f"""
    You are a data visualization expert.

    Here is a preview of a cleaned dataset:

    {sample}

    Your task:
    1. Suggest 3–5 useful charts to visualize this data.
    2. For each chart, return:
       - chart_type (Bar, Pie, Donut, Line, Column, etc.)
       - x (column for x-axis)
       - y (column for y-axis, if applicable)
       - reason (why this chart is helpful)

    Respond in **valid JSON array** like:
    [
      {{
        "chart_type": "Bar",
        "x": "Region",
        "y": "Sales",
        "reason": "To compare total sales across regions."
      }},
      ...
    ]
    Don't use ```json``` to wrap the JSON, just return it as-is.
    Only return the JSON array — no text, no markdown.
    """

    response = model.generate_content(prompt)
    return response.text
