import streamlit as st
import requests
from datetime import date

BACKEND_URL = "https://legaleaseai-wabt.onrender.com"

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase AI")
st.write("AI-powered Legal Document Generator")

document_type = st.selectbox(
    "Select Document Type",
    [
        "Agreement",
        "Contract",
        "NDA",
        "Lease Agreement",
        "Employment Offer Letter"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Alice and Bob"
)

terms = st.text_area(
    "Terms / Conditions",
    placeholder="Enter the terms and conditions..."
)

effective_date = st.date_input(
    "Effective Date",
    value=date.today()
)

if st.button("🚀 Generate Document"):

    if not parties or not terms:
        st.warning("Please enter Parties and Terms.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": str(effective_date)
        }

        try:
            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()

                generated_text = (
                    data.get("generated_text")
                    or data.get("text")
                    or data.get("document")
                    or data.get("content")
                )

                if generated_text:
                    st.session_state["document"] = generated_text
                else:
                    st.error("Backend response-la document text kidaikkala.")
            else:
                st.error(f"Backend Error: {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error(f"Connection Error: {e}")


if "document" in st.session_state:

    st.subheader("📄 Generated Document")

    edited_document = st.text_area(
        "Edit Document",
        value=st.session_state["document"],
        height=500
    )

    st.session_state["document"] = edited_document

    st.download_button(
        "⬇️ Download TXT",
        data=edited_document,
        file_name="legal_document.txt",
        mime="text/plain"
    )
