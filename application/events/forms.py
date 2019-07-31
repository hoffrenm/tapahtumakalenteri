from flask_wtf import FlaskForm
from wtforms import StringField, validators

class EventForm(FlaskForm):
    name = StringField("Tapahtuman nimi", [validators.Length(min=4)])
    location = StringField("Tapahtuman sijainti", [validators.Length(min=4)])
 
    class Meta:
        csrf = False