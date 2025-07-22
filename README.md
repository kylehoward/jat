# Job Application Tracker – Complete Installation & Usage Guide (2025)

This document provides everything you need to install, configure, and run the enhanced Job Application Tracker with per-job tracking, platform job counters, reporting, email, and management—all backed by Docker and Flask.

## 🚀 Quick-Start Installation Instructions

### 1. Prerequisites

- **Docker Desktop installed and running**
    - Download for Windows, Mac, or Linux from the Docker website.
    - No need to install Python, pip, or any dependencies locally.
- **Optional Editor** (VS Code, Notepad++, etc.) for modifying files.

### 2. Preparing Your Project Folder

1. **Create a new folder called `job-tracker`.**

2. **Inside that folder, create these files:**
    - `Dockerfile`
    - `requirements.txt`
    - `app.py`
    - A `templates/` subfolder with the HTML files:
        - `index.html`
        - `tracker.html`
        - `report.html`
        - `management.html`
        - `settings.html`

3. **Copy the code from the sections below into the proper file, matching filenames.**

### 3. Build and Run the Application

Open a terminal/PowerShell, `cd` into your `job-tracker` directory, and run:

```powershell
docker build -t jobtracker .
```

Once the image is built, start the app:

```powershell
docker run -p 5000:5000 jobtracker
```

**Then open your browser to [http://localhost:5000](http://localhost:5000).**

### 4. First-Time Setup

- **No manual database steps:** The app auto-creates its database (`jobs.db`) on first run.
- **Configure email:** Go to "Report Email Settings" in the web UI to input SMTP username/password.
- **You can now add job applications per site and enjoy tracking/reporting!**

# Source Files

## `requirements.txt`

```text
flask
flask_sqlalchemy
flask_mail
flask_wtf
bcrypt
```

## `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
```

## `app.py`

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-to-a-strong-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mail = Mail(app)

SITES = [
    ("Y Combinator (Work at a Startup)", "https://www.workatastartup.com"),
    ("Government Jobs", "https://www.governmentjobs.com"),
    ("Welcome to the Jungle (Otta)", "https://www.welcometothejungle.com/en"),
    ("EchoJobs", "https://echojobs.io"),
    ("Twitter", "https://twitter.com"),
    ("Levels.fyi", "https://www.levels.fyi/jobs/"),
    ("Carbons Jobs", "https://jobs.carbons.io"),
    ("Built In", "https://builtin.com/jobs"),
    ("Handshake", "https://joinhandshake.com"),
    ("Wellfound (AngelList Talent)", "https://wellfound.com"),
    ("Dice", "https://www.dice.com"),
    ("Jobright", "https://jobright.com"),
    ("Indeed", "https://www.indeed.com"),
    ("SimplyHired", "https://www.simplyhired.com"),
    ("ZipRecruiter", "https://www.ziprecruiter.com"),
    ("TrueUp.io", "https://www.trueup.io"),
    ("Monster", "https://www.monster.com"),
    ("RippleMatch", "https://ripplematch.com"),
    ("WayUp", "https://www.wayup.com"),
]

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    visible = db.Column(db.Boolean, default=True)

class ReportSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smtp_username = db.Column(db.String(256))
    smtp_password_hash = db.Column(db.String(256))

def apply_smtp_config():
    settings = ReportSettings.query.first()
    if settings:
        app.config['MAIL_SERVER'] = 'mail.kyle-howard.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        app.config['MAIL_USERNAME'] = settings.smtp_username or ''
        app.config['MAIL_PASSWORD'] = session.get('smtp_password', '')

apply_smtp_config()

@app.before_first_request
def create_tables():
    db.create_all()
    if not ReportSettings.query.first():
        db.session.add(ReportSettings())
        db.session.commit()

@app.route('/')
def index():
    site_counts = {}
    for name, _ in SITES:
        count = Application.query.filter_by(site=name).count()
        site_counts[name] = count
    return render_template('index.html', sites=SITES, site_counts=site_counts)

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if request.method == 'POST':
        site = request.form['site']
        position = request.form['position']
        status = request.form['status']
        notes = request.form['notes']
        app_entry = Application(
            site=site,
            position=position,
            status=status,
            notes=notes,
            last_update=datetime.utcnow(),
            visible=True
        )
        db.session.add(app_entry)
        db.session.commit()
        return redirect(url_for('tracker'))
    applications = Application.query.order_by(Application.site, Application.last_update.desc()).all()
    return render_template('tracker.html', sites=SITES, applications=applications)

@app.route('/report', methods=['GET', 'POST'])
def report():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    applications = Application.query
    if start_date and end_date:
        try:
            sd = datetime.strptime(start_date, '%Y-%m-%d')
            ed = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            applications = applications.filter(Application.last_update >= sd, Application.last_update  timedelta(days=30)
    return not (app.status.lower() == "rejected" or stale)

@app.route('/management', methods=['GET', 'POST'])
def management():
    show_hidden = request.args.get('show_hidden', '0') == '1'
    apps = Application.query.order_by(Application.last_update.desc()).all()
    for a in apps:
        should_be_visible = is_active(a)
        if not should_be_visible and a.visible:
            a.visible = False
        elif should_be_visible and not a.visible:
            a.visible = True
    db.session.commit()
    if not show_hidden:
        apps = [a for a in apps if a.visible]
    return render_template('management.html', applications=apps, show_hidden=show_hidden)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    settings = ReportSettings.query.first()
    if request.method == 'POST':
        username = request.form['smtp_username']
        raw_pw = request.form['smtp_password']
        if username:
            settings.smtp_username = username
        if raw_pw:
            settings.smtp_password_hash = generate_password_hash(raw_pw)
        db.session.commit()
        flash('Settings updated.', 'success')
    return render_template('settings.html', settings=settings)

@app.route('/send_report', methods=['POST'])
def send_report():
    pw = request.form.get('smtp_password', '')
    settings = ReportSettings.query.first()
    if not (settings and check_password_hash(settings.smtp_password_hash or '', pw)):
        flash("Invalid password for SMTP. Not sending.", "error")
        return redirect(url_for('report'))
    session['smtp_password'] = pw
    apply_smtp_config()
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    applications = Application.query
    if start_date and end_date:
        sd = datetime.strptime(start_date, '%Y-%m-%d')
        ed = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        applications = applications.filter(Application.last_update >= sd, Application.last_update 


    Job Sites


    Job Search Sites
    
    {% for name, link in sites %}
        
            {{ name }} 
            ( #{{ site_counts[name] }} )
        
    {% endfor %}
    
    
        Track Applications | 
        View Report | 
        Manage Visibility | 
        Report Email Settings
    


```

## `templates/tracker.html`

```html



    Application Tracker


    Add Application
    
        Site:
        {% for name, link in sites %}
            {{ name }}{% endfor %}
        
        Position:
        
        Status:
        
            Applied
            Interviewing
            Rejected
            Offer
        
        Notes:
        
        Add
    
    Tracked Applications
    
        SitePositionStatusLast UpdateNotes
        {% for app in applications %}
        
            {{ app.site }}
            {{ app.position }}
            {{ app.status }}
            {{ app.last_update.strftime('%Y-%m-%d') }}
            {{ app.notes | default('', true) }}
        
        {% endfor %}
    
    
        Back to Home | 
        View Report
    


```

## `templates/report.html`

```html



    Applications Report


    Applications by Site
    
        Start Date: 
        End Date: 
        Preview Report
    
    
        Start Date: 
        End Date: 
        SMTP Password: 
        Send Report
    
    
        
            SitePositionStatusLast Update
        
        {% for app in data %}
        
            {{ app.site }}
            {{ app.position }}
            {{ app.status }}
            {{ app.last_update.strftime('%Y-%m-%d') }}
        
        {% endfor %}
    
    Platform Totals
    
        PlatformTotal AppsActive Apps
        {% for platform, _ in sites %}
        
            {{ platform }}
            {{ site_counts[platform] }}
            {{ active_counts[platform] }}
        
        {% endfor %}
    
    
        Back to Home | 
        Config Email Settings
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        
        {% for category, message in messages %}
          {{ message }}
        {% endfor %}
        
      {% endif %}
    {% endwith %}


```

## `templates/management.html`

```html



    Application Management


    Manage Application Visibility
    
        
            
            Show Inactive/Hidden Applications
        
        Update
    
    
        
            SitePositionStatusLast UpdateVisible
        
        {% for app in applications %}
        
            {{ app.site }}
            {{ app.position }}
            {{ app.status }}
            {{ app.last_update.strftime('%Y-%m-%d') }}
            {{ "Yes" if app.visible else "No" }}
        
        {% endfor %}
    
    
        Back to Home | 
        View Report
    


```

## `templates/settings.html`

```html



    Report Email Settings


    Configure Report Email SMTP
    
        SMTP Username:
        
        SMTP Password:
        
        Save Settings
    
    
        Back to Home | 
        View Report
    
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        
        {% for category, message in messages %}
          {{ message }}
        {% endfor %}
        
      {% endif %}
    {% endwith %}


```

# Notes for Markdown to Word Conversion

- All code blocks are in [fenced code block](https://pandoc.org/MANUAL.html#extension-fenced_code_blocks) syntax with language identifiers for best rendering during conversion.
- Blank lines are included above and below code blocks for compatibility.
- Copy this markdown file directly into Pandoc for best fidelity when exporting to DOCX.

Your **Job Application Tracker** is now fully ready for use!