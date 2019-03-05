/* ===================== positve passed test ===================== */
INSERT INTO buyer_referral_type (type)
VALUES ('Internal'),
       ('Other');

INSERT INTO buyer (email_address, buyer_referral_type_id, first_name, last_name, phone_number)
VALUES ('test@testing.com',1,'joe','smith','234'),
       ('apple@orange.com',1,'apple','orange','1');

INSERT INTO city (city) VALUES ('Montreal');
INSERT INTO event (date, time, city_id, city_txt) VALUES ('01/02/2019', '01:01:01', 1, 'toronto');

INSERT INTO ticket (event_id, row, section, price, quantity)
VALUES (1, 'A1', 23, 45, 4);

UPDATE ticket SET
  buyer_id = 1,
  date_sold = current_timestamp,
  delivery_by_email = TRUE,
  sold = TRUE
WHERE event_id = 1;

-- INSERT INTO ticket (event_id, buyer_email_adress, row, section, price, date_sold, delivery_by_mail, delivery_by_phone)
-- VALUES

/* ===================== positve failed test ===================== */
-- missing required fields when purchasing: delivery_by_email, delivery_by_phone
UPDATE ticket SET
  buyer_id = 1,
  date_sold = current_timestamp
WHERE event_id = 4;