from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email, URL


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
    lundi_ouverture = SelectField("Lundi ouverture", choices=time)
    lundi_fermeture = SelectField("Lundi fermeture", choices=time)
    mardi_ouverture = SelectField("Mardi ouverture", choices=time)
    mardi_fermeture = SelectField("Mardi fermeture", choices=time)
    mercredi_ouverture = SelectField("Mercredi ouverture", choices=time)
    mercredi_fermeture = SelectField("Mercredi fermeture", choices=time)
    jeudi_ouverture = SelectField("Jeudi ouverture", choices=time)
    jeudi_fermeture = SelectField("Jeudi fermeture", choices=time)
    vendredi_ouverture = SelectField("Vendredi ouverture", choices=time)
    vendredi_fermeture = SelectField("Vendredi fermeture", choices=time)
    samedi_ouverture = SelectField("Samedi ouverture", choices=time)
    samedi_fermeture = SelectField("Samedi fermeture", choices=time)
    dimanche_ouverture = SelectField("Dimanche ouverture", choices=time)
    dimanche_fermeture = SelectField("Dimanche fermeture", choices=time)
    submit = SubmitField('Enregistrer')

class CommentaireForm(FlaskForm):
     note_equipement = SelectField("Equipement", choices=["Je ne souhaite pas donner mon avis", '🏋', '🏋🏋', "🏋🏋🏋", "🏋🏋🏋🏋", "🏋🏋🏋🏋🏋"])
     note_personnel = SelectField("Personnel", choices=["Je ne souhaite pas donner mon avis", '🙋',"🙋🙋", "🙋🙋🙋", "🙋🙋🙋🙋", "🙋🙋🙋🙋🙋"])
     note_proprete = SelectField("Propreté", choices=["Je ne souhaite pas donner mon avis",'🧹', "🧹🧹", "🧹🧹🧹", "🧹🧹🧹🧹", "🧹🧹🧹🧹🧹"])
     note_cours = SelectField("Cours", choices=["Je ne souhaite pas donner mon avis", '💪', "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
     note_spa = SelectField("Zone spa", choices=["Je ne souhaite pas donner mon avis","💆", "💆💆", "💆💆💆", "💆💆💆💆", "💆💆💆💆💆"])
     note_piscine = SelectField("Piscine", choices=["Je ne souhaite pas donner mon avis", '🏊', "🏊🏊", "🏊🏊🏊", "🏊🏊🏊🏊", "🏊🏊🏊🏊🏊"])
     commenter = SubmitField('Register')



