import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

DEBUG_API_KEY = os.getenv("API_KEY", "default_safe_value") 

@app.route('/')
def index():
    return "<h1>Welcome to the Secure Pipeline Lab!</h1>"

@app.route('/search')
def search():
    user_input = request.args.get('q', '')
    # nosemgrep: python.flask.security.audit.render-template-string.render-template-string
    return render_template_string("<h1>Searching for: {{ query }}</h1>", query=user_input)

@app.route('/ping')
def ping():
    host = request.args.get('host', '')
    # VULNERABLE: unsanitized user input passed to a shell command
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return result.stdout

@app.route('/vulnerable-search')
def vulnerable_search():
    user_input = request.args.get('q', '')
    # VULNERABLE: raw user input concatenated directly into the template source (SSTI)
    template = "<h1>Searching for: " + user_input + "</h1>"
    return render_template_string(template)

if __name__ == "__main__":
    # nosemgrep: python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host
    app.run(host='0.0.0.0', port=5000)