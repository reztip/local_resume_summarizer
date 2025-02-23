from pathlib import Path
import re
import os
import json
from typing import Union
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage


def get_prompt():
    with open("./src/prompts.json", "r") as file:
        prompts = json.load(file)
        return ChatPromptTemplate([
            ("system",
            prompts['summarizer']
            )
        ])

def get_model():
    prompt_template = ChatPromptTemplate([
        get_prompt(),
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

