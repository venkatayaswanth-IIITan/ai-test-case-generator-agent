
import streamlit as st
import pandas as pd

from test_case_generator import generate_test_cases
from database import (
    create_tables,
    save_results,
    get_history,
    get_saved_results
)
from export_utils import export_to_csv


st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)

create_tables()

st.title("🧪 AI Test Case Generator Agent")

st.write(
    "Convert software requirements into "
    "positive, negative and edge-case test scenarios using AI."
)

st.divider()

# Session state
if "cases" not in st.session_state:
    st.session_state.cases = []

if "requirement" not in st.session_state:
    st.session_state.requirement = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "assumptions" not in st.session_state:
    st.session_state.assumptions = []


# Requirement input
st.subheader("Enter Software Requirement")

requirement = st.text_area(
    "Describe your software feature:",
    placeholder=(
        "Example: A user should be able to "
        "login using email and password."
    ),
    height=130
)


# Generate button
if st.button("🚀 Generate Test Cases", type="primary"):

    if not requirement.strip():

        st.warning("Please enter a software requirement.")

    else:

        try:

            with st.spinner("AI Agent is analyzing your requirement..."):

                data = generate_test_cases(requirement)

                st.session_state.cases = data["test_cases"]
                st.session_state.requirement = requirement
                st.session_state.summary = data.get(
                    "feature_summary", ""
                )
                st.session_state.assumptions = data.get(
                    "assumptions", []
                )

            st.success("Test cases generated successfully!")

        except Exception as e:

            st.error(f"Generation failed: {e}")


# Generated results
if st.session_state.cases:

    st.divider()

    st.subheader("Requirement Analysis")

    st.write(st.session_state.summary)

    if st.session_state.assumptions:

        st.warning(
            "Assumptions: " +
            ", ".join(st.session_state.assumptions)
        )

    st.subheader("Generated Test Cases")

    df = pd.DataFrame(st.session_state.cases)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="test_case_editor"
    )

    # Convert edited table back to dictionaries
    st.session_state.cases = edited_df.to_dict(
        orient="records"
    )

    st.caption(
        "Edit cells directly. Delete rows using the table controls."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("💾 Save Results"):

            try:

                if not st.session_state.cases:
                    st.warning("No test cases to save.")

                else:

                    save_results(
                        st.session_state.requirement,
                        {
                            "feature_summary": st.session_state.summary,
                            "assumptions": st.session_state.assumptions,
                            "test_cases": st.session_state.cases
                        }
                    )

                    st.success("Results saved successfully!")

            except Exception as e:

                st.error(f"Save failed: {e}")

    with col2:

        if st.button("🗑️ Clear Results"):

            st.session_state.cases = []
            st.session_state.requirement = ""
            st.session_state.summary = ""
            st.session_state.assumptions = []

            st.rerun()

    with col3:

        csv_data = export_to_csv(
            st.session_state.cases
        )

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="test_cases.csv",
            mime="text/csv"
        )


# History section
st.divider()

st.subheader("📚 Previous Test Case History")

history = get_history()

if history:

    for item in history:

        history_id, old_requirement, summary = item

        with st.expander(
            f"Requirement #{history_id}: {old_requirement}"
        ):

            st.write("Feature Summary:", summary)

            saved_cases = get_saved_results(history_id)

            if saved_cases:

                history_df = pd.DataFrame(saved_cases)

                st.dataframe(
                    history_df,
                    use_container_width=True,
                    hide_index=True
                )

else:

    st.info("No saved history available yet.")

st.divider()

st.caption(
    "AI Test Case Generator Agent | Built using "
    "Python, Streamlit, Ollama, LangChain and SQLite"
)
