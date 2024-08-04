from flask import render_template, url_for, flash, redirect, request, Blueprint
from insurance import app, conn, bcrypt
from flask_login import current_user
from insurance.models_e import select_emp_cus_accounts, get_all_claims, update_claim_status, get_claims_for_managed_customers

#202212
from insurance import roles, mysession


iEmployee = 1
iCustomer = 2 # bruges til transfer/

Employee = Blueprint('Employee', __name__)


# @Employee.route("/add_customer", methods=['GET', 'POST'])
# def add_customer():

#     if not current_user.is_authenticated:
#         return redirect(url_for('Login.home'))

#     #202212
#     # employee only
#     if not mysession["role"] == roles[iEmployee]:
#         flash('Adding customers is employee only.','danger')
#         return redirect(url_for('Login.login'))

#     form = AddCustomerForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         name=form.username.data
#         CPR_number=form.CPR_number.data
#         password=hashed_password
#         insert_customers(name, CPR_number, password)
#         flash('Account has been created! The customer is now able to log in', 'success')
#         return redirect(url_for('Login.home'))
#     return render_template('add_customer.html', title='Add Customer', form=form)

@Employee.route("/account", methods=['GET'])
def account():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]:
        flash('Viewing account details is employee only.', 'danger')
        return redirect(url_for('Login.login'))
    
    mysession["state"]="account"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)
    return render_template('account.html', title='Account', role=role)

@Employee.route("/manage_customers", methods=['GET', 'POST'])
def manage_customers():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]:
        flash('Managing customers is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    mysession["state"] = "manage_customers"
    print(mysession)
    role = mysession["role"]
    print('role: ' + role)
    employee_id = current_user.get_id()
    print(employee_id)

    managed_customers = select_emp_cus_accounts(employee_id)
    print(managed_customers)

    return render_template('manage_customers.html', title='Manage Customers', customers=managed_customers, role=role)

@Employee.route("/review_claims", methods=['GET'])
def review_claims():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]:
        flash('Reviewing claims is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    mysession["state"] = "review_claims"
    print(mysession)
    role = mysession["role"]
    print('role: ' + role)

    employee_id = current_user.get_id()
    pending_claims, resolved_claims = get_claims_for_managed_customers(employee_id)
    print(pending_claims, resolved_claims)

    return render_template('review_claims.html', title='Review Claims', pending_claims=pending_claims, resolved_claims=resolved_claims, role=role)


@Employee.route("/update_claim_status/<int:claim_id>", methods=['POST'])
def update_claim_status_route(claim_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]:
        flash('Updating claims is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    action = request.form.get('action')
    if action not in ['approve', 'reject']:
        flash('Invalid action.', 'danger')
        return redirect(url_for('Employee.review_claims'))

    status = 'approved' if action == 'approve' else 'rejected'
    try:
        update_claim_status(claim_id, status)
        flash(f'Claim {claim_id} has been {status}.', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('Employee.review_claims'))



