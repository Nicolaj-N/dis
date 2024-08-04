from flask import render_template, url_for, flash, redirect, request, Blueprint
from insurance import app, conn, bcrypt
from flask_login import current_user
from insurance.models import select_all_policies, add_policy_to_customer, get_customer_active_policies, get_customer_expired_policies, customer_has_active_policy, remove_db_policy, customer_has_active_policy_type, customer_has_active_claim, close_db_claim, get_customer_active_claims, get_customer_resolved_claims, add_claim_to_customer
from insurance.forms import SelectPolicyForm, MakeClaimForm

import datetime
from dateutil.relativedelta import relativedelta


#202212
# roles is defined in the init-file
from insurance import roles, mysession
iEmployee = 1
iCustomer = 2


Customer = Blueprint('Customer', __name__)

@Customer.route("/account", methods=['GET'])
def account():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing account details is customer only.', 'danger')
        return redirect(url_for('Login.login'))
    
    mysession["state"]="account"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)
    return render_template('account.html', title='Account', role=role)

@Customer.route("/add_policy", methods=['GET', 'POST'])
def add_policy():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Adding policies is customer only.','danger')
        return redirect(url_for('Login.login'))

    form = SelectPolicyForm()
    policies = select_all_policies()
    form.policy.choices = [(policy.id, f"{policy.policy_type} - ${policy.premium} - {str(datetime.date.today())} to {str(datetime.date.today() + relativedelta(years=1))}") for policy in policies]

    if form.validate_on_submit():
        policy_template_id = form.policy.data
        customer_id = current_user.get_id()

        if customer_has_active_policy_type(customer_id, policy_template_id):
            flash('You already have this policy.', 'danger')
        else:
            try:
                add_policy_to_customer(customer_id, policy_template_id)
                flash('Policy added successfully!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('Customer.active_policies'))

    mysession["state"]="add_policy"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)
    return render_template('add_policy.html', title='Add Policy', form=form, role=role)

@Customer.route("/active_policies", methods=['GET'])
def active_policies():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="active_policies"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)

    customer_id = current_user.get_id()
    active_policies = get_customer_active_policies(customer_id)

    return render_template('policies.html', title='Active Policies', policies=active_policies, active=True, role=role)


@Customer.route("/expired_policies", methods=['GET'])
def expired_policies():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()
    expired_policies = get_customer_expired_policies(customer_id)

    mysession["state"]="expired_policies"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)

    return render_template('policies.html', title='Expired Policies', policies=expired_policies, role=role)


@Customer.route("/active_claims", methods=['GET'])
def active_claims():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()
    active_claims = get_customer_active_claims(customer_id)

    mysession["state"]="active_claims"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)
    return render_template('claims.html', title='Active Claims', claims=active_claims, active=True, role=role)


@Customer.route("/resolved_claims", methods=['GET'])
def resolved_claims():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()
    resolved_claims = get_customer_resolved_claims(customer_id)

    mysession["state"]="resolved_claims"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)

    return render_template('claims.html', title='Resolved Claims', claims=resolved_claims, role=role)

@Customer.route("/customer/make_claim/<int:policy_id>", methods=['POST'])
def make_claim(policy_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))
    
    if policy_id is None:
        flash('No policy provided active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))
    
    customer_id = current_user.get_id()

    if not customer_has_active_policy(customer_id, policy_id):
        flash('Customer does not own the policy, or the policy has expired', 'danger')
        return redirect(url_for('Login.login'))
    
    form = MakeClaimForm()
    if form.validate_on_submit():
        claim_amount = form.claim_amount.data
        description = form.description.data

        try:
            add_claim_to_customer(policy_id, claim_amount, description)
            flash('Claim added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'An error occurred: {e}', 'danger')

        return redirect(url_for('Customer.active_claims'))
    
    mysession["state"]="make_claim"
    print(mysession)
    role =  mysession["role"]
    print('role: '+ role)

    return render_template('make_claim.html', title='Make Claim', policy_id=policy_id, form=form, role=role)

@Customer.route("/customer/close_claim/<int:claim_id>", methods=['POST'])
def close_claim(claim_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Closing claims is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()

    if not customer_has_active_claim(customer_id, claim_id):
        flash('Claim does not belong to the customer or has been resolved', 'danger')
        return redirect(url_for('Login.login'))

    try:
        close_db_claim(claim_id)
        flash('Claim closed successfully!', 'success')
    except Exception as e:
        conn.rollback()
        
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('Customer.active_claims'))


@Customer.route("/policy_payments", methods=['GET'])
def policy_payments():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()
    active_policies = get_customer_active_policies(customer_id)

    return render_template('policies.html', title='Active Policies', policies=active_policies)


@Customer.route("/claim_payouts", methods=['GET'])
def claim_payouts():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Viewing active policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()
    active_policies = get_customer_active_policies(customer_id)

    return render_template('policies.html', title='Active Policies', policies=active_policies)



@Customer.route("/customer/remove_policy/<int:policy_id>", methods=['POST'])
def remove_policy(policy_id):
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iCustomer]:
        flash('Removing policies is customer only.', 'danger')
        return redirect(url_for('Login.login'))

    customer_id = current_user.get_id()

    if not customer_has_active_policy(customer_id, policy_id):
        flash('Policy does not belong to the customer or has expired', 'danger')
        return redirect(url_for('Login.login'))

    try:
        remove_db_policy(policy_id)
        flash('Policy removed successfully!', 'success')
    except Exception as e:
        conn.rollback()
        
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('Customer.active_policies'))

