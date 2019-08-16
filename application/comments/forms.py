from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class CommentForm(FlaskForm):
    content = StringField("", [validators.Length(min=1)], render_kw={"class": "form-control", "placeholder": "kirjoita kommentti"})
    
    class Meta:
        csrf = False