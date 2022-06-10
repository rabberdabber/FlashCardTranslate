from tokenize import String
from wtforms import SelectField,SubmitField,StringField,IntegerField
from wtforms.validators import DataRequired,ValidationError,InputRequired
from flask_wtf import FlaskForm

#fetch the available languages from the API instead of a list
codes = ['en','es','fr','de','it','zh-CN','ja','ko','in','ru','th','vi','zh-TW']
languages = ['English','Spanish','French','German','Italian','Simplified Chinese','Japanese','Korean','Indonesian','Russian','Vietnamese','Thai','Traditional Chinese']
choices = list(zip(codes,languages))
language_dict = dict(choices)

def is_equal_to(form,field):
    if field.data == form.target.data:
        raise ValidationError('Source and target languages must be different')
    
        
class LanguageForm(FlaskForm):
    source = SelectField('source',choices=choices,validators=[InputRequired(),is_equal_to])
    target = SelectField('target',choices=choices,validators=[InputRequired()])
    add = SubmitField('Add')
    search = SubmitField('Link')
    delete = SubmitField('Delete')
    
class WordForm(FlaskForm):
    text = StringField('text',validators=[InputRequired()])
    add = SubmitField('Add')
    search = SubmitField('Search')
    
class ApiForm(FlaskForm):
    method = SelectField('method',choices=['GET','POST','DELETE'],validators=[InputRequired()])
    resource = SelectField('resource',choices=['categories','cards','card from category','category','card'],validators=[InputRequired()])
    category_id = IntegerField('category_id',default=0)
    card_id = IntegerField('card_id',default=0)
    word = StringField('word')
    source = StringField('source')
    target = StringField('target')
    submit = SubmitField('submit')
    
    