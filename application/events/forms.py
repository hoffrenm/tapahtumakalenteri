from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.fields.html5 import TimeField, DateField

class EventForm(FlaskForm):
    name = StringField("Tapahtuman nimi", [validators.Length(min=4)])
    location = StringField("Tapahtuman sijainti", [validators.Length(min=4)])
    time = TimeField("Kellonaika", format='%H:%M')
    date = DateField("Päivämäärä", format='%Y-%m-%d')

    class Meta:
        csrf = False