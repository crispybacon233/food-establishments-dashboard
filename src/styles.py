# src/utils.py

import streamlit as st


def apply_base_style():
    """Applies a consistent, dashboard-like visual style across pages."""

    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 1rem;
                max-width: 1300px;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.8rem;
            }
            .dashboard-subtitle {
                color: #6b7280;
                margin-top: -0.35rem;
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .panel {
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 0.75rem 0.9rem;
                background: #ffffff;
            }
            [data-testid="stDataFrame"] {
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }
            [data-testid="stDataFrame"] [role="columnheader"] {
                background: #f8fafc;
                font-weight: 600;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )