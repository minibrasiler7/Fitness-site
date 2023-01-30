from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email
import email_validator


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Pseudo', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Register')

class FitnessForm(FlaskForm):
    fitness_name = StringField('Nom', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    photo_url = FileField('URL image du fitness', validators=[DataRequired()])
    adresse_url = StringField("URL de l'adresse", validators=[DataRequired()])
    note_equipement = SelectField("Equipement", choices=["Je ne souhaite pas donner mon avis", 'hello', '🏋🏋', "🏋🏋🏋", "🏋🏋🏋🏋", "🏋🏋🏋🏋🏋"])
    note_personnel = SelectField("Personnel", choices=["Je ne souhaite pas donner mon avis", '🙋',"🙋🙋", "🙋🙋🙋", "🙋🙋🙋🙋", "🙋🙋🙋🙋🙋"])
    note_proprete = SelectField("Propreté", choices=["Je ne souhaite pas donner mon avis",'🧹', "🧹🧹", "🧹🧹🧹", "🧹🧹🧹🧹", "🧹🧹🧹🧹🧹"])
    note_cours = SelectField("Cours", choices=["Je ne souhaite pas donner mon avis", '💪', "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    is_spa = BooleanField("Y'a t-il une zone SPA ?", validators=[DataRequired()])
    note_spa = SelectField("Zone spa", choices=["Je ne souhaite pas donner mon avis",'🧖', "🧖‍🧖‍", "🧖‍🧖‍🧖‍", "🧖‍🧖‍🧖‍🧖‍", "🧖‍🧖‍🧖‍🧖‍🧖‍"])
    prix_mensuel = FloatField("Prix mensuel moyen pour un accès complet", validators=[DataRequired()])
    submit = SubmitField('Register')

