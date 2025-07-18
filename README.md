# Business Intelligence Agent

A comprehensive Business Intelligence Agent powered by Gemini AI and CrewAI that automates data analysis, generates insights, and provides interactive Q&A capabilities for business data.

## Features

### 🚀 Complete BI Workflow
- **Step 1: Data Input** - Upload CSV, Excel, PDF, or text files with automatic validation
- **Step 2: Data Analysis & Preprocessing** - Automatic data cleaning, type detection, and quality assessment
- **Step 3: Goal Definition** - Define analysis objectives with guided templates
- **Step 4: Results Presentation** - Interactive dashboards, KPIs, and AI-powered visualizations
- **Step 5: Q&A Analysis** - Answer specific business questions about your data
- **Step 6: Feedback & Iteration** - Continuous improvement and additional analysis

### 🤖 AI-Powered Features
- **Gemini AI Integration** - Advanced natural language processing for insights
- **Smart Chart Generation** - AI-recommended visualizations based on data patterns
- **Financial Analysis** - Automated calculation of key financial ratios and metrics
- **Executive Summaries** - C-level ready reports and recommendations
- **Intelligent Q&A** - Natural language queries about your business data

### 📊 Advanced Analytics
- **KPI Dashboards** - Interactive performance indicators with filtering
- **Trend Analysis** - Time-series analysis and growth calculations
- **Correlation Analysis** - Statistical relationships and pattern discovery
- **Financial Ratios** - ROA, ROE, profit margins, and efficiency metrics
- **Risk Assessment** - Automated identification of business risks and opportunities

### 💼 Business Intelligence Capabilities
- Year-over-year growth analysis
- Revenue and profitability trends
- Cost structure optimization
- Market share and competitive analysis
- Operational efficiency insights
- Customer and product performance
- Seasonal pattern identification

## Installation

### Prerequisites
- Python 3.8 or higher
- Gemini API key (provided: `AIzaSyDzTSzogzG7ntlLHBOoHISaKC12g4ljW-s`)

### Quick Setup (Recommended)

**Option 1: Automated Setup**
1. **Run the setup script**
   ```bash
   setup_and_run.bat
   ```
   This will automatically install dependencies, generate sample data, and start the application.

**Option 2: Manual Setup**
1. **Navigate to the project directory**
   ```bash
   cd "c:\Users\DELL\Downloads\BI PP"
   ```

2. **Install minimal dependencies (recommended to avoid conflicts)**
   ```bash
   pip install -r requirements_minimal.txt
   ```

3. **Generate sample data for testing**
   ```bash
   python -c "from utils.sample_data_generator import save_sample_datasets; save_sample_datasets()"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The Gemini API key is already configured in the application

### Troubleshooting Installation Issues

If you encounter the `onnxruntime` error:
- Use `requirements_minimal.txt` instead of `requirements.txt`
- This removes CrewAI dependencies that cause conflicts
- The application will work with Gemini AI only (still full-featured)

## Usage Guide

### Getting Started

1. **Upload Your Data**
   - Supported formats: CSV, Excel (.xlsx, .xls), PDF, TXT
   - Maximum file size: 50MB
   - The system automatically validates file compatibility

2. **Review Data Processing**
   - View data quality summary and column types
   - Check for missing values and duplicates
   - Review cleaned data preview

3. **Define Analysis Goals**
   - Choose from predefined templates:
     - Revenue trends analysis
     - Top-performing products/categories
     - Financial ratios calculation
     - Year-over-year growth analysis
     - Customer segmentation
     - Seasonal patterns
   - Or provide custom analysis requirements

4. **Explore Results**
   - Interactive KPI dashboard with filtering
   - AI-recommended visualizations
   - Statistical analysis and correlations
   - Comprehensive business insights

5. **Ask Questions**
   - Common questions provided:
     - "What is the YoY growth in revenue?"
     - "What is the return on capital employed?"
     - "Calculate debt-to-equity ratio"
     - "Show profit margin trends"
   - Ask custom questions about your data

6. **Export and Share**
   - Download cleaned data as CSV
   - Export analysis reports
   - Share insights with stakeholders

### Sample Data

The application includes sample data generators for testing:

```python
from utils.sample_data_generator import save_sample_datasets
save_sample_datasets()
```

This generates three sample datasets:
- **Financial Data**: Quarterly financial metrics by product and region
- **Sales Data**: Daily sales transactions with performance metrics
- **Operational Data**: Manufacturing and operational efficiency metrics

## Technical Architecture

### Core Components

1. **SimplifiedBIAgent (`utils/simplified_bi_agent.py`)**
   - Main AI agent powered by Gemini AI
   - Handles document extraction and comprehensive analysis
   - Provides financial insights and business recommendations

2. **Data Processing (`utils/data_cleaner.py`)**
   - File validation and compatibility checking
   - Automatic data cleaning and preprocessing
   - Column type detection and conversion

3. **Visualization Engine (`utils/chart_generator.py`)**
   - AI-recommended chart generation
   - Interactive Plotly visualizations
   - Statistical analysis charts
   - Correlation heatmaps

4. **KPI Dashboard (`utils/kpi_cards.py`)**
   - Dynamic KPI calculation
   - Interactive filtering
   - Trend analysis
   - Financial ratio calculations

5. **Gemini Integration (`utils/gemini_summary.py`)**
   - Advanced AI analysis and insights
   - Natural language processing
   - Financial analysis capabilities

### AI Capabilities

- **Gemini 1.5 Flash**: Fast response for real-time analysis
- **Natural Language Processing**: Understand business questions
- **Pattern Recognition**: Identify trends and anomalies
- **Financial Analysis**: Calculate key business metrics
- **Report Generation**: Create executive-ready summaries

## Configuration

### API Configuration
The Gemini API key is pre-configured in the application:
```python
GEMINI_API_KEY = "AIzaSyDzTSzogzG7ntlLHBOoHISaKC12g4ljW-s"
```

### Customization Options

1. **Analysis Templates**: Modify `app.py` to add custom analysis templates
2. **Chart Types**: Extend `chart_generator.py` for additional visualization types
3. **KPI Metrics**: Customize `kpi_cards.py` for specific business metrics
4. **AI Agents**: Modify `crew_ai_integration.py` to add specialized agents

## Supported Business Use Cases

### Financial Analysis
- Income statement analysis
- Balance sheet review
- Cash flow analysis
- Financial ratio calculation
- Profitability assessment
- Cost structure optimization

### Sales & Marketing
- Sales performance tracking
- Product performance analysis
- Customer segmentation
- Market share analysis
- Lead source effectiveness
- Revenue trend analysis

### Operations
- Operational efficiency metrics
- Production performance
- Quality control analysis
- Resource utilization
- Cost per unit analysis
- Productivity trends

### Strategic Planning
- Year-over-year comparisons
- Growth rate calculations
- Market opportunity analysis
- Competitive positioning
- Risk assessment
- Performance benchmarking

## Troubleshooting

### Common Issues

1. **File Upload Errors**
   - Check file size (max 50MB)
   - Ensure supported format (CSV, Excel, PDF, TXT)
   - Verify file is not corrupted

2. **Analysis Errors**
   - Ensure data has numerical columns for KPIs
   - Check for sufficient data rows (minimum 2-3 rows)
   - Verify column names don't contain special characters

3. **Visualization Issues**
   - Confirm data types are properly detected
   - Check for missing values in key columns
   - Ensure adequate data for meaningful visualizations

### Performance Tips

- For large datasets (>10K rows), consider sampling for faster processing
- Use date filters to focus on specific time periods
- Clear browser cache if experiencing loading issues
- Restart the application if memory usage becomes high

## Advanced Features

### CrewAI Multi-Agent Analysis
When enabled, the system uses specialized AI agents:
- **Data Analyst**: Statistical analysis and pattern recognition
- **Financial Analyst**: Financial metrics and ratio calculation
- **BI Specialist**: Strategic insights and recommendations
- **Report Writer**: Executive summary generation

### Custom Analysis Workflows
The application supports custom analysis workflows:
1. Upload data
2. Define specific objectives
3. Run targeted analysis
4. Generate custom reports
5. Export results

### API Integration
The system can be extended to integrate with:
- Database connections
- Cloud storage services
- Business intelligence platforms
- Reporting tools

## Support and Maintenance

### Regular Updates
- Check for new Streamlit versions
- Update dependencies regularly
- Monitor API usage and limits
- Backup analysis results

### Performance Monitoring
- Monitor memory usage for large datasets
- Track API response times
- Review error logs for issues
- Optimize queries for better performance

## Future Enhancements

Planned features for future releases:
- Real-time data streaming
- Advanced machine learning models
- Custom dashboard builder
- Multi-user collaboration
- API endpoint creation
- Advanced export formats
- Database integration
- Automated report scheduling

---

**Built with**: Streamlit, Pandas, Plotly, Gemini AI, CrewAI, and Python