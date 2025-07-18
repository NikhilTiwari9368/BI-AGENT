from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import os

class BICrewAI:
    """
    Business Intelligence Crew using CrewAI for advanced analysis
    """
    
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        self.setup_agents()
    
    def setup_agents(self):
        """Setup specialized AI agents for different BI tasks"""
        
        # Data Analyst Agent
        self.data_analyst = Agent(
            role='Senior Data Analyst',
            goal='Analyze datasets to identify patterns, trends, and insights',
            backstory="""You are a senior data analyst with 10+ years of experience in 
                        business intelligence. You excel at finding meaningful patterns in data 
                        and translating complex analysis into business insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Financial Analyst Agent
        self.financial_analyst = Agent(
            role='Financial Analyst',
            goal='Perform financial analysis and calculate key financial metrics',
            backstory="""You are a certified financial analyst specializing in corporate 
                        finance, ratio analysis, and financial performance evaluation. 
                        You can interpret financial statements and identify financial trends.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Business Intelligence Specialist
        self.bi_specialist = Agent(
            role='Business Intelligence Specialist',
            goal='Provide strategic insights and recommendations based on data analysis',
            backstory="""You are a business intelligence specialist who transforms data 
                        insights into actionable business strategies. You understand market 
                        dynamics and can recommend data-driven decisions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Report Writer Agent
        self.report_writer = Agent(
            role='Business Report Writer',
            goal='Create comprehensive business reports with clear insights and recommendations',
            backstory="""You are an expert business report writer who can synthesize complex 
                        analysis into clear, executive-level reports with actionable insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def analyze_dataset(self, df: pd.DataFrame, analysis_goals: list) -> str:
        """
        Use CrewAI to perform comprehensive dataset analysis
        """
        
        # Prepare data summary
        data_summary = self._prepare_data_summary(df)
        goals_text = "\n".join([f"- {goal}" for goal in analysis_goals])
        
        # Define tasks
        data_analysis_task = Task(
            description=f"""
            Analyze this dataset and provide detailed insights:
            
            Dataset Summary:
            {data_summary}
            
            Analysis Goals:
            {goals_text}
            
            Please provide:
            1. Data quality assessment
            2. Key patterns and trends identified
            3. Statistical insights
            4. Notable outliers or anomalies
            5. Data relationships and correlations
            """,
            agent=self.data_analyst,
            expected_output="Detailed data analysis with specific findings and statistical insights"
        )
        
        financial_analysis_task = Task(
            description=f"""
            Based on the dataset analysis, perform financial analysis:
            
            {data_summary}
            
            Focus on:
            1. Financial performance metrics
            2. Profitability analysis
            3. Growth trends
            4. Financial ratios (if applicable)
            5. Revenue and cost analysis
            6. Year-over-year comparisons
            """,
            agent=self.financial_analyst,
            expected_output="Comprehensive financial analysis with key metrics and ratios"
        )
        
        business_insights_task = Task(
            description=f"""
            Provide strategic business insights based on the data and financial analysis.
            
            Analysis Goals:
            {goals_text}
            
            Deliver:
            1. Strategic insights
            2. Business opportunities identified
            3. Risk assessment
            4. Market position analysis
            5. Competitive advantages/disadvantages
            6. Actionable recommendations
            """,
            agent=self.bi_specialist,
            expected_output="Strategic business insights with actionable recommendations"
        )
        
        report_generation_task = Task(
            description=f"""
            Create a comprehensive executive summary report combining all analysis.
            
            Include:
            1. Executive Summary (key findings in 3-4 bullet points)
            2. Detailed Analysis Results
            3. Financial Performance Overview
            4. Strategic Recommendations
            5. Risk Factors and Mitigation
            6. Next Steps
            
            Format the report professionally for executive review.
            """,
            agent=self.report_writer,
            expected_output="Professional executive report with clear structure and insights"
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[self.data_analyst, self.financial_analyst, self.bi_specialist, self.report_writer],
            tasks=[data_analysis_task, financial_analysis_task, business_insights_task, report_generation_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Error in CrewAI analysis: {str(e)}"
    
    def financial_deep_dive(self, df: pd.DataFrame) -> str:
        """
        Specialized financial analysis using CrewAI
        """
        
        data_summary = self._prepare_data_summary(df)
        
        financial_task = Task(
            description=f"""
            Perform a comprehensive financial deep-dive analysis:
            
            {data_summary}
            
            Analyze:
            1. Revenue trends and growth patterns
            2. Profit margins and profitability
            3. Expense structure and cost analysis
            4. Return on investment metrics
            5. Liquidity and solvency ratios
            6. Efficiency ratios
            7. Market valuation metrics
            8. Financial health indicators
            9. Year-over-year performance
            10. Quarterly/seasonal patterns
            
            Provide specific calculations and business implications for each metric.
            """,
            agent=self.financial_analyst,
            expected_output="Detailed financial analysis with specific calculations and business implications"
        )
        
        crew = Crew(
            agents=[self.financial_analyst],
            tasks=[financial_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Error in financial analysis: {str(e)}"
    
    def answer_business_question(self, df: pd.DataFrame, question: str) -> str:
        """
        Answer specific business questions using CrewAI
        """
        
        data_summary = self._prepare_data_summary(df)
        
        question_task = Task(
            description=f"""
            Answer this specific business question using the dataset:
            
            Question: {question}
            
            Dataset Information:
            {data_summary}
            
            Provide:
            1. Direct answer to the question
            2. Supporting data and calculations
            3. Context and background
            4. Business implications
            5. Additional insights related to the question
            6. Recommendations based on the findings
            
            Be specific and use actual data points when possible.
            """,
            agent=self.bi_specialist,
            expected_output="Comprehensive answer with supporting data and business implications"
        )
        
        crew = Crew(
            agents=[self.bi_specialist],
            tasks=[question_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def _prepare_data_summary(self, df: pd.DataFrame) -> str:
        """Prepare comprehensive data summary for analysis"""
        
        # Basic info
        basic_info = f"""
        Dataset Overview:
        - Rows: {len(df)}
        - Columns: {len(df.columns)}
        - Column Names: {', '.join(df.columns.tolist())}
        """
        
        # Data types
        dtype_info = f"""
        Data Types:
        {df.dtypes.to_string()}
        """
        
        # Missing values
        missing_info = f"""
        Missing Values:
        {df.isnull().sum().to_string()}
        """
        
        # Statistical summary for numerical columns
        if len(df.select_dtypes(include=['number']).columns) > 0:
            stats_info = f"""
            Statistical Summary:
            {df.describe().to_string()}
            """
        else:
            stats_info = "\nStatistical Summary: No numerical columns found"
        
        # Sample data
        sample_info = f"""
        Sample Data (First 5 rows):
        {df.head().to_string()}
        """
        
        # Value counts for categorical columns (top categories)
        categorical_info = "\nCategorical Column Summaries:\n"
        for col in df.select_dtypes(include=['object']).columns[:3]:  # Limit to 3 columns
            top_values = df[col].value_counts().head(5)
            categorical_info += f"\n{col} - Top 5 values:\n{top_values.to_string()}\n"
        
        return basic_info + dtype_info + missing_info + stats_info + sample_info + categorical_info
    
    def generate_recommendations(self, analysis_results: str) -> str:
        """
        Generate strategic recommendations based on analysis results
        """
        
        recommendation_task = Task(
            description=f"""
            Based on the following analysis results, generate strategic business recommendations:
            
            Analysis Results:
            {analysis_results}
            
            Provide:
            1. Top 5 strategic recommendations
            2. Implementation priorities (High/Medium/Low)
            3. Expected impact of each recommendation
            4. Resource requirements
            5. Timeline for implementation
            6. Success metrics to track
            7. Potential risks and mitigation strategies
            
            Focus on actionable, data-driven recommendations.
            """,
            agent=self.bi_specialist,
            expected_output="Prioritized strategic recommendations with implementation details"
        )
        
        crew = Crew(
            agents=[self.bi_specialist],
            tasks=[recommendation_task],
            verbose=True,
            process=Process.sequential
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"
