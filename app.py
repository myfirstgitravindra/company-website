from flask import Flask, render_template
import os

app = Flask(__name__)

# File to store visitor count
COUNT_FILE = '/data/visitor_count.txt'

def get_visitor_count():
    """Read the current visitor count from file."""
    try:
        if os.path.exists(COUNT_FILE):
            with open(COUNT_FILE, 'r') as f:
                count = int(f.read().strip())
        else:
            count = 0
    except:
        count = 0
    return count

def increment_visitor_count():
    """Increment and save the visitor count."""
    count = get_visitor_count() + 1
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(COUNT_FILE), exist_ok=True)
        with open(COUNT_FILE, 'w') as f:
            f.write(str(count))
    except:
        pass
    return count

@app.route('/')
def home():
    """Main page that shows visitor count."""
    count = increment_visitor_count()
    return render_template('index.html', visitor_count=count)

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes."""
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)