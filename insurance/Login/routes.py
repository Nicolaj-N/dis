from flask import render_template, url_for, flash, redirect, request, Blueprint
from insurance import app, conn, bcrypt
from insurance.forms import CustomerLoginForm, EmployeeLoginForm
from flask_login import login_user, current_user, logout_user, login_required
from insurance.models import select_employee
from insurance.models import Customers, select_customer
from insurance.models import get_customer_active_policies
from insurance import roles, mysession
import logging

iCustomer = 2

logging.basicConfig(level=logging.DEBUG)
Login = Blueprint('Login', __name__)

posts = [{}]


@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)

    policies = None

    if current_user.is_authenticated and role == roles[iCustomer]:
        policies = get_customer_active_policies(current_user.get_id())

    return render_template('home.html', role=role, policies=policies, active=True)

@Login.route("/login", methods=['GET', 'POST'])
def login():

    mysession["state"]="login"
    print(mysession)
    role=None

    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    is_employee = True if request.args.get('is_employee') == 'true' else False
    form = EmployeeLoginForm() if is_employee else CustomerLoginForm()

    # Først bekræft, at inputtet fra formen er gyldigt... 
    if form.validate_on_submit():

        #
        # her checkes noget som skulle være sessionsvariable, men som er en GET-parameter
        # implementeret af AL. Ideen er at teste på om det er et employee login
        # eller om det er et customer login.
        # betinget tildeling. Enten en employee - eller en customer instantieret
        # Skal muligvis laves om. Hvad hvis nu user ikke blir instantieret
        #
        user = select_employee(form.id.data) if is_employee else select_customer(form.id.data)

        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        
        if user != None and bcrypt.check_password_hash(user[2], form.password.data):

            print("role:" + user.role)
            if user.role == 'employee':
                mysession["role"] = roles[1] #employee
            elif user.role == 'customer':
                mysession["role"] = roles[2] #customer
            else:
                mysession["role"] = roles[0] #none

            mysession["id"] = form.id.data
            print(mysession)
            print(roles)

            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    return render_template('login.html', title='Login', is_employee=is_employee, form=form
    , role=role
    )
      

@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    mysession["role"]="none"
    return redirect(url_for('Login.home'))


@Login.route("/account")
@login_required
def account():
    mysession["state"]="account"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)

    accounts = []
    return render_template('account.html', title='Account'
    , acc=accounts, role=role
    )
