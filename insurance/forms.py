from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, IntegerField, DecimalField,  RadioField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

# class AddCustomerForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#     CPR_number = IntegerField('CPR_number',
#                         validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Add')

class CustomerLoginForm(FlaskForm):
    id = IntegerField('CPR_number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EmployeeLoginForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SelectPolicyForm(FlaskForm):
    policy = RadioField('Policy', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Select Policy')

class MakeClaimForm(FlaskForm):
    claim_amount = DecimalField('Claim Amount', validators=[DataRequired(), NumberRange(min=0)], places=2)
    description = TextAreaField('Claim Description', validators=[DataRequired(), Length(max=500)])

class AddPolicyForm(FlaskForm):
    policy_type = StringField('Policy Type', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    premium = DecimalField('Premium', validators=[DataRequired(), NumberRange(min=0)])
    cover_amount = DecimalField('Cover Amount', validators=[DataRequired(), NumberRange(min=0)])
    excess = DecimalField('Excess', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Policy')

class UpdatePolicyForm(FlaskForm):
    policy_type = StringField('Policy Type', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    premium = DecimalField('Premium', validators=[DataRequired(), NumberRange(min=0)])
    cover_amount = DecimalField('Cover Amount', validators=[DataRequired(), NumberRange(min=0)])
    excess = DecimalField('Excess', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Policy')
