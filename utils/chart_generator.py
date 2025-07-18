import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np
from utils.gemini_summary import get_chart_summary, get_chart_recommendations
import json

def generate_smart_charts(df, types, api_key=None):
    """Generate intelligent charts based on data types and AI recommendations"""
    
    cat_cols = [col for col, typ in types.items() if typ == "categorical"]
    num_cols = [col for col, typ in types.items() if typ == "numerical"]
    date_cols = [col for col, typ in types.items() if typ == "datetime"]
    
    if not num_cols:
        st.warning("⚠️ No numerical columns found for visualization.")
        return
    
    # Get AI-powered chart recommendations
    if api_key:
        try:
            st.subheader("🤖 AI-Recommended Charts")
            recommendations = get_chart_recommendations(df, api_key)
            
            # Clean and parse JSON response
            recommendations_clean = recommendations.strip()
            if recommendations_clean.startswith("```json"):
                recommendations_clean = recommendations_clean.replace("```json", "").strip()
            if recommendations_clean.endswith("```"):
                recommendations_clean = recommendations_clean[:recommendations_clean.rfind("```")].strip()
            
            try:
                chart_recs = json.loads(recommendations_clean)
                
                # Generate recommended charts
                for i, rec in enumerate(chart_recs[:4]):  # Limit to 4 charts
                    try:
                        fig = create_chart_from_recommendation(df, rec)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown(f"**💡 Why this chart:** {rec.get('reason', 'N/A')}")
                    except Exception as e:
                        st.error(f"Error creating recommended chart {i+1}: {str(e)}")
                        
            except json.JSONDecodeError:
                st.warning("⚠️ Could not parse AI chart recommendations. Showing default charts.")
                generate_default_charts(df, cat_cols, num_cols, date_cols, api_key)
                
        except Exception as e:
            st.warning(f"⚠️ AI recommendations unavailable: {str(e)}. Showing default charts.")
            generate_default_charts(df, cat_cols, num_cols, date_cols, api_key)
    else:
        generate_default_charts(df, cat_cols, num_cols, date_cols, api_key)
    
    # Additional analysis charts
    st.subheader("📊 Statistical Analysis")
    generate_statistical_charts(df, num_cols)
    
    # Correlation analysis
    if len(num_cols) > 1:
        st.subheader("🔗 Correlation Analysis")
        generate_correlation_heatmap(df, num_cols)

def create_chart_from_recommendation(df, recommendation):
    """Create a chart based on AI recommendation"""
    chart_type = recommendation.get('chart_type', '').lower()
    x_col = recommendation.get('x')
    y_col = recommendation.get('y')
    
    if not x_col or x_col not in df.columns:
        return None
    
    try:
        if chart_type in ['bar', 'column']:
            if y_col and y_col in df.columns:
                # Aggregate data if needed
                if df[x_col].dtype == 'object':
                    df_agg = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(15).reset_index()
                    fig = px.bar(df_agg, x=x_col, y=y_col, 
                               title=f"{recommendation.get('chart_type', 'Bar')} Chart: {y_col} by {x_col}")
                else:
                    fig = px.bar(df.head(20), x=x_col, y=y_col,
                               title=f"{recommendation.get('chart_type', 'Bar')} Chart: {y_col} by {x_col}")
            else:
                fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
                
        elif chart_type in ['pie', 'donut']:
            if y_col and y_col in df.columns:
                df_agg = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(10).reset_index()
                hole = 0.4 if chart_type == 'donut' else 0
                fig = px.pie(df_agg, names=x_col, values=y_col, hole=hole,
                           title=f"{recommendation.get('chart_type', 'Pie')} Chart: {y_col} by {x_col}")
            else:
                value_counts = df[x_col].value_counts().head(10)
                fig = px.pie(values=value_counts.values, names=value_counts.index,
                           title=f"Distribution of {x_col}")
                
        elif chart_type == 'line':
            if y_col and y_col in df.columns:
                # Sort by x_col if it's numeric or date
                if pd.api.types.is_numeric_dtype(df[x_col]) or pd.api.types.is_datetime64_any_dtype(df[x_col]):
                    df_sorted = df.sort_values(x_col)
                    fig = px.line(df_sorted, x=x_col, y=y_col,
                                title=f"Line Chart: {y_col} over {x_col}")
                else:
                    df_agg = df.groupby(x_col)[y_col].sum().reset_index()
                    fig = px.line(df_agg, x=x_col, y=y_col,
                                title=f"Line Chart: {y_col} by {x_col}")
            else:
                return None
                
        elif chart_type == 'scatter':
            if y_col and y_col in df.columns:
                fig = px.scatter(df, x=x_col, y=y_col,
                               title=f"Scatter Plot: {y_col} vs {x_col}")
            else:
                return None
                
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_col, title=f"Histogram of {x_col}")
            
        else:
            # Default to bar chart
            if y_col and y_col in df.columns:
                fig = px.bar(df.head(20), x=x_col, y=y_col,
                           title=f"Chart: {y_col} by {x_col}")
            else:
                fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
        
        fig.update_layout(height=500, showlegend=True)
        return fig
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def generate_default_charts(df, cat_cols, num_cols, date_cols, api_key):
    """Generate default chart set when AI recommendations are not available"""
    
    top_n = st.slider("Select Top N items for Charts", 5, 30, 10, key="chart_slider")
    
    # Time series charts if date columns exist
    if date_cols and num_cols:
        st.subheader("📈 Time Series Analysis")
        for date_col in date_cols[:1]:  # Only first date column
            for num_col in num_cols[:2]:  # First 2 numeric columns
                try:
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col])
                    df_time = df_time.sort_values(date_col)
                    
                    fig = px.line(df_time, x=date_col, y=num_col,
                                title=f"{num_col} Trend Over Time")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if api_key:
                        try:
                            prompt = f"Analyze the time series trend of {num_col} over {date_col} in this business data."
                            summary = get_chart_summary(prompt, api_key)
                            st.info(f"🧠 AI Insight: {summary}")
                        except:
                            pass
                except Exception as e:
                    st.error(f"Error creating time series chart: {str(e)}")
    
    # Category vs Numeric charts
    if cat_cols and num_cols:
        st.subheader("📊 Category Analysis")
        for cat in cat_cols[:2]:  # Limit to avoid overload
            for num in num_cols[:2]:
                try:
                    # Aggregate and get top N
                    df_plot = df.groupby(cat)[num].sum().sort_values(ascending=False).head(top_n).reset_index()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_bar = px.bar(df_plot, x=cat, y=num, 
                                       title=f"Top {top_n} {cat} by {num}")
                        fig_bar.update_xaxes(tickangle=45)
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    with col2:
                        fig_pie = px.pie(df_plot, names=cat, values=num, hole=0.4,
                                       title=f"{cat} Distribution ({num})")
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    if api_key:
                        try:
                            prompt = f"Analyze the relationship between {cat} and {num} in this business dataset. What insights can be drawn?"
                            summary = get_chart_summary(prompt, api_key)
                            st.info(f"🧠 AI Insight: {summary}")
                        except:
                            pass
                            
                except Exception as e:
                    st.error(f"Error creating category chart: {str(e)}")
    
    # Distribution charts for numeric columns
    if num_cols:
        st.subheader("📊 Distribution Analysis")
        for num_col in num_cols[:3]:  # First 3 numeric columns
            try:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = px.histogram(df, x=num_col, nbins=30,
                                          title=f"Distribution of {num_col}")
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    fig_box = px.box(df, y=num_col, title=f"Box Plot of {num_col}")
                    st.plotly_chart(fig_box, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error creating distribution chart for {num_col}: {str(e)}")

def generate_statistical_charts(df, num_cols):
    """Generate statistical analysis charts"""
    if len(num_cols) < 2:
        return
    
    try:
        # Summary statistics
        summary_stats = df[num_cols].describe()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Statistics comparison
            fig_stats = go.Figure()
            for stat in ['mean', 'std', 'min', 'max']:
                fig_stats.add_trace(go.Bar(
                    name=stat.title(),
                    x=num_cols,
                    y=summary_stats.loc[stat],
                ))
            
            fig_stats.update_layout(
                title="Statistical Summary Comparison",
                xaxis_title="Columns",
                yaxis_title="Values",
                barmode='group'
            )
            st.plotly_chart(fig_stats, use_container_width=True)
        
        with col2:
            # Box plots for comparison
            fig_box = go.Figure() 
            for col in num_cols:
                fig_box.add_trace(go.Box(y=df[col], name=col))
            
            fig_box.update_layout(
                title="Distribution Comparison (Box Plots)",
                yaxis_title="Values"
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error generating statistical charts: {str(e)}")

def generate_correlation_heatmap(df, num_cols):
    """Generate correlation heatmap for numerical columns"""
    try:
        correlation_matrix = df[num_cols].corr()
        
        fig = px.imshow( 
            correlation_matrix,
            title="Correlation Matrix",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # Strong correlation threshold
                    strong_correlations.append({
                        'Variable 1': correlation_matrix.columns[i],
                        'Variable 2': correlation_matrix.columns[j],
                        'Correlation': corr_value
                    })
        
        if strong_correlations:
            st.write("**Strong Correlations (|r| > 0.7):**")
            for corr in strong_correlations:
                st.write(f"- {corr['Variable 1']} ↔ {corr['Variable 2']}: {corr['Correlation']:.3f}")
                
    except Exception as e:
        st.error(f"Error generating correlation heatmap: {str(e)}")

def create_advanced_chart(df, chart_config):
    """Create advanced charts based on configuration"""
    try:
        chart_type = chart_config.get('type', 'bar')
        title = chart_config.get('title', 'Chart')
        
        if chart_type == 'multi_line':
            fig = go.Figure()
            for col in chart_config.get('y_columns', []):
                fig.add_trace(go.Scatter(
                    x=df[chart_config['x_column']],
                    y=df[col],
                    mode='lines',
                    name=col
                ))
            fig.update_layout(title=title)
            
        elif chart_type == 'stacked_bar':
            fig = px.bar(
                df, 
                x=chart_config['x_column'],
                y=chart_config['y_columns'],
                title=title
            )
            
        elif chart_type == 'area':
            fig = px.area(
                df,
                x=chart_config['x_column'],
                y=chart_config['y_column'],
                title=title
            )
            
        else:
            return None
            
        return fig
        
    except Exception as e:
        st.error(f"Error creating advanced chart: {str(e)}")
        return None
