# write all your SQL queries in this file.
from datetime import datetime
from insurance import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql, extras
from insurance.models import PolicyTemplate






def select_emp_cus_accounts(emp_cpr_number):
    cur = conn.cursor()
    sql = """
    SELECT c.CPR_number, c.name, c.address
    FROM manages m
    JOIN customers c ON m.CPR_number = c.CPR_number
    WHERE m.emp_cpr_number = %s;
    """
    cur.execute(sql, (emp_cpr_number,))
    customers = cur.fetchall()
    cur.close()
    return customers

def get_all_claims():
    cur = conn.cursor()
    sql = """
    SELECT cl.claim_id, cl.policy_id, c.CPR_number, c.name, cl.claim_date, cl.claim_amount, cl.status, cl.description
    FROM claims cl
    JOIN policies p ON cl.policy_id = p.policy_id
    JOIN customer_policies cp ON cp.policy_id = p.policy_id
    JOIN customers c ON cp.CPR_number = c.CPR_number
    ORDER BY cl.claim_date DESC;
    """
    cur.execute(sql)
    claims = cur.fetchall()
    cur.close()
    return claims

def get_claims_for_managed_customers(employee_id):
    cur = conn.cursor()
    sql = """
    SELECT cl.claim_id, cl.policy_id, c.CPR_number, c.name, cl.claim_date, cl.claim_amount, cl.status, cl.description
    FROM claims cl
    JOIN policies p ON cl.policy_id = p.policy_id
    JOIN customer_policies cp ON cp.policy_id = p.policy_id
    JOIN customers c ON cp.CPR_number = c.CPR_number
    JOIN manages m ON c.CPR_number = m.CPR_number
    WHERE m.emp_cpr_number = %s
    ORDER BY cl.claim_date DESC;
    """
    cur.execute(sql, (employee_id,))
    claims = cur.fetchall()
    cur.close()

    pending_claims = [claim for claim in claims if claim[6] == 'pending']
    resolved_claims = [claim for claim in claims if claim[6] != 'pending']

    return pending_claims, resolved_claims




def update_claim_status(claim_id, status):
    cur = conn.cursor()
    try:
        sql = """
        UPDATE claims
        SET status = %s
        WHERE claim_id = %s;
        """
        cur.execute(sql, (status, claim_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def get_all_policies():
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    sql = "SELECT * FROM policies"
    cur.execute(sql)
    policies = cur.fetchall()
    cur.close()
    return policies

def get_policy_by_id(policy_id):
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    sql = "SELECT * FROM policies WHERE policy_id = %s"
    cur.execute(sql, (policy_id, ))
    policy = cur.fetchone()
    cur.close()
    return policy


def add_policy(policy_type, start_date, end_date, premium, cover_amount, excess):
    cur = conn.cursor()
    sql = """
    INSERT INTO policies (policy_type, start_date, end_date, premium, cover_amount, excess)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (policy_type, start_date, end_date, premium, cover_amount, excess))
    conn.commit()
    cur.close()

def update_policy(policy_id, start_date, end_date, premium, cover_amount, excess):
    cur = conn.cursor()
    try:
        sql = """
        UPDATE policies
        SET policy_type = %s, start_date = %s, end_date = %s, premium = %s, cover_amount = %s, excess = %s
        WHERE policy_id = %s
        """
        cur.execute(sql, (start_date, end_date, premium, cover_amount, excess, policy_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def delete_policy(policy_id):
    cur = conn.cursor()
    try:
        # Check for dependencies in customer_policies and claims
        cur.execute("DELETE FROM customer_policies WHERE policy_id = %s", (policy_id,))
        cur.execute("DELETE FROM claims WHERE policy_id = %s", (policy_id,))
        
        # Now delete the policy
        cur.execute("DELETE FROM policies WHERE policy_id = %s", (policy_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback the transaction if any exception occurs
        raise e  # Re-raise the exception to be handled by the calling function
    finally:
        cur.close()




# def select_emp_investments(emp_cpr_number):
#     # employee id is parameter
#     cur = conn.cursor()
#     sql = """
#     SELECT i.account_number, a.cpr_number, a.created_date 
#     FROM investmentaccounts i
#     JOIN accounts a ON i.account_number = a.account_number
#     JOIN manages m ON m.account_number = a.account_number
#     JOIN employees e ON e.id = m.emp_cpr_number
#     WHERE e.id = %s
#     """
#     cur.execute(sql, (emp_cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset

# def select_emp_investments_with_certificates(emp_cpr_number):
#     # employee id is parameter
#     cur = conn.cursor()
#     sql = """
#     SELECT i.account_number, a.cpr_number, a.created_date
#     , cd.cd_number, start_date, maturity_date, rate, amount 
#     FROM investmentaccounts i
#     JOIN accounts a ON i.account_number = a.account_number
#     JOIN certificates_of_deposit cd ON i.account_number = cd.account_number    
#     JOIN manages m ON m.account_number = a.account_number
#     JOIN employees e ON e.id = m.emp_cpr_number
#     WHERE e.id = %s
#     ORDER BY 1
#     """
#     cur.execute(sql, (emp_cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset

# def select_emp_investments_certificates_sum(emp_cpr_number):
#     # employee id is parameter
#     cur = conn.cursor()
#     sql = """
#     SELECT account_number, cpr_number, created_date, sum
#     FROM vw_cd_sum
#     WHERE emp_cpr_number = %s
#     ORDER BY 2,1
#     """
#     cur.execute(sql, (emp_cpr_number,))
#     tuple_resultset = cur.fetchall()
#     cur.close()
#     return tuple_resultset
