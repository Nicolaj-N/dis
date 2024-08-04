# write all your SQL queries in this file.
from insurance import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql


@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    schema = 'customers'
    id = 'cpr_number'
    if str(user_id).startswith('60'):
        schema = 'employees'
        id = 'id'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        # return-if svarer til nedenstående:
    		# if schema == 'employees':
    		#   return Employees(cur.fetchone())
    		# else:
    		#   return Customers(cur.fetchone())

        return Employees(cur.fetchone()) if schema == 'employees' else Customers(cur.fetchone())
    else:
        return None



class Customers(tuple, UserMixin):
    def __init__(self, user_data):
        self.CPR_number = user_data[0]
        self.name = user_data[1]
        self.password = user_data[2]
        self.address = user_data[3]
        self.role = "customer"

    def get_id(self):
       return (self.CPR_number)


class Employees(tuple, UserMixin):
    def __init__(self, employee_data):
        self.id = employee_data[0]
        self.name = employee_data[1]
        self.password = employee_data[2]
        self.role = "employee"

    def get_id(self):
       return (self.id)

class Policies(tuple):
    def __init__(self, policy_data):
        self.policy_id = policy_data[0]
        self.policy_type = policy_data[1]
        self.start_date = policy_data[2]
        self.end_date = policy_data[3]
        self.premium = policy_data[4]
        self.cover_amount = policy_data[5]
        self.excess = policy_data[6]

class PolicyTemplate(tuple):
    def __init__(self, policy_data):
        self.id = policy_data[0]
        self.policy_type = policy_data[1]
        self.premium = policy_data[2]
        self.cover_amount = policy_data[3]
        self.excess = policy_data[4]

def insert_customers(name, CPR_number, password):
    cur = conn.cursor()
    sql = """
    INSERT INTO customers(name, CPR_number, password)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (name, CPR_number, password))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_customer(CPR_number):
    cur = conn.cursor()
    sql = """
    SELECT * FROM customers
    WHERE CPR_number = %s
    """
    cur.execute(sql, (CPR_number,))
    user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

#cus-1-3-2024
def select_customer_direct(CPR_number):
    #SELECT cpr_number, name, address FROM Customers
    cur = conn.cursor()
    sql = """
    SELECT *
     FROM customers
    WHERE CPR_number = %s
    AND DIRECT IS TRUE
    """
    cur.execute(sql, (CPR_number,))
    user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_employee(id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM employees
    WHERE id = %s
    """
    cur.execute(sql, (id,))
    user = Employees(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_all_policies():
    cur = conn.cursor()
    sql = """
    SELECT * FROM policy_templates
    """
    cur.execute(sql)
    policies = [PolicyTemplate(row) for row in cur.fetchall()]
    cur.close()
    return policies

def select_policy(policy_id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM policy_templates WHERE id = %s
    """
    cur.execute(sql, (policy_id,))
    policy = PolicyTemplate(cur.fetchone()) if cur.rowcount > 0 else None
    cur.close()
    return policy

def add_policy_to_customer(customer_id, policy_id):
    policy = select_policy(policy_id)
    if policy is None:
        raise Exception(f"Policy with id {policy_id} not found")
    
    cur = conn.cursor()
    sql = """
    INSERT INTO policies (policy_type, start_date, end_date, premium, cover_amount, excess)
    VALUES (%s, current_date::timestamp, current_date::timestamp + interval '1 year', %s, %s, %s)
    RETURNING (policy_id)
    """
    cur.execute(sql, (policy.policy_type, policy.premium, policy.cover_amount, policy.excess))
    new_policy_id = cur.fetchone()

    if new_policy_id is None:
        raise Exception(f"Policy could not be created, please try again")
    
    sql = """
    INSERT INTO customer_policies (CPR_number, policy_id)
    VALUES (%s, %s)
    """
    cur.execute(sql, (customer_id, new_policy_id))
    conn.commit()
    cur.close()

def get_customer_active_policies(customer_id):
    cur = conn.cursor()
    sql = """
    SELECT 
        p.policy_id, 
        p.policy_type, 
        p.start_date, 
        p.end_date, 
        p.premium
    FROM 
        customer_policies cp
    JOIN 
        policies p ON cp.policy_id = p.policy_id
    WHERE 
        cp.CPR_number = %s
        AND p.start_date <= CURRENT_TIMESTAMP
        AND p.end_date >= CURRENT_TIMESTAMP;
    """
    cur.execute(sql, (customer_id,))
    active_policies = cur.fetchall()
    cur.close()
    return active_policies

def get_customer_expired_policies(customer_id):
    cur = conn.cursor()
    sql = """
    SELECT 
        p.policy_id, 
        p.policy_type, 
        p.start_date, 
        p.end_date, 
        p.premium
    FROM 
        customer_policies cp
    JOIN 
        Policies p ON cp.policy_id = p.policy_id
    WHERE 
        cp.CPR_number = %s
        AND p.end_date < CURRENT_TIMESTAMP;
    """
    cur.execute(sql, (customer_id,))
    expired_policies = cur.fetchall()
    cur.close()
    return expired_policies

def remove_db_policy(policy_id):
    cur = conn.cursor()
    sql = """
    UPDATE policies
    SET end_date = CURRENT_TIMESTAMP
    WHERE policy_id = %s;
    """
    cur.execute(sql, (policy_id,))
    conn.commit()
    cur.close()


def customer_has_active_policy_type(customer_id, template_policy_id):
    cur = conn.cursor()
    sql = """
    SELECT 1
    FROM customer_policies cp
    JOIN policies p ON cp.policy_id = p.policy_id
    WHERE cp.CPR_number = %s 
        AND p.policy_type in
            (SELECT policy_type FROM policy_templates WHERE id = %s) 
        AND p.end_date > CURRENT_TIMESTAMP
    LIMIT 1;
    """
    cur.execute(sql, (customer_id, template_policy_id))
    exists = cur.fetchone() is not None
    cur.close()
    return exists

def customer_has_active_policy(customer_id, policy_id):
    cur = conn.cursor()
    sql = """
    SELECT 1
    FROM customer_policies cp
    JOIN policies p ON cp.policy_id = p.policy_id
    WHERE cp.CPR_number = %s AND cp.policy_id = %s AND p.end_date > CURRENT_TIMESTAMP
    LIMIT 1;
    """
    cur.execute(sql, (customer_id, policy_id))
    exists = cur.fetchone() is not None
    cur.close()
    return exists



def customer_has_active_claim(customer_id, claim_id):
    cur = conn.cursor()
    sql = """
    SELECT 1
    FROM customer_policies cp
        JOIN policies p ON cp.policy_id = p.policy_id
        JOIN claims c ON p.policy_id = c.policy_id
    WHERE cp.CPR_number = %s AND c.claim_id = %s AND c.status = 'pending'
    LIMIT 1;
    """
    cur.execute(sql, (customer_id, claim_id))
    exists = cur.fetchone() is not None
    cur.close()
    return exists

def close_db_claim(claim_id):
    cur = conn.cursor()
    sql = """
    UPDATE claims
    SET status = 'closed'
    WHERE claim_id = %s;
    """
    cur.execute(sql, (claim_id,))
    conn.commit()
    cur.close()


def get_customer_active_claims(customer_id):
    cur = conn.cursor()
    sql = """
    SELECT 
        c.claim_id,
        c.policy_id,
        c.claim_date,
        c.claim_amount,
        c.status,
        c.description
    FROM customer_policies cp
        JOIN policies p ON cp.policy_id = p.policy_id
        JOIN claims c ON p.policy_id = c.policy_id
    WHERE 
        cp.CPR_number = %s
        AND status = 'pending';
    """
    cur.execute(sql, (customer_id,))
    active_claims = cur.fetchall()
    cur.close()
    return active_claims


def get_customer_resolved_claims(customer_id):
    cur = conn.cursor()
    sql = """
    SELECT 
        c.claim_id, 
        c.policy_id, 
        c.claim_date, 
        c.claim_amount, 
        c.status,
        c.description
    FROM customer_policies cp
        JOIN policies p ON cp.policy_id = p.policy_id
        JOIN claims c ON p.policy_id = c.policy_id
    WHERE 
        cp.CPR_number = %s
        AND status != 'pending';
    """
    cur.execute(sql, (customer_id,))
    active_claims = cur.fetchall()
    cur.close()
    return active_claims

def add_claim_to_customer(policy_id, claim_amount, description):
    cur = conn.cursor()
    sql = """
    INSERT INTO claims (policy_id, claim_date, claim_amount, status, description)
    VALUES (%s, CURRENT_TIMESTAMP, %s, 'pending', %s)
    """
    cur.execute(sql, (policy_id, claim_amount, description))
    conn.commit()
    cur.close()