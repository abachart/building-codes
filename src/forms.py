from unicodedata import numeric
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, NumberRange
from src.models import User, UserProjects, UserLocations, Project, Location, ProjectCodes, LocationCodes, Code

# LoginForm class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# RegistrationForm class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
# AddCodeForm class
# adds a code to either a project or a location
class AddCodeForm(FlaskForm):
    select = SelectField(u'Add Code', coerce=int)
    submit = SubmitField('Add Code')
    
# CreateProjectForm class
class CreateProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Project')

# CreateLocationForm class
class CreateLocationForm(FlaskForm):
    state = SelectField('State', choices=[('N/A', 'Other'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add Location')

# DeleteForm class
# deletes a project or a location
class DeleteForm(FlaskForm):
    select = SelectField(u'Delete', coerce=int)
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Delete')
    
# CreateCodeForm class
class CreateCodeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1000, max=9999)])
    link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField('Add Code')

# DeleteCodeForm class
class DeleteCodeForm(FlaskForm):
    select = SelectField(u'Delete', coerce=int)
    confirm = BooleanField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Delete')
    
# DeleteAccountForm class
class DeleteAccountForm(FlaskForm):
    password = PasswordField('Please Enter your Password to Delete:', validators=[DataRequired()])
    submit = SubmitField('Delete')