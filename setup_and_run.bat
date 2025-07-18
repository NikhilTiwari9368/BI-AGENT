@echo off
echo Setting up Business Intelligence Agent...
echo.

REM Install minimal requirements (without CrewAI to avoid onnxruntime issues)
echo Installing required packages...
pip install -r requirements_minimal.txt

echo.
echo Generating sample datasets for testing...
python -c "from utils.sample_data_generator import save_sample_datasets; save_sample_datasets()"

echo.
echo Setup complete! Starting the BI Agent...
echo The application will open at http://localhost:8501
echo.

REM Start the Streamlit application
streamlit run app.py
