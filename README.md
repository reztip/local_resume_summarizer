# Resume and Job Description Summarizer

This is a small demo application made in afternoon by "vibe coding", to assist either an HR Person or a candidate assess how a resume fares in relation to a job description by leaning on an LLM to do summarization.
The summaries can help in tailoring resumes to specific job applications, or good interview focus areas.

It would be straightforward to Dockerize or package this.

## Features

- Upload resumes in PDF format.
- Enter job descriptions with rich text support.
- Generate summaries for both resumes and job descriptions.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Ollama with relevant models installed, of your choosing

### Dependencies

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### Running the Application

0. Ensure Ollama (https://ollama.com/download) and your model of choice are installed, e.g. Llama3.2 or Deepseek.

Set the relevant environment variable for your model name, e.g.
```bash
export MODEL_NAME=llama3.2
```

1. Clone the repository:

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run src/__main__.py
```

4. Open your web browser and go to `http://localhost:8501` to access the application.

## Usage

1. **Upload Resume**: Use the "Upload Resume" section to upload your resume in PDF format.
2. **Enter Job Description**: Use the "Enter Job Description" section to paste the job description text.
3. The application will generate summaries for both the resume and the job description.

## License

Feel free to use this however you want, as either an HR person or a candidate.
