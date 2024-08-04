from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#from flask import session
#from flask_session import Session


app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

# set your own database
#db = "dbname='bank' user='postgres' host='127.0.0.1' password = 'UIS'"
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Check Configuration section for more details
#SESSION_TYPE = 'filesystem'


roles = ["none","employee","customer"]
print(roles)
# mysession = {"state" : "initializing","role" : "none", "id": 0}
# mysession = {"state" : "initializing","role" : "customer", "id": 5005}
mysession = {"state" : "initializing","role" : "employee", "id": 6003 ,"age" : 202212}
print(mysession)

from insurance.Login.routes import Login
from insurance.Customer.routes import Customer
from insurance.Employee.routes import Employee
app.register_blueprint(Login)
app.register_blueprint(Customer)
app.register_blueprint(Employee)
