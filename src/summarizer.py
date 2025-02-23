from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama

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

def summarize_pdf(file_path):
    """Main function to load, split and summarize the PDF content"""
    pages = load_pdf(file_path)
    texts = split_text(pages)
    
    # Create summarization chain with LLM
    summary_chain = Ollama(model = 'deepseek-context')
    
    # Process all chunks in parallel
    results = summary_chain.invoke([text.content for text in texts])

    print(results)
    
    return results

