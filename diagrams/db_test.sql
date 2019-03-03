/* ===================== positve passed test ===================== */
INSERT INTO buyer (email_address, buyer_referral_type_id, first_name, last_name, phone_number)
VALUES ('test@testing.com',1,'joe','smith','234'),
       ('apple@orange.com',1,'apple','orange','1');
INSERT INTO payment_method (buyer_id, billing_address, city, postal_code, credit_card_number, security_code, month_exp, year_exp)
VALUES ('1', '123 apple.ave p.0 box 34', 'pumpkinville', '0123456789', '1234123412345', '1234', 1, 2019);

INSERT INTO city_type (city) VALUES ('Montreal');
INSERT INTO event (date, time, city_type_id) VALUES ('01/02/2019', '01:01:01', 1);

INSERT INTO ticket (event_id, row, section, price, quantity)
VALUES (4, 'A1', 23, 45, 4);

UPDATE ticket SET
  buyer_id = 1,
  date_sold = current_timestamp,
  delivery_by_email = TRUE,
  sold = TRUE
WHERE event_id = 4;

-- INSERT INTO ticket (event_id, buyer_email_adress, row, section, price, date_sold, delivery_by_mail, delivery_by_phone)
-- VALUES

/* ===================== positve failed test ===================== */

-- email, postal_code, credit_card_number, security_code, month_exp, date_exp
INSERT INTO payment_method (buyer_email_address, billing_address, city, postal_code, credit_card_number, security_code, month_exp, year_exp)
VALUES ('A@B.COM', '123 apple.ave p.0 box 34', 'pumpkinville', '012345678910', '1234123412345', '12345', 13, 2014);

-- missing required fields when purchasing: delivery_by_email, delivery_by_phone
UPDATE ticket SET
  buyer_id = 1,
  date_sold = current_timestamp
WHERE event_id = 4;