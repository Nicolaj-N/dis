--
-- schema_ins.sql
-- Populate bank schema with data.
--
\echo Emptying the bank database. Deleting all tuples.

DELETE FROM customers
DELETE FROM employees
DELETE FROM manages
DELETE FROM policies
DELETE FROM policy_templates
DELETE FROM customer_policies
DELETE FROM claims

\echo .
\echo
\echo Adding data:
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5000, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-DB3-C-Lasse', 'aud Auditorium A, bygning 1, 1. sal Universitetsparken 15 (Zoo)');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5001, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-PD3-C-Anders', 'øv* Kursussal 1, bygning 3, 1.sal Universitetsparken 15 (Zoo)');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5002, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-DB2-C-Ziming', 'øv 4032, Ole Maaløes Vej 5 (Biocenter)');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5003, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-PD2-C-Hubert', 'øv Auditorium Syd, Nørre Alle 51');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5004, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-DB1-C-Jan', 'øv A112, Universitetsparken 5, HCØ');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5005, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-PD1-C-Marco', 'Aud 07, Universitetsparken 5, HCØ');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5006, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-LE1-C-Marcos', 'AUD 02 in the HCØ building (HCØ, Universitetsparken 5)');
INSERT INTO public.customers(cpr_number, password, name, address) VALUES (5007, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-LE2-C-Finn', 'AUD 02 in the HCØ building (HCØ, Universitetsparken 5)');

INSERT INTO public.customers(cpr_number, password, name, address) 
VALUES (5008, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-PD1-C-Rikke', 'AUD 08, Universitetsparken 5, HCØ')
,      (5009, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-DB1-C-Pax'  , 'AUD 05, Universitetsparken 5, HCØ')
,      (5010, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'UIS-PD2-C-Nadja', 'AUD 08, Universitetsparken 5, HCØ')
;

UPDATE public.customers SET address = 'AUD 08, Universitetsparken 5, HCØ' WHERE cpr_number IN (5001); 
UPDATE public.customers SET address = 'aud - Lille UP1 - 04-1-22, Universitetsparken 1-3, DIKU' WHERE cpr_number IN (5003, 5007); 
UPDATE public.customers SET address = 'online-zoom'      WHERE cpr_number IN (5006); 
UPDATE public.customers SET name    = 'UIS-DB2-C-Anders' WHERE cpr_number IN (5008); 
UPDATE public.customers SET name    = 'UIS-LE-C-Hubert'  WHERE cpr_number IN (5003); 

	



\echo ..

INSERT INTO public.Employees(id, name, password)
VALUES (6000, 'UIS-DB3-E-Lasse',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx')
, (6001, 'UIS-PD3-E-Anders',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6002, 'UIS-DB2-E-Ziming',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6003, 'UIS-PD2-E-Hubert',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6004, 'UIS-DB1-E-Jan'   ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6005, 'UIS-PD1-E-Marco' ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6006, 'UIS-LE1-E-Marcos',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (6007, 'UIS-LE2-E-Finn' ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
;

INSERT INTO public.Employees(id, name, password)
VALUES (6008, 'UIS-PD3-E-Rikke',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
,      (6009, 'UIS-DB2-E-Pax'  ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
,      (6010, 'UIS-PD2-E-Nadja',  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
;

\echo ....
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6000, 5000);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6000, 5001);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6001, 5002);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6001, 5003);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6002, 5004);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6002, 5005);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6003, 5006);
INSERT INTO public.manages(emp_cpr_number, cpr_number) VALUES (6003, 5007);

--
-- from schema_upd.sql 20231112
--
\echo "from schema_upd.sql 20231112"

-- new certificate fixed rate 4 percent
\echo ..............



--
-- from schema_upd_2.sql 20231112
--
\echo "from schema_upd_2.sql 20231112"


UPDATE public.customers SET name    = 'C-5000-Theo'        , address = '3-0-25, UP 1 (DIKU)' WHERE cpr_number IN (5000); 
UPDATE public.customers SET name    = 'C-5001-Lennard'     , address = 'Kursussal 4A, UP 15 (ZOO)' WHERE cpr_number IN (5001); 
UPDATE public.customers SET name    = 'C-5002-Karl'        , address = '4-0-24, Biocenter' WHERE cpr_number IN (5002); 
UPDATE public.customers SET name    = 'C-5003-Christian M' , address = 'Lundbeck Auditoriet, Biocenter' WHERE cpr_number IN (5003);
--JAN 
UPDATE public.customers SET name    = 'C-5004-Jan'          , address = 'AB Teori 2, NEXS (DHL)' WHERE cpr_number IN (5004); 
UPDATE public.customers SET name    = 'C-5005-Asbjørn Marco', address = 'Auditorium A, UP 15 (ZOO)' WHERE cpr_number IN (5005); 
UPDATE public.customers SET name    = 'C-5006-Christian A'  , address = 'Aud 01, UP 5 (HCØ)' WHERE cpr_number IN (5006); 
UPDATE public.customers SET name    = 'C-5007-Cathy'        , address = '4-0-05, Biocenter' WHERE cpr_number IN (5007); 
--Anders
UPDATE public.customers SET name    = 'C-5008-Anders'       , address = 'AB Teori 2(DHL),Aud 01(HCØ),3-0-25(DIKU)' WHERE cpr_number IN (5008); 
UPDATE public.customers SET name    = 'C-5009-Axel'         , address = 'Lundbeck Auditoriet, Biocenter' WHERE cpr_number IN (5009); 
UPDATE public.customers SET name    = 'C-5010-Andreas'      , address = '4-0-10, Biocenter' WHERE cpr_number IN (5010); 
--
INSERT INTO public.customers(cpr_number,  password, name, address) 
VALUES (5011, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'C-5011-Ana'     , 'Auditorium A (ZOO), Kursussal 4A (ZOO),4-0-24, Biocenter')
,      (5012, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'C-5012-Dmitri'  , 'Lundbeck Auditoriet, 4-0-05,4-0-10  Biocenter')
;


--  delete from public.customers where cpr_number in (5011, 5012);

UPDATE public.employees SET password    = '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO' WHERE id IN (6000); 



UPDATE public.employees SET name    = 'DIS-E-Ana' WHERE id IN (6000); 
UPDATE public.employees SET name    = 'LE-E-Dmitri' WHERE id IN (6001); 
UPDATE public.employees SET name    = 'DS-E-Andreas' WHERE id IN (6002); 
UPDATE public.employees SET name    = 'DS-E-Asbjørn Marco' WHERE id IN (6003); 
UPDATE public.employees SET name    = 'DS-E-Axel' WHERE id IN (6004); --JAN
UPDATE public.employees SET name    = 'DIS-E-Cathy' WHERE id IN (6005); 
UPDATE public.employees SET name    = 'DS-E-Christian Arboe' WHERE id IN (6006); --Marco
UPDATE public.employees SET name    = 'DS-E-Christian M' WHERE id IN (6007); 
UPDATE public.employees SET name    = 'DS-E-Karl' WHERE id IN (6010); 
UPDATE public.employees SET name    = 'DIS-E-Jan' WHERE id IN (6008); 
UPDATE public.employees SET name    = 'UIS-E-Anders' WHERE id IN (6009); 
UPDATE public.employees SET name    = 'DS-E-Karl' WHERE id IN (6010); 


INSERT INTO public.Employees(id, name, password)
VALUES (6011, 'DIS-E-Lennard'  ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
,      (6012, 'DS-E-Theo'      ,  '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
;

-- select name, cpr_number, count (account_number) from customers natural join accounts group by name, cpr_number order by 2;
-- select emp_cpr_number, account_number, cpr_number from manages natural join accounts order by 3,1;

\echo ...............

-- test
INSERT INTO policy_templates (policy_type, premium)
VALUES ('Health Insurance', 500.00);
INSERT INTO policy_templates (policy_type, premium)
VALUES ('Travel Insurance', 200.00);
-- ALTER TABLE Customers ADD COLUMN policy_id INTEGER REFERENCES Policies(policy_id);


\echo ...............
\echo done
