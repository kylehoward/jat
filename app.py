from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    ("Wellfound", "https://wellfound.com"),
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
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', sites=SITES)

@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if request.method == 'POST':
        site = request.form['site']
        status = request.form['status']
        notes = request.form['notes']
        db.session.add(Application(site=site, status=status, notes=notes))
        db.session.commit()
        return redirect(url_for('tracker'))
    applications = Application.query.all()
    return render_template('tracker.html', sites=SITES, applications=applications)

@app.route('/report')
def report():
    data = db.session.query(Application.site, db.func.count()).group_by(Application.site).all()
    return render_template('report.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
