from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, URL
import email_validator


time = ["fermé", "24/24"]

for i in range(288):
    minute = i*5
    heure = minute//60
    minute_restante = minute - 60*heure
    if heure <10:
        heure = f"0{heure}"
    if minute_restante<10:
        minute_restante= f"0{minute_restante}"
    temps_string = f"{heure}:{minute_restante}"
    time.append(temps_string)



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
    photo = StringField("URL de l'image", validators=[DataRequired(), URL()])
    adresse_url = StringField("URL de l'adresse", validators=[DataRequired(), URL()])
    site_url = StringField("URL du site", validators=[DataRequired(), URL()])
    note_equipement = SelectField("Equipement", choices=["Je ne souhaite pas donner mon avis", '🏋', '🏋🏋', "🏋🏋🏋", "🏋🏋🏋🏋", "🏋🏋🏋🏋🏋"])
    note_personnel = SelectField("Personnel", choices=["Je ne souhaite pas donner mon avis", '🙋',"🙋🙋", "🙋🙋🙋", "🙋🙋🙋🙋", "🙋🙋🙋🙋🙋"])
    note_proprete = SelectField("Propreté", choices=["Je ne souhaite pas donner mon avis",'🧹', "🧹🧹", "🧹🧹🧹", "🧹🧹🧹🧹", "🧹🧹🧹🧹🧹"])
    is_cours = BooleanField("Y'a t-il des cours ?")
    note_cours = SelectField("Cours", choices=["Je ne souhaite pas donner mon avis", '💪', "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    is_spa = BooleanField("Y'a t-il une zone SPA ?")
    note_spa = SelectField("Zone spa", choices=["Je ne souhaite pas donner mon avis","💆", "💆💆", "💆💆💆", "💆💆💆💆", "💆💆💆💆💆"])
    is_piscine = BooleanField("Y'a t-il une piscine?")
    note_piscine = SelectField("Piscine", choices=["Je ne souhaite pas donner mon avis", '🏊', "🏊🏊", "🏊🏊🏊", "🏊🏊🏊🏊", "🏊🏊🏊🏊🏊"])
    prix_mensuel = FloatField("Prix mensuel moyen pour un accès complet", validators=[DataRequired()])
    lundi_ouverture = StringField('Lundi ouverture', validators=[DataRequired()])
    lundi_fermeture = StringField('Lundi fermeture', validators=[DataRequired()])
    mardi_ouverture = StringField('Mardi ouverture', validators=[DataRequired()])
    mardi_fermeture = StringField('Mardi fermeture', validators=[DataRequired()])
    mercredi_ouverture = StringField('Mercredi ouverture', validators=[DataRequired()])
    mercredi_fermeture = StringField('Mercredi fermeture', validators=[DataRequired()])
    jeudi_ouverture = StringField('Jeudi ouverture', validators=[DataRequired()])
    jeudi_fermeture = StringField('Jeudi fermeture', validators=[DataRequired()])
    vendredi_ouverture = StringField('Vendredi ouverture', validators=[DataRequired()])
    vendredi_fermeture = StringField('Vendredi fermeture', validators=[DataRequired()])
    samedi_ouverture = StringField('Samedi ouverture', validators=[DataRequired()])
    samedi_fermeture = StringField('Samedi fermeture', validators=[DataRequired()])
    dimanche_ouverture = StringField('Dimanche ouverture', validators=[DataRequired()])
    dimanche_fermeture = StringField('Dimanche fermeture', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class CommentaireForm(FlaskForm):
     note_equipement = SelectField("Equipement", choices=["Je ne souhaite pas donner mon avis", '🏋', '🏋🏋', "🏋🏋🏋", "🏋🏋🏋🏋", "🏋🏋🏋🏋🏋"])
     note_personnel = SelectField("Personnel", choices=["Je ne souhaite pas donner mon avis", '🙋',"🙋🙋", "🙋🙋🙋", "🙋🙋🙋🙋", "🙋🙋🙋🙋🙋"])
     note_proprete = SelectField("Propreté", choices=["Je ne souhaite pas donner mon avis",'🧹', "🧹🧹", "🧹🧹🧹", "🧹🧹🧹🧹", "🧹🧹🧹🧹🧹"])
     note_cours = SelectField("Cours", choices=["Je ne souhaite pas donner mon avis", '💪', "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
     note_spa = SelectField("Zone spa", choices=["Je ne souhaite pas donner mon avis","💆", "💆💆", "💆💆💆", "💆💆💆💆", "💆💆💆💆💆"])
     note_piscine = SelectField("Piscine", choices=["Je ne souhaite pas donner mon avis", '🏊', "🏊🏊", "🏊🏊🏊", "🏊🏊🏊🏊", "🏊🏊🏊🏊🏊"])
     commenter = SubmitField('Register')


class ContactForm(FlaskForm):
     nom = StringField('Nom de votre fitness', validators=[DataRequired()])
     email = StringField('Votre email', validators=[DataRequired()])
     adresse = StringField('Adresse de votre fitness', validators=[DataRequired()])
     code_postal = IntegerField(validators=[DataRequired()])
     ville = StringField('Ville de votre fitness', validators=[DataRequired()])
     is_piscine = BooleanField("Y'a t-il une piscine? Cocher si oui")
     is_spa = BooleanField("Y'a t-il un sauna ou hammam? Cocher si oui")
     is_cours = BooleanField("Y'a t-il des cours collectifs? Cocher si oui")
     envoyer = SubmitField('Envoyer')

class Updateform(FlaskForm):
     nom = StringField('Nom de votre fitness', validators=[DataRequired()])
     url_site = StringField('Site du fitness', validators=[DataRequired()])
     url_map = StringField('URL google maps', validators=[DataRequired()])
     url_image = StringField('URL image du fitness', validators=[DataRequired()])
     adresse = StringField('Adresse de votre fitness', validators=[DataRequired()])
     code_postal = IntegerField(validators=[DataRequired()])
     ville = StringField('Ville de votre fitness', validators=[DataRequired()])
     is_piscine = BooleanField("Y'a t-il une piscine? Cocher si oui")
     is_spa = BooleanField("Y'a t-il un sauna ou hammam? Cocher si oui")
     is_cours = BooleanField("Y'a t-il des cours collectifs? Cocher si oui")
     envoyer = SubmitField('Envoyer')



