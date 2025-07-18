import pandas as pd
import numpy as np

def clean_data(df):
    """Clean and preprocess the dataset"""
    df = df.copy()
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    for col in df.columns:
        if df[col].dtype == "object":
            # For categorical data, fill with mode
            if not df[col].mode().empty:
                df[col].fillna(df[col].mode().iloc[0], inplace=True)
            else:
                df[col].fillna("Unknown", inplace=True)
        else:
            # For numerical data, fill with mean
            df[col].fillna(df[col].mean(), inplace=True)
    
    # Convert potential date columns
    for col in df.columns:
        if df[col].dtype == "object":
            # Try to convert to datetime if it looks like dates
            if any(keyword in col.lower() for keyword in ['date', 'time', 'year', 'month']):
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
    
    return df

def detect_column_types(df):
    """Detect and categorize column types for analysis"""
    types = {}
    for col in df.columns:
        if "datetime" in str(df[col].dtype):
            types[col] = "datetime"
        elif df[col].dtype == "object":
            # Check if it's actually numeric but stored as string
            try:
                pd.to_numeric(df[col])
                types[col] = "numerical"
            except:
                types[col] = "categorical"
        else:
            types[col] = "numerical"
    return types

def validate_file(uploaded_file):
    """Validate uploaded file for compatibility and quality"""
    try:
        # Check file size (limit to 50MB)
        if uploaded_file.size > 50 * 1024 * 1024:
            return False, "File size too large. Please upload files smaller than 50MB."
        
        # Check file extension
        allowed_extensions = ['.csv', '.xlsx', '.xls', '.pdf', '.txt']
        file_extension = '.' + uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            return False, f"Unsupported file type. Supported types: {', '.join(allowed_extensions)}"
        
        # Basic content validation for CSV/Excel
        if file_extension in ['.csv', '.xlsx', '.xls']:
            try:
                # Try to read a small sample
                if file_extension == '.csv':
                    sample_df = pd.read_csv(uploaded_file, nrows=5)
                else:
                    sample_df = pd.read_excel(uploaded_file, nrows=5)
                
                if len(sample_df.columns) == 0:
                    return False, "File appears to be empty or has no columns."
                
                if len(sample_df) == 0:
                    return False, "File appears to have no data rows."
                
                # Reset file pointer
                uploaded_file.seek(0)
                
                return True, f"Valid {file_extension} file with {len(sample_df.columns)} columns detected."
                
            except Exception as e:
                return False, f"Error reading file: {str(e)}"
        
        # For PDF and TXT files
        elif file_extension in ['.pdf', '.txt']:
            return True, f"Valid {file_extension} file ready for content extraction."
        
        return True, "File validation passed."
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def get_data_quality_report(df):
    """Generate a comprehensive data quality report"""
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'column_types': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum(),
        'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_columns': len(df.select_dtypes(include=['object']).columns),
        'datetime_columns': len(df.select_dtypes(include=['datetime64']).columns)
    }
    
    # Check for potential issues
    issues = []
    
    # High missing value columns
    missing_pct = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_pct[missing_pct > 50].index.tolist()
    if high_missing:
        issues.append(f"Columns with >50% missing values: {high_missing}")
    
    # Duplicate rows
    if report['duplicate_rows'] > 0:
        issues.append(f"{report['duplicate_rows']} duplicate rows found")
    
    # Single value columns
    single_value_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if single_value_cols:
        issues.append(f"Columns with single/no values: {single_value_cols}")
    
    report['data_quality_issues'] = issues
    
    return report
