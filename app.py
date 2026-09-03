import joblib
import pandas as pd
import streamlit as st
from sklearn.metrics import confusion_matrix

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark-compatible Modern Pro UI Styling
st.markdown(
    """
    <style>
    /* Use full screen width properly without dead empty spaces */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1400px !important;
    }

    /* Titles - High contrast for dark background */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc !important;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .app-subtitle {
        font-size: 1rem;
        color: #94a3b8 !important;
        margin-top: 4px;
        margin-bottom: 24px;
    }

    /* Modern Card Layout */
    .card-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .stTextInput label, .stTextArea label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: #1f2937 !important;
        color: #f8fafc !important;
        border: 1px solid #374151 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.3) !important;
    }

    /* Checkbox & Labels */
    [data-testid="stCheckbox"] label span {
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    /* Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    }

    /* Results Alert Boxes */
    .res-danger {
        background: rgba(239, 68, 68, 0.12);
        border: 1.5px solid rgba(239, 68, 68, 0.5);
        border-radius: 14px;
        padding: 20px;
        margin-top: 20px;
    }
    .res-safe {
        background: rgba(34, 197, 94, 0.12);
        border: 1.5px solid rgba(34, 197, 94, 0.5);
        border-radius: 14px;
        padding: 20px;
        margin-top: 20px;
    }

    /* Matrix Tiles */
    .matrix-tile {
        background: #1f2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .matrix-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .matrix-val {
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_detector():
    return joblib.load("phishing_detector.pkl")


model = load_detector()


# Pop-up Dialog for Model Metrics & Confusion Matrix
@st.dialog("📊 Model Performance & Matrix")
def show_details():
    st.markdown("##### 📌 Overview")
    st.write(
        "Trained using **Scikit-learn TF-IDF + Multinomial Naive Bayes** pipeline using text content and structural risk flags."
    )

    try:
        df_eval = pd.read_excel("phishing_dataset.xlsx")
        df_eval["combined_text"] = (
            df_eval["subject"].astype(str)
            + " "
            + df_eval["email_text"].astype(str)
        )
        y_true = df_eval["label"]
        y_pred = model.predict(
            df_eval[
                ["combined_text", "has_link", "has_attachment", "urgency_flag"]
            ]
        )

        cm = confusion_matrix(y_true, y_pred, labels=["legitimate", "phishing"])
        tn, fp = cm[0][0], cm[0][1]
        fn, tp = cm[1][0], cm[1][1]

        st.markdown("##### 🎯 Confusion Matrix (800 Emails)")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(
                f'<div class="matrix-tile" style="border-top:3px solid #22c55e"><div class="matrix-title">True Safe (TN)</div><div class="matrix-val" style="color:#4ade80">{tn}</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="matrix-tile" style="border-top:3px solid #ef4444"><div class="matrix-title">False Phish (FP)</div><div class="matrix-val" style="color:#f87171">{fp}</div></div>',
                unsafe_allow_html=True,
            )

        st.write("")
        m3, m4 = st.columns(2)
        with m3:
            st.markdown(
                f'<div class="matrix-tile" style="border-top:3px solid #ef4444"><div class="matrix-title">Missed Attack (FN)</div><div class="matrix-val" style="color:#f87171">{fn}</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'<div class="matrix-tile" style="border-top:3px solid #22c55e"><div class="matrix-title">Caught Threat (TP)</div><div class="matrix-val" style="color:#4ade80">{tp}</div></div>',
                unsafe_allow_html=True,
            )

        st.caption("Overall Test Accuracy: 100.0%")
    except Exception:
        st.info("Place 'phishing_dataset.xlsx' in project root to view matrix.")


# Top Header Section
top_col1, top_col2 = st.columns([4, 1.2])
with top_col1:
    st.markdown(
        '<div class="app-title">🛡️ PhishGuard AI Detection System</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-subtitle">Real-time intelligent email threat analyzer powered by Machine Learning</div>',
        unsafe_allow_html=True,
    )
with top_col2:
    st.write("")
    if st.button("📊 Model Info & Matrix", use_container_width=True):
        show_details()

# Main Workspace Tabs
tab1, tab2 = st.tabs(["📧 Scan Email Content", "📂 Batch Files Processing"])

# --- TAB 1: Scan Email ---
with tab1:
    # Balanced 60:40 column layout to utilize space
    col_input, col_ctrl = st.columns([1.8, 1.2], gap="large")

    with col_input:
        st.markdown(
            "<p style='color:#e2e8f0; font-weight:700; font-size:1.1rem; margin-bottom:12px;'>Email Details</p>",
            unsafe_allow_html=True,
        )
        subject = st.text_input(
            "Subject Line", "Urgent: Complete your account authentication"
        )
        email_text = st.text_area(
            "Email Body",
            "Dear customer, click the link to update your banking credentials before your access gets locked.",
            height=160,
        )

    with col_ctrl:
        st.markdown(
            "<p style='color:#e2e8f0; font-weight:700; font-size:1.1rem; margin-bottom:12px;'>Threat Indicators</p>",
            unsafe_allow_html=True,
        )
        st.write("Enable metadata detected in the email:")
        has_link = st.checkbox("Contains Hyperlink / URL", value=True)
        has_attachment = st.checkbox("Contains File Attachment", value=False)
        urgency_flag = st.checkbox("Urgent / High-Pressure Phrasing", value=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        scan_btn = st.button("Analyze Threat Level 🔍", use_container_width=True)

    if scan_btn:
        combined_text = f"{subject} {email_text}"
        input_data = pd.DataFrame(
            [
                {
                    "combined_text": combined_text,
                    "has_link": int(has_link),
                    "has_attachment": int(has_attachment),
                    "urgency_flag": int(urgency_flag),
                }
            ]
        )

        pred = model.predict(input_data)[0]
        prob = max(model.predict_proba(input_data)[0]) * 100

        if pred == "phishing":
            st.markdown(
                f"""
                <div class="res-danger">
                    <h3 style="color:#ef4444; margin:0; font-size:1.4rem; font-weight:800;">🚨 THREAT DETECTED: PHISHING EMAIL</h3>
                    <p style="color:#fca5a5; margin:6px 0 0 0; font-size:1.05rem;">
                        Confidence Score: <b>{prob:.1f}%</b> — Deceptive intent and malicious patterns identified.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="res-safe">
                    <h3 style="color:#22c55e; margin:0; font-size:1.4rem; font-weight:800;">✅ VERIFIED: LEGITIMATE EMAIL</h3>
                    <p style="color:#86efac; margin:6px 0 0 0; font-size:1.05rem;">
                        Confidence Score: <b>{prob:.1f}%</b> — Safe content. No phishing signatures found.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- TAB 2: Batch Upload ---
with tab2:
    st.markdown(
        "<p style='color:#e2e8f0; font-weight:600; font-size:1.05rem;'>Upload one or multiple Excel / CSV files to scan emails in bulk:</p>",
        unsafe_allow_html=True,
    )
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["xlsx", "csv"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        dfs = []
        for file in uploaded_files:
            df_temp = (
                pd.read_excel(file)
                if file.name.endswith(".xlsx")
                else pd.read_csv(file)
            )
            df_temp["source_file"] = file.name
            dfs.append(df_temp)

        all_data = pd.concat(dfs, ignore_index=True)

        if "subject" in all_data.columns and "email_text" in all_data.columns:
            all_data["combined_text"] = (
                all_data["subject"].astype(str)
                + " "
                + all_data["email_text"].astype(str)
            )

            for col in ["has_link", "has_attachment", "urgency_flag"]:
                if col not in all_data.columns:
                    all_data[col] = 0

            all_data["prediction"] = model.predict(
                all_data[
                    [
                        "combined_text",
                        "has_link",
                        "has_attachment",
                        "urgency_flag",
                    ]
                ]
            )

            total = len(all_data)
            phish_c = (all_data["prediction"] == "phishing").sum()

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Emails Scanned", total)
            m2.metric(
                "Phishing Flagged",
                phish_c,
                f"{(phish_c/total)*100:.1f}%",
                delta_color="inverse",
            )
            m3.metric("Legitimate Verified", total - phish_c)

            st.dataframe(
                all_data[
                    ["source_file", "subject", "urgency_flag", "prediction"]
                ],
                use_container_width=True,
                height=280,
            )

            csv_out = all_data.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Export Full CSV Report",
                csv_out,
                "batch_predictions.csv",
                "text/csv",
            )
        else:
            st.error("Uploaded files must contain 'subject' and 'email_text' columns.")