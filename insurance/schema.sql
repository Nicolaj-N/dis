\i schema_drop.sql

CREATE TABLE IF NOT EXISTS customers(
  CPR_number INTEGER PRIMARY KEY,
  name VARCHAR(60),
  password VARCHAR(120),
  address TEXT
);


CREATE TABLE IF NOT EXISTS employees(
	id INTEGER PRIMARY KEY,
    name VARCHAR(20),
    password VARCHAR(120)
);


CREATE TABLE IF NOT EXISTS manages(
	emp_cpr_number INTEGER NOT NULL REFERENCES employees(id),
	CPR_number INTEGER NOT NULL REFERENCES customers(CPR_number)
);
ALTER TABLE manages ADD CONSTRAINT pk_manages
  PRIMARY KEY (emp_cpr_number, CPR_number)
  ;


CREATE TABLE IF NOT EXISTS policies(
    policy_id SERIAL PRIMARY KEY,
    policy_type VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    premium DECIMAL(10, 2),
	cover_amount DECIMAL(10, 2),
	excess DECIMAL(10, 2)
);


CREATE TABLE IF NOT EXISTS policy_templates(
    id SERIAL PRIMARY KEY,
    policy_type VARCHAR(50),
    premium DECIMAL(10, 2),
	cover_amount DECIMAL(10, 2),
	excess DECIMAL(10, 2)
);


CREATE TABLE IF NOT EXISTS customer_policies(
    id SERIAL PRIMARY KEY,
    CPR_number INTEGER REFERENCES customers(CPR_number),
    policy_id INTEGER REFERENCES policies(policy_id)
);


CREATE TABLE IF NOT EXISTS claims(
    claim_id SERIAL PRIMARY KEY,
    policy_id INTEGER REFERENCES policies(policy_id),
    claim_date TIMESTAMP,
    claim_amount DECIMAL(10, 2),
    status VARCHAR(20),
    description TEXT
);


-- CREATE TABLE IF NOT EXISTS payments(
--     payment_id SERIAL PRIMARY KEY,
--     payment_date TIMESTAMP,
--     amount DECIMAL(10, 2),
--     payment_method VARCHAR(20)
-- );

-- CREATE TABLE IF NOT EXISTS policy_payments(
-- 	id SERIAL PRIMARY KEY,
-- 	policy_id INTEGER REFERENCES policies(policy_id),
-- 	payment_id INTEGER REFERENCES payments(payment_id)
-- );

-- CREATE TABLE IF NOT EXISTS claim_payments(
-- 	id SERIAL PRIMARY KEY,
-- 	claim_id INTEGER REFERENCES claims(claim_id),
-- 	payment_id INTEGER REFERENCES payments(payment_id)
-- );


-- \i sql_ddl/vw_cd_sum.sql
-- \i sql_ddl/vw_invest_accounts.sql
-- \i sql_ddl/vw_invest_certificates.sql
-- \i sql_ddl/vw_tdw.sql
-- \i sql_ddl/ddl-customers-001-add.sql
