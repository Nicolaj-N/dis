from flask import render_template, url_for, flash, redirect, request, Blueprint
from insurance import app, conn, bcrypt
from flask_login import current_user
from insurance.models_e import select_emp_cus_accounts, update_claim_status, get_claims_for_managed_customers
from insurance.models_e import get_all_policies, get_policy_by_id, add_policy, update_policy, delete_policy
from insurance.forms import AddPolicyForm, UpdatePolicyForm
import datetime
from dateutil.relativedelta import relativedelta

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


@Employee.route("/manage_policies", methods=['GET'])
def manage_policies():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]: 
        flash('Managing policies is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    mysession["state"] = "manage_policies"
    print(mysession)
    role = mysession["role"]
    print('role: ' + role)

    policies = get_all_policies()
    return render_template('manage_policies.html', title='Manage Policies', policies=policies, role=role)

@Employee.route("/emp_add_policy", methods=['GET', 'POST'])
def add_policy_route():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]: 
        flash('Adding policies is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    form = AddPolicyForm()
    if form.validate_on_submit():
        try:
            add_policy(form.policy_type.data, form.start_date.data, form.end_date.data, form.premium.data, form.cover_amount.data, form.excess.data)
            flash('Policy added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('Employee.manage_policies'))
    return render_template('emp_add_policy.html', title='Add Policy', form=form)

@Employee.route("/update_policy/<int:policy_id>", methods=['GET', 'POST'])
def update_policy(policy_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))
    
    print(f"Route hit for updating policy: {policy_id}")


    if not mysession["role"] == roles[iEmployee]:
        flash('Updating policies is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    policy = get_policy_by_id(policy_id)
    if not policy:
        flash('Policy not found.', 'danger')
        return redirect(url_for('Employee.manage_policies'))
    
    mysession["state"] = "update_policy"
    role = mysession["role"]

    form = UpdatePolicyForm()
    if form.validate_on_submit():
            print("Form validated")
            try:
                print(f"Updating policy: {policy_id}")
                print(f"Start Date: {form.start_date.data}")
                print(f"End Date: {form.end_date.data}")
                print(f"Premium: {form.premium.data}")
                print(f"Cover Amount: {form.cover_amount.data}")
                print(f"Excess: {form.excess.data}")
                update_policy(policy_id, form.start_date.data, form.end_date.data, form.premium.data, form.cover_amount.data, form.excess.data)
                flash('Policy updated successfully!', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('Employee.manage_policies'))
    else:
        form.start_date.data = policy['start_date']
        form.end_date.data = policy['end_date']
        form.premium.data = policy['premium']
        form.cover_amount.data = policy['cover_amount']
        form.excess.data = policy['excess']
    return render_template('update_policy.html', title='Update Policy', form=form, policy=policy, role=role)

@Employee.route("/delete_policy/<int:policy_id>", methods=['POST'])
def delete_policy_route(policy_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]: 
        flash('Deleting policies is employee only.', 'danger')
        return redirect(url_for('Login.login'))

    try:
        delete_policy(policy_id)
        flash('Policy deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('Employee.manage_policies'))




