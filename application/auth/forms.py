from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus", render_kw={"class": "form-control"})
    password = PasswordField("Salasana", render_kw={"class": "form-control"})
  
    class Meta:
        csrf = False

class AccountCreateForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2)], render_kw={"class": "form-control"})
    username = StringField("Käyttäjätunnus", [validators.Length(min=3)], render_kw={"class": "form-control"})
    password = PasswordField("Salasana", [validators.Length(min=6)], render_kw={"class": "form-control"})
    
    class Meta:
        csrf = False
