from click import confirm
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app import app, db
from models import BuildingCode, Item, Location
from flask import render_template, request, url_for, redirect, flash

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
    
# For selecting a code to be deleted from the database
class SelectCodeDeleteForm(FlaskForm):
    code_select = SelectField(u'Delete', coerce=int)
    submit_delete_code = SubmitField('Delete')

# For selecting a location to be deleted from the database
class SelectLocationDeleteForm(FlaskForm):
    location_select = SelectField(u'Delete', coerce=int)
    submit_delete_location = SubmitField('Delete')
    
##### GENERAL FUNCTIONS #####
# For checking if a building code is already tied to a location
def exists(item, location):
    for i in location:
        if i.code_id == item.code_id:
            return True
    return False

##### ROUTES #####

### LOCATION_HOME ###
# This is the page that will display the entire list of locations

# Main route
@app.route('/locations')
def locations():
    cur_locations = Location.query.order_by(Location.state, Location.city)
    return render_template('locations_home.html', cur_locations=cur_locations, cur_page='location')



### LOCATION/ID ###
# This is the page that will display the codes for a specific location and allow users to add codes to this location

# Main route
@app.route('/locations/<int:location_id>', methods = ['GET', 'POST'])
def location(location_id):
    # forms
    add_form = AddItemForm()
    
    # get the location, all the codes, and all the items tied to the location
    cur_location = Location.query.filter_by(id=location_id).first_or_404(description = 'Location not found')
    cur_codes = BuildingCode.query.all()
    cur_items = Item.query.filter_by(location_id=location_id).all()
    
    # add items to the form
    add_form.item_select.choices = [(code.id, f'{BuildingCode.query.get(code.id).name}, {BuildingCode.query.get(code.id).year}') for code in cur_codes]
    
    # if the form is submitted, tie the code to the location by creating an item
    if request.method == 'POST':
        if add_form.validate_on_submit():
            code_id = add_form.item_select.data
            if(code_id not in [item.code_id for item in cur_items]):
                item = Item(code_id=code_id, location_id=location_id)
                db.session.add(item)
                db.session.commit()
            return redirect(url_for('location', location_id=location_id))
    return render_template('location.html', location=cur_location, codes=cur_codes, items=cur_items, add_form=add_form, cur_page='location')

# This route opens a codes link in a new tab
@app.route('/link/<int:code_id>')
def code_link(code_id):
    cur_code = BuildingCode.query.filter_by(id=code_id).first_or_404(description = 'Code not found')
    return redirect(cur_code.link)

# This route adds a code to a location
@app.route('/add_item/<int:location_id>/<int:code_id>')
def add_item_to_location(location_id, code_id):
    new_item = Item(code_id = code_id, location_id = location_id)
    location = Location.query.filter_by(id = location_id).first_or_404(description = "No such location found.")
    if not exists(new_item, location.codes):
        #using db session add the new item
        db.session.add(new_item)
        #commit the database changes here
        db.session.commit()
    # redirect to location add code page
    return redirect(url_for('add_item_page', location_id=location_id))

# This route removes a selected code from a location
@app.route('/delete_item/<int:location_id>/<int:item_id>')
def delete_item_from_location(location_id, item_id):
    item = Item.query.filter_by(id = item_id).first_or_404(description = "No such item found.")
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('location', location_id=location_id))


### MANAGE_CODES ###
# This is the page that will allow the user to add or delete a code

# Main route
@app.route('/manage-codes', methods = ['GET', 'POST'])
def manage_codes():
    all_codes = BuildingCode.query.order_by('name')
    create_form = CreateCodeForm()
    delete_form = SelectCodeDeleteForm()
    delete_form.code_select.choices = [(code.id, code.name) for code in all_codes]
    if request.method == 'POST':
        if create_form.validate_on_submit():
            new_code = BuildingCode(name = create_form.name.data, year = create_form.year.data, link = create_form.link.data)
            db.session.add(new_code)
            db.session.commit()
            flash('New code added!')
            return redirect(url_for('manage_codes'))
        if delete_form.validate_on_submit():##***
            code_id = delete_form.code_select.data
            code = BuildingCode.query.filter_by(id = code_id).first_or_404(description = "No such code found.")
            db.session.delete(code)
            db.session.commit()
            flash('Code deleted!')
            return redirect(url_for('manage_codes'))
    else:
        flash('All fields are required.')
    return render_template('manage_codes.html', create_form=create_form, delete_form=delete_form, codes=all_codes, cur_page='manage_codes')

# This route deletes a code and removes any item ties it has to locations
def delete_code(code_id):
    code = BuildingCode.query.filter_by(id = code_id).first_or_404(description = "Error")
    matching_items = Item.query.filter_by(code_id = code_id).all()
    for i in matching_items:
        db.session.delete(i)
    db.session.delete(code)
    db.session.commit()
    return redirect(url_for('manage_codes'))

### MANAGE_LOCATION ###
# This is the page that will allow the user to add or delete a location

# Main route
#manage locations page
@app.route('/manage-locations', methods = ['GET', 'POST'])
def manage_locations():
    all_locations = Location.query.order_by('city')
    create_form = CreateLocationForm()
    delete_form = SelectLocationDeleteForm()
    delete_form.location_select.choices = [(location.id, location.city) for location in all_locations]
    if request.method == 'POST':
        if create_form.validate_on_submit():
            new_location = Location(state = create_form.state.data, city = create_form.city.data)
            db.session.add(new_location)
            db.session.commit()
            flash('New location added!')
            return redirect(url_for('manage_locations'))
        if delete_form.validate_on_submit():
            location_id = delete_form.location_select.data
            location = Location.query.filter_by(id = location_id).first_or_404(description = "Error")
            matching_items = Item.query.filter_by(location_id = location_id).all()
            for i in matching_items:
                db.session.delete(i)
            db.session.delete(location)
            db.session.commit()
            flash('Location deleted!')
            return redirect(url_for('manage_locations'))
    return render_template('manage_locations.html', create_form=create_form, delete_form=delete_form, locations=all_locations, cur_page='manage_locations')