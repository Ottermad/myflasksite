from flask import Flask, render_template, request, redirect, url_for, g, session,abort, flash
import sqlite3
from contextlib import closing
import sendgrid

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def portfolio():
	context = {"page": "portfolio"}
	return render_template("portfolio.html", **context)

@app.route("/about")
def about():
	context = {"page": "about"}
	return render_template("about.html", **context)

@app.route("/contact")
def contact():
	context = {"page": "contact"}
	return render_template("contact.html", **context)

@app.route('/show_entries')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route("/send_email", methods=["POST"])
def send_email():
	sendgrid_object = sendgrid.SendGridClient("", "")
	message = sendgrid.Mail()
	sender = request.form["email"]
	subject = request.form["subject"]
	body = request.form["emailbody"]
	message.add_to("charlie.thomas@attwoodthomas.net")
	message.set_from(sender)
	message.set_subject(subject)
	message.set_html(body)

	sendgrid_object.send(message)

	return redirect(url_for('contact'))
if __name__ == "__main__":
	app.run(debug=True)
