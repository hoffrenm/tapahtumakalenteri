from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
from wtforms.fields.html5 import TimeField, DateField

class EventForm(FlaskForm):
    name = StringField("Tapahtuman nimi", [validators.Length(min=4)], render_kw={"class": "form-control"})
    location = StringField("Tapahtuman sijainti", [validators.Length(min=4)], render_kw={"class": "form-control"})
    time = TimeField("Kellonaika", format='%H:%M', render_kw={"class": "form-control"})
    date = DateField("Päivämäärä", format='%Y-%m-%d', render_kw={"class": "form-control"})
    attendee_max = IntegerField("Maksimi osallistujamäärä (valinnainen)", render_kw={"class": "form-control"})
    attendee_min = IntegerField("Minimi osallistujamäärä, jotta tapahtuma järjestetään (valinnainen", render_kw={"class": "form-control"})

    class Meta:
        csrf = False

class EventModifyForm(FlaskForm):
    name = StringField("Tapahtuman nimi", [validators.Length(min=4)], render_kw={"class": "form-control"})
    location = StringField("Tapahtuman sijainti", [validators.Length(min=4)], render_kw={"class": "form-control"})
    time = TimeField("Kellonaika", format='%H:%M', render_kw={"class": "form-control"})
    date = DateField("Päivämäärä", format='%Y-%m-%d', render_kw={"class": "form-control"})
    attendee_max = IntegerField("Maksimi osallistujamäärä (valinnainen)", render_kw={"class": "form-control"})
    attendee_min = IntegerField("Minimi osallistujamäärä, jotta tapahtuma järjestetään (valinnainen", render_kw={"class": "form-control"})

    class Meta:
        csrf = False