from click import confirm
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app import app, db
from models import BuildingCode, Item, Location
from flask import render_template, request, url_for, redirect, flash

#form for adding a new building code
class CreateCodeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField('Add')

#form for adding a new location
class CreateLocationForm(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add')
    
#form to confirm deletion of code
class ConfirmDeleteForm(FlaskForm):
    code_select = SelectField(u'Delete', coerce=int)
    delete = SubmitField('Delete')

#form to add item to a location
class AddItemForm(FlaskForm):
    item_select = SelectField(u'Add Code', coerce=int)
    add = SubmitField('Add')

#form to create a new location
class CreateLocationForm(FlaskForm):
    state = SelectField('State', choices=[('N/A', 'Other'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add')

#form to delete a location
class DeleteLocationForm(FlaskForm):
    location_select = SelectField(u'Delete', coerce=int)
    delete = SubmitField('Delete')


#function to check if item is already tied to a location
def exists(item, location):
    for i in location:
        if i.code_id == item.code_id:
            return True
    return False

#page that shows list of all locations
@app.route('/locations')
def locations():
    cur_locations = Location.query.order_by(Location.state, Location.city)
    return render_template('locations_home.html', cur_locations=cur_locations, cur_page='location')

#page that shows all codes for a location #***
@app.route('/locations/<int:location_id>', methods = ['GET', 'POST'])
def location(location_id):
    add_form = AddItemForm()
    cur_location = Location.query.filter_by(id=location_id).first_or_404(description = 'Location not found')
    cur_codes = BuildingCode.query.all()
    cur_items = Item.query.filter_by(location_id=location_id).all()
    add_form.item_select.choices = [(code.id, f'{BuildingCode.query.get(code.id).name}, {BuildingCode.query.get(code.id).year}') for code in cur_codes]
    if request.method == 'POST':
        if add_form.validate_on_submit():
            code_id = add_form.item_select.data
            if(code_id not in [item.code_id for item in cur_items]):
                add_item(code_id, location_id)
            return redirect(url_for('location', location_id=location_id))
    return render_template('location.html', location=cur_location, codes=cur_codes, items=cur_items, add_form=add_form, cur_page='location')
def add_item(code_id, location_id):
    item = Item(code_id=code_id, location_id=location_id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('location', location_id=location_id))

#route that opens a codes link in a new tab
@app.route('/link/<int:code_id>')
def code_link(code_id):
    cur_code = BuildingCode.query.filter_by(id=code_id).first_or_404(description = 'Code not found')
    return redirect(cur_code.link)

#route that adds a code to a location
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

#route that deletes a code from a location
@app.route('/delete_item/<int:location_id>/<int:item_id>')
def delete_item_from_location(location_id, item_id):
    item = Item.query.filter_by(id = item_id).first_or_404(description = "No such item found.")
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('location', location_id=location_id))


#route for manage codes page
@app.route('/manage-codes', methods = ['GET', 'POST'])
def manage_codes():
    all_codes = BuildingCode.query.order_by('name')
    form = CreateCodeForm()
    delete_form = ConfirmDeleteForm()
    delete_form.code_select.choices = [(code.id, code.name) for code in all_codes]
    if request.method == 'POST':
        if form.validate_on_submit():
            new_code = BuildingCode(name = form.name.data, year = form.year.data, link = form.link.data)
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
    return render_template('manage_codes.html', form=form, delete_form=delete_form, codes=all_codes, cur_page='manage_codes')

def delete_code(code_id):
    code = BuildingCode.query.filter_by(id = code_id).first_or_404(description = "Error")
    matching_items = Item.query.filter_by(code_id = code_id).all()
    for i in matching_items:
        db.session.delete(i)
    db.session.delete(code)
    db.session.commit()
    return redirect(url_for('manage_codes'))

#manage locations page
@app.route('/manage-locations', methods = ['GET', 'POST'])
def manage_locations():
    all_locations = Location.query.order_by('city')
    create_form = CreateLocationForm()
    delete_form = DeleteLocationForm()
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


@app.route('/test')
def test():
    return render_template('test.html')
    