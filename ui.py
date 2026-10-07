import streamlit as st


def apply_visual_style() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f3f6f3;
            color: #26383a;
        }
        h1, h2, h3 {
            color: #21484a;
            font-family: Georgia, "Charter", serif;
            letter-spacing: 0;
        }
        .stApp p, .stApp li {
            color: #34484a;
            font-family: "Trebuchet MS", sans-serif;
            letter-spacing: 0;
            line-height: 1.6;
        }
        section[data-testid="stSidebar"] {
            background: #e8efec;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border-left: 3px solid #bd7049;
            border-radius: 4px;
            padding: 0.75rem 1rem;
        }
        [data-testid="stAlert"] {
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
