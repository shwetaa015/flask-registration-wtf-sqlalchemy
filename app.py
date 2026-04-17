from flask_wtf import FlaskForm
from flask import Flask, render_template, request
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


web = Flask(__name__)
web.config['SECRET_KEY']='mysecret123'

web.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(web)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

@web.route('/', methods=['POST', 'GET'])
@web.route('/register', methods=['POST', 'GET'])

def home():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name = form.name.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()

        return render_template('confirmation.html', name = form.name.data, email=form.email.data)

    return render_template('register.html', form=form)


if __name__ == "__main__":
    web.run(debug=True)
