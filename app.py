import streamlit as st
import utils
import prompts

st.set_page_config(page_title="Insightopedia", page_icon="💡",layout="wide")

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #F8FAFC;
}
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
}
.stDownloadButton>button {
    background-color: #16A34A;
    color: white;
    border-radius: 10px;
}
.stExpander {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,3])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80)

with col2:
    st.title("Insightopedia")
    st.subheader("From Research Papers to Insurance Policy —Best friend of a common man.")
    st.caption("AI-powered document intelligence for research & insurance")


st.sidebar.title("Navigation")
option= st.sidebar.selectbox("Choose Content Type", ["Research Paper","Insurance Policy"])

if  option=='Research Paper':
    st.header("📄 Research Paper Analyser")
    st.warning("AI-generated academic summary. Verify with original paper before citing.")
    upload_file= st.file_uploader("Upload a Research Paper(PDF)", type=["pdf"])

    if upload_file is not None:
        if upload_file.size>8*1024*1024:
            st.error("File size must be under 8MB")
        elif upload_file.type != "application/pdf":
            st.error("Invalid File Type. Please upload PDF")
        else:

            try:

                st.success("File uploaded successfully")
                with st.spinner("Extracting text..."):
                    Text= utils.extract_text_from_pdf (upload_file)

                    if not Text.strip():
                        st.error("Could not extract readable text from PDF.")
                        st.stop()

                with st.spinner("Analysing..."):
                    Result=utils.smart_trim(Text)
                    final_result=utils.generate_response(prompts.research_prompt(Result))
                st.subheader("AI Analysis Report")
                with st.expander("View full Analysis"):
                    if "⚠️" in final_result:
                        st.error(final_result)
                    else:
                        st.markdown("### 📊 Structured Analysis Report")
                        st.markdown(final_result)
                # Download button
                    pdf_file = utils.generate_pdf(final_result)

                    st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_file,
                    file_name="research_analysis.pdf",
                    mime="application/pdf")

        
            except Exception as e:
                st.error("Something went wrong. Please try again")
    
    else:
        st.info("Please upload a file to begin the analysis")

elif option == "Insurance Policy":
    st.header("🛡 Insurance Policy Insight")

    st.warning("This AI analysis does not replace professional financial advice.")

    upload_file = st.file_uploader(
        "Upload Insurance Policy (PDF or Image)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if upload_file is not None:

        if upload_file.size > 8 * 1024 * 1024:
            st.error("File size must be under 8MB.")
            st.stop()

        try:
            with st.spinner("Extracting text..."):
                if upload_file.type == "application/pdf":
                    Text = utils.extract_text_from_pdf(upload_file)
                else:
                    Text = utils.extract_text_from_image(upload_file)

            if not Text.strip():
                st.error("Could not extract readable text.")
                st.stop()
                
            with st.spinner("Analyzing Insurance Policy..."):
                processed_text = utils.smart_trim(Text)
                final_result = utils.generate_response(prompts.insurance_prompt(processed_text))

            st.success("Policy Analysis Complete")
            st.subheader("Insurance Insight Report")
            with st.expander("View full Analysis"):
                if "⚠️" in final_result:
                    st.error(final_result)
                else:
                    st.markdown("### 📊 Structured Analysis Report")
                    st.markdown(final_result)
            # Download button
            pdf_file = utils.generate_pdf(final_result)

            st.download_button(
                label="📥 Download as PDF",
                data=pdf_file,
                file_name="Insurance_Insight.pdf",
                 mime="application/pdf"
)
        except Exception as e:
            st.error("Something went wrong while processing the policy. Please try again")
            st.write(e)

    else:
        st.info("Please upload an insurance policy document.")

st.markdown("---")
st.caption("© 2026 Insightopedia | AI-Powered Document Intelligence")
 