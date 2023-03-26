from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'specter'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Url_saver(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    input_url = db.Column("input_url", db.String())
    shortened_url = db.Column("shortened_url", db.String())

    def __init__(self, input_url, shortened_url):
        self.input_url = input_url
        self.shortened_url = shortened_url

def shorten_url():
    letters = string.ascii_letters
    return r''.join(random.choice(letters) for i in range(10))


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form.get("input_url")
        hashid=shorten_url()
        base_url=os.path.dirname(url_received)
        shortened_url=os.path.join(base_url,hashid)
        url_to_be_added = Url_saver(input_url=request.form.get('input_url'),
                    shortened_url=shortened_url)
        db.session.add(url_to_be_added)
        db.session.commit()
        print(shortened_url)
        return render_template('url_page.html',url_to_be_added=shortened_url,url_received=url_received)
    else:
        url_to_be_added=""
        return render_template('url_page.html',url_to_be_added=url_to_be_added,url_received=url_to_be_added)


@app.route("/copy",methods=["POST"])
def copy_url():
    if request.method=="POST":
        shortened_url=request.form.get("shortened_url")
        original_url = Url_saver.query.filter_by(shortened_url=shortened_url).first()
        if original_url:
            return f"Your input URL <h3>{original_url.input_url}</h3> got saved"
        else:
            return f'<h1>Url doesnt exist</h1>'

@app.route('/all_urls')
def display_all():
    return render_template('History_page.html', vals=Url_saver.query.all())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
