import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def display_kpis(df, types):
    """Display comprehensive KPI dashboard with filters and advanced metrics"""
    
    st.markdown("### 📊 Key Performance Indicators")
    
    # Detect column types
    category_cols = [col for col, typ in types.items() if typ == "categorical"]
    date_cols = [col for col, typ in types.items() if typ == "datetime"]
    numeric_cols = [col for col, typ in types.items() if typ == "numerical"]
    
    if not numeric_cols:
        st.info("⚠️ No numerical columns found for KPI generation.")
        return
    
    df_filtered = df.copy()
    
    # Filters Section
    with st.expander("🔍 Apply Filters", expanded=False):
        col1, col2 = st.columns(2)
        
        # Category Filter
        with col1:
            if category_cols:
                selected_cat_col = st.selectbox("🌍 Filter by Category", ["None"] + category_cols)
                if selected_cat_col != "None":
                    unique_categories = df[selected_cat_col].dropna().unique().tolist()
                    selected_cat_val = st.selectbox(f"Select {selected_cat_col}", ["All"] + unique_categories)
                    
                    if selected_cat_val != "All":
                        df_filtered = df_filtered[df_filtered[selected_cat_col] == selected_cat_val]
        
        # Date Filter
        with col2:
            if date_cols:
                selected_date_col = st.selectbox("📅 Filter by Date", ["None"] + date_cols)
                if selected_date_col != "None":
                    df_filtered[selected_date_col] = pd.to_datetime(df_filtered[selected_date_col], errors="coerce")
                    
                    # Date range selection
                    min_date = df_filtered[selected_date_col].min()
                    max_date = df_filtered[selected_date_col].max()
                    
                    if pd.notna(min_date) and pd.notna(max_date):
                        date_range = st.date_input(
                            f"Select Date Range for {selected_date_col}",
                            value=(min_date.date(), max_date.date()),
                            min_value=min_date.date(),
                            max_value=max_date.date()
                        )
                        
                        if len(date_range) == 2:
                            start_date, end_date = date_range
                            df_filtered = df_filtered[
                                (df_filtered[selected_date_col].dt.date >= start_date) &
                                (df_filtered[selected_date_col].dt.date <= end_date)
                            ]
    
    # Display filter summary
    if len(df_filtered) != len(df):
        st.info(f"📊 Showing {len(df_filtered):,} rows out of {len(df):,} total rows after filtering")
    
    # Main KPI Dashboard
    st.markdown("### 📈 Executive KPI Dashboard")
    
    # Calculate key business metrics
    kpi_data = calculate_business_kpis(df_filtered, numeric_cols, date_cols)
    
    # Display KPIs in cards
    display_kpi_cards(kpi_data)
    
    # Performance trends (if date data available)
    if date_cols and len(df_filtered) > 1:
        st.markdown("### 📈 Performance Trends")
        display_trend_analysis(df_filtered, numeric_cols, date_cols[0])
    
    # Detailed metrics table
    st.markdown("### 📋 Detailed Metrics")
    display_detailed_metrics(df_filtered, numeric_cols)

def calculate_business_kpis(df, numeric_cols, date_cols):
    """Calculate comprehensive business KPIs"""
    
    kpis = {}
    
    for col in numeric_cols:
        data = df[col].dropna()
        
        if len(data) == 0:
            continue
            
        # Basic statistics
        kpis[col] = {
            'total': data.sum(),
            'average': data.mean(),
            'median': data.median(),
            'max': data.max(),
            'min': data.min(),
            'std': data.std(),
            'count': len(data),
            'variance': data.var(),
            'skewness': data.skew() if len(data) > 2 else 0,
            'kurtosis': data.kurtosis() if len(data) > 3 else 0
        }
        
        # Growth calculations (if date column available)
        if date_cols and len(df) > 1:
            try:
                df_sorted = df.sort_values(date_cols[0])
                first_value = df_sorted[col].iloc[0]
                last_value = df_sorted[col].iloc[-1]
                
                if first_value != 0:
                    growth_rate = ((last_value - first_value) / abs(first_value)) * 100
                    kpis[col]['growth_rate'] = growth_rate
                else:
                    kpis[col]['growth_rate'] = 0
                    
                # Period-over-period analysis
                if len(df_sorted) >= 2:
                    period_changes = df_sorted[col].pct_change().dropna()
                    kpis[col]['avg_period_change'] = period_changes.mean() * 100
                    kpis[col]['volatility'] = period_changes.std() * 100
                    
            except Exception:
                kpis[col]['growth_rate'] = 0
                kpis[col]['avg_period_change'] = 0
                kpis[col]['volatility'] = 0
        
        # Financial ratios (if applicable column names)
        if 'revenue' in col.lower() or 'sales' in col.lower():
            kpis[col]['type'] = 'revenue'
        elif 'profit' in col.lower() or 'earnings' in col.lower():
            kpis[col]['type'] = 'profit'
        elif 'cost' in col.lower() or 'expense' in col.lower():
            kpis[col]['type'] = 'expense'
        else:
            kpis[col]['type'] = 'general'
    
    return kpis

def display_kpi_cards(kpi_data):
    """Display KPI cards in a responsive grid"""
    
    # Determine most important metrics to highlight
    priority_metrics = []
    for col, data in kpi_data.items():
        if data['type'] in ['revenue', 'profit']:
            priority_metrics.append(col)
    
    # If no priority metrics, use first few numeric columns
    if not priority_metrics:
        priority_metrics = list(kpi_data.keys())[:4]
    
    # Display priority KPIs in main cards
    cols = st.columns(min(4, len(priority_metrics)))
    
    for idx, col in enumerate(priority_metrics[:4]):
        data = kpi_data[col]
        
        with cols[idx]:
            # Determine delta for growth indication
            delta = None
            delta_color = "normal"
            
            if 'growth_rate' in data and data['growth_rate'] != 0:
                delta = f"{data['growth_rate']:.1f}%"
                delta_color = "normal" if data['growth_rate'] >= 0 else "inverse"
            
            # Format the main value based on magnitude
            main_value = data['total']
            if abs(main_value) >= 1e9:
                formatted_value = f"${main_value/1e9:.2f}B"
            elif abs(main_value) >= 1e6:
                formatted_value = f"${main_value/1e6:.2f}M"
            elif abs(main_value) >= 1e3:
                formatted_value = f"${main_value/1e3:.2f}K"
            else:
                formatted_value = f"${main_value:,.2f}"
            
            # Display metric card
            st.metric(
                label=f"📊 {col.replace('_', ' ').title()}",
                value=formatted_value,
                delta=delta
            )
            
            # Additional info in smaller text
            st.caption(f"Avg: ${data['average']:,.2f} | Count: {data['count']:,}")
    
    # Additional metrics in expandable section
    with st.expander("📈 Additional Metrics", expanded=False):
        for col, data in kpi_data.items():
            if col not in priority_metrics[:4]:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total", f"${data['total']:,.2f}")
                with col2:
                    st.metric("Average", f"${data['average']:,.2f}")
                with col3:
                    st.metric("Max", f"${data['max']:,.2f}")
                with col4:
                    st.metric("Min", f"${data['min']:,.2f}")
                
                st.markdown("---")

def display_trend_analysis(df, numeric_cols, date_col):
    """Display trend analysis for time-series data"""
    
    try:
        df_time = df.copy()
        df_time[date_col] = pd.to_datetime(df_time[date_col])
        df_time = df_time.sort_values(date_col)
        
        # Select top metrics for trend analysis
        selected_metrics = st.multiselect(
            "Select metrics for trend analysis:",
            numeric_cols,
            default=numeric_cols[:2]  # Default to first 2 metrics
        )
        
        if selected_metrics:
            import plotly.express as px
            import plotly.graph_objects as go
            
            # Create trend chart
            fig = go.Figure()
            
            for metric in selected_metrics:
                fig.add_trace(go.Scatter(
                    x=df_time[date_col],
                    y=df_time[metric],
                    mode='lines+markers',
                    name=metric,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title="Performance Trends Over Time",
                xaxis_title="Date",
                yaxis_title="Value",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend summary
            st.markdown("**Trend Summary:**")
            for metric in selected_metrics:
                if len(df_time) >= 2:
                    first_val = df_time[metric].iloc[0]
                    last_val = df_time[metric].iloc[-1]
                    
                    if first_val != 0:
                        change_pct = ((last_val - first_val) / abs(first_val)) * 100
                        trend_icon = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
                        st.write(f"{trend_icon} {metric}: {change_pct:+.1f}% change")
                    
    except Exception as e:
        st.error(f"Error in trend analysis: {str(e)}")

def display_detailed_metrics(df, numeric_cols):
    """Display detailed statistical metrics in a table"""
    
    metrics_data = []
    
    for col in numeric_cols:
        data = df[col].dropna()
        
        if len(data) > 0:
            metrics_data.append({
                'Metric': col,
                'Count': len(data),
                'Sum': data.sum(),
                'Mean': data.mean(),
                'Median': data.median(),
                'Std Dev': data.std(),
                'Min': data.min(),
                'Max': data.max(),
                'Range': data.max() - data.min(),
                'CV (%)': (data.std() / data.mean() * 100) if data.mean() != 0 else 0
            })
    
    if metrics_data:
        metrics_df = pd.DataFrame(metrics_data)
        
        # Format numeric columns
        numeric_format_cols = ['Sum', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Range']
        for col in numeric_format_cols:
            metrics_df[col] = metrics_df[col].apply(lambda x: f"{x:,.2f}")
        
        metrics_df['CV (%)'] = metrics_df['CV (%)'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        # Download option
        csv = metrics_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Metrics Summary",
            data=csv,
            file_name="kpi_summary.csv",
            mime="text/csv"
        )

def calculate_financial_ratios(df):
    """Calculate common financial ratios if applicable columns exist"""
    
    ratios = {}
    
    # Common financial column patterns
    revenue_cols = [col for col in df.columns if any(term in col.lower() for term in ['revenue', 'sales', 'income'])]
    profit_cols = [col for col in df.columns if any(term in col.lower() for term in ['profit', 'earnings', 'net_income'])]
    asset_cols = [col for col in df.columns if any(term in col.lower() for term in ['asset', 'total_assets'])]
    equity_cols = [col for col in df.columns if any(term in col.lower() for term in ['equity', 'shareholders_equity'])]
    
    try:
        # Profit margins
        if revenue_cols and profit_cols:
            for rev_col in revenue_cols:
                for prof_col in profit_cols:
                    if pd.api.types.is_numeric_dtype(df[rev_col]) and pd.api.types.is_numeric_dtype(df[prof_col]):
                        profit_margin = (df[prof_col].sum() / df[rev_col].sum()) * 100
                        ratios[f'Profit Margin ({prof_col}/{rev_col})'] = f"{profit_margin:.2f}%"
        
        # Return on Assets (ROA)
        if profit_cols and asset_cols:
            for prof_col in profit_cols:
                for asset_col in asset_cols:
                    if pd.api.types.is_numeric_dtype(df[prof_col]) and pd.api.types.is_numeric_dtype(df[asset_col]):
                        roa = (df[prof_col].sum() / df[asset_col].sum()) * 100
                        ratios[f'ROA ({prof_col}/{asset_col})'] = f"{roa:.2f}%"
        
        # Return on Equity (ROE)
        if profit_cols and equity_cols:
            for prof_col in profit_cols:
                for eq_col in equity_cols:
                    if pd.api.types.is_numeric_dtype(df[prof_col]) and pd.api.types.is_numeric_dtype(df[eq_col]):
                        roe = (df[prof_col].sum() / df[eq_col].sum()) * 100
                        ratios[f'ROE ({prof_col}/{eq_col})'] = f"{roe:.2f}%"
        
    except Exception as e:
        ratios['Error'] = f"Could not calculate ratios: {str(e)}"
    
    return ratios
