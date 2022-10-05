from random import choices
from flask import render_template, request, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from forms import LoginForm, RegistrationForm, AddCodeForm, CreateProjectForm, DeleteForm, CreateCodeForm, CreateLocationForm, DeleteCodeForm, DeleteAccountForm
from models import User, UserProjects, UserLocations, Project, Location, ProjectCodes, LocationCodes, Code
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

##### HOME #####
@app.route('/')
def home():
    return render_template('home.html', cur_page='home')

##### PROJECTS_HOME #####
@app.route('/projects')
@login_required
def projects():
    # get users projects
    user_projects = UserProjects.query.filter_by(user_id=current_user.id).all()
    # get projects
    cur_projects = Project.query.filter(Project.id.in_([project.project_id for project in user_projects])).all()
    return render_template('projects_home.html', cur_page='projects', projects=cur_projects)

##### PROJECT/ID #####
@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project(project_id):
    # get codes for project
    all_codes = Code.query.all()
    cur_project = Project.query.filter_by(id=project_id).first_or_404()
    project_codes = ProjectCodes.query.filter_by(project_id=project_id).all()
    # set up form
    add_form = AddCodeForm()
    choices = []
    for code in all_codes:
        if(code.id not in [project_code.code_id for project_code in project_codes]):
            choices.append((code.id, f'{code.name}, {code.year}'))
    add_form.select.choices = choices
    # add codes to form
    if request.method == 'POST':
        if add_form.validate_on_submit():
            code_id = add_form.select.data
            project_code = ProjectCodes(code_id=code_id, project_id=project_id)
            db.session.add(project_code)
            db.session.commit()
            return redirect(url_for('project', project_id=project_id))
    return render_template('project.html', cur_page='project', project=cur_project, codes=project_codes, add_form=add_form)

@app.route('/project/delete/<int:project_id>/<int:code_id>')
@login_required
def delete_code_from_project(code_id, project_id):
    project_code = ProjectCodes.query.filter_by(code_id=code_id, project_id=project_id).first_or_404()
    db.session.delete(project_code)
    db.session.commit()
    return redirect(url_for('project', project_id=project_id))
    
##### EDIT_PROJECTS #####
@app.route('/edit-projects', methods=['GET', 'POST'])
@login_required
def edit_projects():
    # get user projects
    user_projects = UserProjects.query.filter_by(user_id=current_user.id).all()
    # set up forms
    create_form = CreateProjectForm()
    delete_form = DeleteForm()
    # delete_form choices
    choices = []
    for project in user_projects:
        choices.append((project.project_id, Project.query.filter_by(id=project.project_id).first().name))
    delete_form.select.choices = choices
    # Create Project or Delete Project
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            if not current_user.check_password(delete_form.password.data):
                flash('Invalid Password')
                return redirect(url_for('edit_projects'))
            del_project = Project.query.filter_by(id=delete_form.select.data).first()
            del_user_project = UserProjects.query.filter_by(project_id=del_project.id).first()
            del_project_codes = ProjectCodes.query.filter_by(project_id=del_project.id).all()
            for del_project_code in del_project_codes:
                db.session.delete(del_project_code)
            db.session.delete(del_user_project)
            db.session.delete(del_project)
            db.session.commit()
            return redirect(url_for('edit_projects'))
        if create_form.validate_on_submit():
            new_project = Project(name=create_form.name.data)
            db.session.add(new_project)
            db.session.commit()
            user_project = UserProjects(user_id=current_user.id, project_id=new_project.id)
            db.session.add(user_project)
            db.session.commit()
            return redirect(url_for('edit_projects'))
    return render_template('edit_projects.html', cur_page='edit-projects', create_form=create_form, delete_form=delete_form)

    
##### LOCATIONS_HOME #####
@app.route('/locations')
@login_required
def locations():
    # get users locations
    user_locations = UserLocations.query.filter_by(user_id=current_user.id).all()
    # get locations
    cur_locations = Location.query.filter(Location.id.in_([location.location_id for location in user_locations])).all()
    return render_template('locations_home.html', cur_page='locations', locations=cur_locations)

##### LOCATION/ID #####
@app.route('/location/<int:location_id>', methods=['GET', 'POST'])
@login_required
def location(location_id):
    # get codes for location
    all_codes = Code.query.all()
    cur_location = Location.query.filter_by(id=location_id).first_or_404()
    location_codes = LocationCodes.query.filter_by(location_id=location_id).all()
    # set up form
    add_form = AddCodeForm()
    choices = []
    for code in all_codes:
        if(code.id not in [location_code.code_id for location_code in location_codes]):
            choices.append((code.id, f'{code.name}, {code.year}'))
    add_form.select.choices = choices
    # add codes to form
    if request.method == 'POST':
        if add_form.validate_on_submit():
            code_id = add_form.select.data
            location_code = LocationCodes(code_id=code_id, location_id=location_id)
            db.session.add(location_code)
            db.session.commit()
            return redirect(url_for('location', location_id=location_id))
    return render_template('location.html', cur_page='location', location=cur_location, codes=location_codes, add_form=add_form)

@app.route('/location/delete/<int:location_id>/<int:code_id>')
@login_required
def delete_code_from_location(code_id, location_id):
    location_code = LocationCodes.query.filter_by(code_id=code_id, location_id=location_id).first_or_404()
    db.session.delete(location_code)
    db.session.commit()
    return redirect(url_for('location', location_id=location_id))

##### EDIT_LOCATIONS #####
@app.route('/edit-locations', methods=['GET', 'POST'])
@login_required
def edit_locations():
    # get user locations
    user_locations = UserLocations.query.filter_by(user_id=current_user.id).all()
    # set up forms
    create_form = CreateLocationForm()
    delete_form = DeleteForm()
    # delete_form choices
    choices = []
    for location in user_locations:
        choices.append((location.location_id, f'{Location.query.filter_by(id=location.location_id).first().city}, {Location.query.filter_by(id=location.location_id).first().state}'))
    delete_form.select.choices = choices
    # Create Location or Delete Location
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            if not current_user.check_password(delete_form.password.data):
                flash('Invalid Password')
                return redirect(url_for('edit_locations'))
            del_location = Location.query.filter_by(id=delete_form.select.data).first()
            del_user_location = UserLocations.query.filter_by(location_id=del_location.id).first()
            del_location_codes = LocationCodes.query.filter_by(location_id=del_location.id).all()
            for del_location_code in del_location_codes:
                db.session.delete(del_location_code)
            db.session.delete(del_user_location)
            db.session.delete(del_location)
            db.session.commit()
            return redirect(url_for('edit_locations'))
        if create_form.validate_on_submit():
            new_location = Location(city=create_form.city.data, state=create_form.state.data)
            db.session.add(new_location)
            db.session.commit()
            user_location = UserLocations(user_id=current_user.id, location_id=new_location.id)
            db.session.add(user_location)
            db.session.commit()
            return redirect(url_for('edit_locations'))
    return render_template('edit_locations.html', cur_page='edit-locations', create_form=create_form, delete_form=delete_form)

##### EDIT_CODES #####
@app.route('/edit-codes', methods=['GET', 'POST'])
@login_required
def edit_codes():
    # set up forms
    create_form = CreateCodeForm()
    delete_form = DeleteCodeForm()
    # delete_form choices
    choices = []
    for code in Code.query.all():
        choices.append([code.id, f'{code.name}, {code.year}'])
    delete_form.select.choices = choices
    # post actions
    if request.method == 'POST':
        if delete_form.validate_on_submit():
            del_code = Code.query.filter_by(id=delete_form.select.data).first()
            del_code_locations = LocationCodes.query.filter_by(code_id=del_code.id).all()
            for del_code_location in del_code_locations:
                db.session.delete(del_code_location)
            del_code_projects = ProjectCodes.query.filter_by(code_id=del_code.id).all()
            for del_code_project in del_code_projects:
                db.session.delete(del_code_project)
            db.session.delete(del_code)
            db.session.commit()
            return redirect(url_for('edit_codes'))
        if create_form.validate_on_submit():
            new_code = Code(name=create_form.name.data, year=create_form.year.data, link=create_form.link.data)
            db.session.add(new_code)
            db.session.commit()
            return redirect(url_for('edit_codes'))            
    return render_template('edit_codes.html', cur_page='edit-codes', cur_user=current_user, create_form=create_form, delete_form=delete_form)

##### LOGIN #####
@app.route('/login', methods=['GET', 'POST'])
def login():
    # do nothing if already signed in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LoginForm()
    registration_form = RegistrationForm()
    if request.method == 'POST':
        # allow registration
        if registration_form.validate_on_submit():
            if User.query.filter_by(username=registration_form.username.data).first() is None:
                user = User(username=registration_form.username.data)
                user.set_password(registration_form.password.data)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Username already taken')
                return redirect(url_for('login'))
        # allow sign in
        if login_form.validate_on_submit():
            user = User.query.filter_by(username=login_form.username.data).first()
            if user is None or not user.check_password(login_form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('home'))
    return render_template('login.html', login_form=login_form, registration_form=registration_form, cur_page='login')
        
##### LOGOUT ##### 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

##### ACCOUNT #####
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # set up form
    delete_form = DeleteAccountForm()
    # post actions
    if request.method == 'POST':
        # delete method
        if delete_form.validate_on_submit():
            if not current_user.check_password(delete_form.password.data):
                flash('Invalid Password')
                return redirect(url_for('account'))
            # delete user
            # delete all associated locations and projects
            user_locations = UserLocations.query.filter_by(user_id=current_user.id).all()
            for user_location in user_locations:
                location = Location.query.filter_by(id=user_location.location_id).first()
                location_codes = LocationCodes.query.filter_by(location_id=location.id).all()
                for location_code in location_codes:
                    db.session.delete(location_code)
                db.session.delete(location)
                db.session.delete(user_location)
            user_projects = UserProjects.query.filter_by(user_id=current_user.id).all()
            for user_project in user_projects:
                project = Project.query.filter_by(id=user_project.project_id).first()
                project_codes = ProjectCodes.query.filter_by(project_id=project.id).all()
                for project_code in project_codes:
                    db.session.delete(project_code)
                db.session.delete(project)
                db.session.delete(user_project)
            # delete user
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            return redirect(url_for('home'))
    return render_template('account.html', delete_form=delete_form, cur_page='account')

##### OTHER ROUTES #####

### route for opening a link in a new tab
@app.route('/link/<int:code_id>')
def code_link(code_id):
    cur_code = Code.query.filter_by(id=code_id).first_or_404(description = 'Code not found')
    return redirect(cur_code.link)

### route for handling error 404
@app.errorhandler(404) 
def not_found(e): 
    return render_template('404.html')

### temp nuclear, delete all data
@app.route('/nuclear')
def nuclear():
    User.query.delete()
    UserProjects.query.delete()
    UserLocations.query.delete()
    Project.query.delete()
    Location.query.delete()
    ProjectCodes.query.delete()
    LocationCodes.query.delete()
    Code.query.delete()