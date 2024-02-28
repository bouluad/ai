import os
import openai
from langchain import Encoder
from github import Github

# Set up OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to fetch Markdown files from GitHub repository recursively
def fetch_markdown_files(repo_url):
    # Initialize GitHub instance
    g = Github()
    repo = g.get_repo(repo_url)

    markdown_files = []

    # Recursively fetch Markdown files
    def fetch_files_recursive(directory):
        contents = repo.get_contents(directory)
        for content in contents:
            if content.type == "file" and content.path.endswith('.md'):
                markdown_files.append(content.download_url)
            elif content.type == "dir":
                fetch_files_recursive(content.path)

    fetch_files_recursive("")
    
    return markdown_files

# Function to read Markdown content from file URLs
def read_markdown_files(markdown_files):
    markdown_content = ""
    for file_url in markdown_files:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Read Markdown from URL: {file_url}\n",
            max_tokens=100
        )
        markdown_content += response.choices[0].text.strip()
    return markdown_content

# Function to generate answer using OpenAI API
def generate_answer(question, markdown_content):
    # Initialize Langchain encoder
    encoder = Encoder()

    # Encode question and markdown content as prompt
    prompt = f"Question: {question}\nContext: {markdown_content}\nAnswer:"

    # Generate answer using OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    # Extract the generated answer from the response
    answer = response.choices[0].text.strip()
    
    return answer

if __name__ == "__main__":
    # Accept repository URL as input
    repo_url = input("Enter GitHub repository URL (e.g., username/repository): ")

    # Fetch Markdown files recursively
    markdown_files = fetch_markdown_files(repo_url)

    # Read Markdown content from files
    markdown_content = read_markdown_files(markdown_files)

    # Ask a question
    question = input("Ask a question: ")

    # Generate answer
    answer = generate_answer(question, markdown_content)

    # Display answer
    print("Answer:", answer)
