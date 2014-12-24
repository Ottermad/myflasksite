from flask import Flask, render_template, request, redirect, url_for

# using SendGrid's Python Library - https://github.com/sendgrid/sendgrid-python
import sendgrid

app = Flask(__name__)

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


@app.route("/send_email", methods=["POST"])
def send_email():
	sendgrid_object = sendgrid.SendGridClient("Ottermad", "OttersR0ck")
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