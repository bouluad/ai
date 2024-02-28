import os
import json
from github import Github, GithubIntegration
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# GitHub App credentials
app_id = os.getenv('GITHUB_APP_ID')
private_key_path = os.getenv('GITHUB_PRIVATE_KEY_PATH')

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# GitHub repository and branch
repo_name = "example/repository"
branch_name = "main"

# Organization name
org_name = "org"

# Read configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize GitHub App
private_key = open(private_key_path, 'r').read()
integration = GithubIntegration(app_id, private_key)
github = Github(integration)

# Function to generate Dockerfile using OpenAI's API
def generate_dockerfile(language, project_structure):
    base_image = config.get(language.lower(), "scratch")  # Default to an empty image if language is not recognized

    if isinstance(base_image, str):
        base_image_str = base_image
    else:
        build_stage = base_image.get("build_stage", "")
        run_stage = base_image.get("run_stage", "")
        base_image_str = f"Build stage image: {build_stage}\nRun stage image: {run_stage}"

    prompt = f"Generate a Dockerfile for a {language} project with the following structure:\n{project_structure}\n\nBase image(s) from config: {base_image_str}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].text.strip()

# Function to create or update a file in a GitHub repository
def create_or_update_file(repo, branch, file_path, file_content, commit_message):
    try:
        contents = repo.get_contents(file_path, ref=branch)
        repo.update_file(contents.path, commit_message, file_content, contents.sha, branch=branch)
        print(f"Updated {file_path} in {repo_name}")
    except Exception as e:
        repo.create_file(file_path, commit_message, file_content, branch=branch)
        print(f"Created {file_path} in {repo_name}")

# Function to fork a repository to an organization
def fork_repository_to_org(repo, org_name):
    org = github.get_organization(org_name)
    return org.create_fork(repo)

# Fetch repository information
repo = github.get_repo(repo_name)
repo_language = repo.language

print(f"The primary programming language of {repo_name} is: {repo_language}")

# Fetch project structure
contents = repo.get_contents("", ref=branch_name)
project_structure = ""
for content_file in contents:
    project_structure += f"{content_file.path}\n" if content_file.type == "file" else f"{content_file.path}/\n"

print(f"The project structure of {repo_name} is:\n{project_structure}")

# Fork repository to organization
forked_repo = fork_repository_to_org(repo, org_name)

# Generate Dockerfile based on repository language and project structure
dockerfile_content = generate_dockerfile(repo_language, project_structure)

# Path to save Dockerfile in the repository
dockerfile_path = "Dockerfile"

# Create or update Dockerfile in the forked repository
create_or_update_file(forked_repo, branch_name, dockerfile_path, dockerfile_content, "Update Dockerfile")

# Create a pull request from the forked repository to the original repository
pull_request_title = "Update Dockerfile"
pull_request_body = "Automatically generated Dockerfile."

pull_request = forked_repo.create_pull(
    title=pull_request_title,
    body=pull_request_body,
    base=repo.default_branch,  # Base branch of the original repository
    head=f"{org_name}:{branch_name}"  # Head branch of the forked repository
)

print("Pull request created:", pull_request.html_url)
