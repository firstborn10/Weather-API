import requests, json
from flask import Flask, render_template, url_for, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cities = db.relationship('City', backref='creator')

    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class WeatherForm(FlaskForm):
    city = StringField('city', [validators.DataRequired()])
    state = StringField('state', [validators.DataRequired(),
                validators.Length(min=2, max=2, message="Please enter state as two letter abbreviation")])


@app.route("/", methods=['GET', 'POST'])
def weather_form():
    form = WeatherForm()
    if form.validate_on_submit():
        json_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={form.city.data}'
                                f',US-{form.state.data}&units=imperial&appid=a54927fdb382ca2ead788dda7e720314').json()
        return render_template('weather.html', form=form, response=json_response)
    return render_template('weather_form.html', form=form)
