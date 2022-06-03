from tokenize import String
from wtforms import SelectField,SubmitField,StringField
from wtforms.validators import DataRequired,ValidationError,InputRequired
from flask_wtf import FlaskForm

codes = ['en','es','fr','de','it','zh-CN','ja','ko','in','ru','th','vi','zh-CHT']
languages = ['English','Spanish','French','German','Italian','Chinese','Japanese','Korean','Indonesian','Russian','Vietnamese','Thai','Chinese (Traditional)']
choices = list(zip(codes,languages))

def is_equal_to(form,field):
    if field.data == form.target.data:
        raise ValidationError('Source and target languages must be different')
    
        
class LanguageForm(FlaskForm):
    source = SelectField('srcLanguage',choices=choices,validators=[InputRequired(),is_equal_to])
    target = SelectField('targetLanguage',choices=choices,validators=[InputRequired()])
    add = SubmitField('Add')
    search = SubmitField('Search')
    delete = SubmitField('Delete')
    