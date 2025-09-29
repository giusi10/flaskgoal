from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import TextAreaField

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

class GameForm(FlaskForm):
    team1 = StringField('Team 1', validators=[DataRequired()])
    team2 = StringField('Team 2', validators=[DataRequired()])
    date = DateTimeField(
        'Spielzeit (HH:MM TT.MM.JJJJ)',
        format='%H:%M %d.%m.%Y',
        validators=[DataRequired()]
    )
    location = StringField('Austragungsort', validators=[DataRequired()])
    submit = SubmitField('Spiel erstellen')

class PredictionForm(FlaskForm):
    tip_team1 = IntegerField('Tore Team 1', validators=[DataRequired()])
    tip_team2 = IntegerField('Tore Team 2', validators=[DataRequired()])
    submit = SubmitField('Tipp abgeben')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Passwort-Zurücksetzen-Link senden')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Neues Passwort', validators=[DataRequired()])
    password2 = PasswordField('Wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Passwort zurücksetzen')

class CommentForm(FlaskForm):
    content = TextAreaField('Kommentar', validators=[DataRequired()])
    submit = SubmitField('Absenden')

class ManualResetPasswordForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Neues Passwort', validators=[DataRequired()])
    confirm_password = PasswordField('Passwort bestätigen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Passwort zurücksetzen')