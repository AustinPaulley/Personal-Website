from flask import Flask, render_template, request
import requests
from requests.exceptions import RequestException
import os

app = Flask(__name__)

# Metadata for known repos: tech stack + difficulty
PROJECT_META = {
    "personal-website": {
        "tech": ["Flask", "Python", "HTML", "CSS", "JavaScript"],
        "difficulty": "Intermediate",
        "difficulty_class": "intermediate"
    },
    "Linkedin-Scraper-and-Ai-Phishing-Email-Generator": {
        "tech": ["Python", "Flask", "MongoDB", "OpenAI", "Selenium", "BeautifulSoup"],
        "difficulty": "Research-Level",
        "difficulty_class": "research"
    },
    "Data-Dynamos": {
        "tech": ["Python", "Flask", "Excel"],
        "difficulty": "Intermediate",
        "difficulty_class": "intermediate"
    },
    "Java-2-Code": {
        "tech": ["Java"],
        "difficulty": "Beginner",
        "difficulty_class": "beginner"
    },
    "CollegePython": {
        "tech": ["Python"],
        "difficulty": "Beginner",
        "difficulty_class": "beginner"
    },
}

@app.route('/')
def home():
    github_username = 'AustinPaulley'
    # Define specific repos to fetch
    repo_urls = [
        f'https://api.github.com/repos/{github_username}/personal-website',
        f'https://api.github.com/repos/{github_username}/Linkedin-Scraper-and-Ai-Phishing-Email-Generator'
    ]
    projects = []
    for url in repo_urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            repo = response.json()
        except RequestException:
            repo = {
                'name': 'Error',
                'description': f'Failed to load repo: {url}',
                'html_url': url
            }
        projects.append(repo)

    return render_template('home.html', projects=projects, active_page='home')


@app.route('/resume')
def resume():
    return render_template('resume.html', active_page='resume')


@app.route('/projects')
def projects():
    github_username = 'AustinPaulley'
    url = f'https://api.github.com/users/{github_username}/repos'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        projects = response.json()
    except RequestException:
        projects = []

    # Attach tech stack + difficulty to each project
    for project in projects:
        name = project.get("name", "")
        meta = PROJECT_META.get(name, None)

        if meta:
            project["tech_stack"] = meta["tech"]
            project["difficulty"] = meta["difficulty"]
            project["difficulty_class"] = meta["difficulty_class"]
        else:
            # Sensible defaults for repos without explicit metadata
            project["tech_stack"] = ["Python"]
            project["difficulty"] = "Intermediate"
            project["difficulty_class"] = "intermediate"

    return render_template('projects.html', projects=projects, active_page='projects')


@app.route('/writeups')
def writeups():
    return render_template('writeups.html', active_page='writeups')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    name = None

    if request.method == 'POST':
        name = request.form.get('name')
        success = True

    return render_template('contact.html', success=success, name=name, active_page='contact')


@app.route('/websites')
def websites():
    return render_template('websites.html', active_page='websites')


@app.route('/ai-project')
def ai_project():
    return render_template('ai_project.html', active_page='ai_project')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
