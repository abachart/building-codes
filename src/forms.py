from click import confirm
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from app import app, db
from models import BuildingCode, Item, Location


##### FORMS #####
# For creating a new building code
class CreateCodeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    submit_create_code = SubmitField('Add')

# For creating a new location
class CreateLocationForm(FlaskForm):
    state = SelectField('State', choices=[('N/A', 'Other'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])
    city = StringField('City', validators=[DataRequired()])
    submit_create_location = SubmitField('Add')
    
# For adding a code to a location
class AddItemForm(FlaskForm):
    item_select = SelectField(u'Add Code', coerce=int)
    submit_add_item = SubmitField('Add')

# For selecting a location to be deleted from the database
class SelectDeleteForm(FlaskForm):
    select = SelectField(u'Delete', coerce=int)
    confirm_delete = BooleanField('Confirm Delete', validators=[DataRequired()])
    submit_delete = SubmitField('Delete')
