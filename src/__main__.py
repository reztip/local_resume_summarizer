import streamlit as st
import os
import db_manager
import summarizer

def main():
    manager = db_manager.DBManager()
    with manager:
        manager.global_init()
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    st.set_page_config(page_title="PDF Upload App",
                      layout="centered")

    st.title("Resume and Job Description Summarizer")

    job_description = None
    with st.expander("Enter Job Description"):
        job_description = st.text_area(
            "Paste the job description here",
            height=300,
            help="You can paste the job description text here, including rich text from PDFs or Word files."
        )

    with st.expander("Upload Resume"):
        with manager:
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=['pdf'],
                accept_multiple_files=False,
                key=None,
                help="Upload one or more PDF files to process"
            )

            if uploaded_file is not None:
                # Save uploaded file
                filepath = os.path.join("uploads", uploaded_file.name)
                def save_uploaded_file(uploaded_file):
                    with open(filepath, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    return uploaded_file

                file = save_uploaded_file(uploaded_file)
                path = os.path.join("uploads", file.name)   
                with st.spinner("Summarizing Resume...", show_time=True):
                    summary = summarizer.summarize_pdf(path, job_description=job_description)
                    manager.insert((summary, path))
                st.success(f"File {file.name} was successfully uploaded!")
                st.markdown(summary)


    if len(st.session_state) > 0 and 'uploaded_files' in st.session_state:
        st.subheader("Uploaded Files")
        for file in st.session_state.uploaded_files:
            st.write(f"- {file['name']} ({file['size']} bytes)")

if __name__ == "__main__":
    main()

