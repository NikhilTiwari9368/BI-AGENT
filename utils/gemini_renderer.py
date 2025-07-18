import json
import streamlit as st
from utils.chart_generator import generate_chart

def render_charts_from_gemini(df_clean, chart_json_string):
    try:
        suggestions = json.loads(chart_json_string)

        for chart_info in suggestions:
            chart_type = chart_info.get("chart_type")
            x = chart_info.get("x")
            y = chart_info.get("y")
            reason = chart_info.get("reason", "")

            st.subheader(f"📊 {chart_type} Chart — {x} vs {y if y else 'N/A'}")
            st.caption(f"💡 Gemini Reason: {reason}")

            chart = generate_chart(df_clean, x, y, chart_type)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.warning(f"⚠️ Could not generate {chart_type} chart with x='{x}' and y='{y}'")

    except Exception as e:
        st.error("❌ Failed to parse Gemini chart suggestion JSON.")
        st.code(chart_json_string)
        st.exception(e)
