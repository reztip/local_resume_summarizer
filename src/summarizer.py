from pathlib import Path
import re
import os
from typing import Union
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage


def get_model():
    prompt_template = ChatPromptTemplate([
        ("system", 
         """
         You are an assistant who summarizes resumes from job applications; your resulting output should be a two paragraph summary about the candidate.
         If the resume is too long, you can summarize the most important parts.
         If a job description is available, you should add an additional paragraph that compares the candidate's skills to the job requirements.
         Really be critical in assessing the candidate and job fit as there are probably a large amount of candidates.
         In the second section, also give some suggestions to candidates on how they can make their interview successful in relation to their skills and the job description.
         If no job description is provided, the second section should be omitted.
         The responses should be in markdown format, with headings and paragraphs.
         If the inputs are not really job descriptions or resumes, you can ask the user to provide a real resume or job description.
         """),
        MessagesPlaceholder("resume"),
        MessagesPlaceholder("job_description"),
    ])
    model_name = os.getenv('MODEL_NAME', 'deepseek-r1:14b')
    model = Ollama(model = model_name)
    chain = prompt_template | model
    return chain

def load_pdf(file_path):
    """Load and process PDF file"""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages

def split_text(pages):
    """Split the loaded text into chunks for processing"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10
    )
    texts = splitter.split_documents(pages)
    return texts

def summarize_pdf(resume_path: Union[str, Path], job_description: str = None) -> str:
    """Main function to load, split and summarize the PDF content"""
    job_description = job_description or ''
    pages = load_pdf(resume_path)
    texts = split_text(pages)
    model = get_model()
    results = model.invoke({
        'resume': [HumanMessage('\n'.join(text.page_content for text in texts))],
        'job_description': [SystemMessage(job_description)],
    })
    results = re.sub(r'<think>.*?</think>', '', results, flags=re.DOTALL)
    return results

