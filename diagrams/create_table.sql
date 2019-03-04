/* ------- buyer_referral_type ------- */
  CREATE TABLE IF NOT EXISTS buyer_referral_type (
    id SERIAL,
    type VARCHAR(50) UNIQUE NOT NULL,
    PRIMARY KEY (id)
  );

  INSERT INTO buyer_referral_type (type)
    VALUES ('Internal'),
           ('Other');

/* ------- buyer ------- */
  CREATE TABLE IF NOT EXISTS buyer (
    id SERIAL,
    buyer_referral_type_id BIGINT NOT NULL REFERENCES buyer_referral_type,
    buyer_referral_type_txt VARCHAR(50) NOT NULL,
    email_address VARCHAR(50) UNIQUE CONSTRAINT email_address CHECK (email_address ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$'),
    first_name VARCHAR(50) NOT NULL CONSTRAINT first_name CHECK (first_name ~* '[a-zA-Z]+'),
    last_name VARCHAR(50) NOT NULL CONSTRAINT last_name CHECK (last_name ~* '[a-zA-Z]+'),
    phone_number VARCHAR(50),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id)
  );

/* ------- buyer_payment_method ------- */
  CREATE TABLE IF NOT EXISTS buyer_payment_method (
    id SERIAL,
    buyer_id INT NOT NULL REFERENCES buyer,
    billing_address VARCHAR(100) CONSTRAINT billing_address CHECK (billing_address ~ '[\sA-Za-z0-9.]+'),
    city VARCHAR(100),
    postal_code VARCHAR(10) CONSTRAINT postal_code CHECK (postal_code ~ '[0-9]'),
    credit_card_number VARCHAR(20) UNIQUE,
    security_code VARCHAR(4) CONSTRAINT security_code CHECK (security_code ~ '[0-9]'),
    month_exp INT CONSTRAINT month_exp CHECK (month_exp <=12 AND month_exp >= 1),
    year_exp INT CONSTRAINT year_exp CHECK (year_exp >= extract(YEAR FROM CURRENT_DATE)::INT),
    internal_payment_method BOOLEAN NOT NULL DEFAULT FALSE,
    external_payment_method BOOLEAN NOT NULL DEFAULT FALSE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id)
  );

/* ------- city ------- */
  CREATE TABLE IF NOT EXISTS city (
    id SERIAL,
    city VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (id)
  );

/* ------- event ------- */
  CREATE TABLE IF NOT EXISTS event (
    id SERIAL,
    date DATE NOT NULL,
    time TIME WITH TIME ZONE NOT NULL,
    city_type_id INT NOT NULL REFERENCES city,
    PRIMARY KEY (id)
  );

/* ------- ticket ------- */
CREATE TABLE IF NOT EXISTS ticket (
  id SERIAL,
  event_id BIGINT NOT NULL REFERENCES event,
  buyer_id INT REFERENCES buyer,
  row VARCHAR(5) NOT NULL,
  section INT NOT NULL,
  quantity INT NOT NULL,
  price INT NOT NULL,
  sold BOOLEAN NOT NULL DEFAULT FALSE,
  date_sold TIMESTAMP,
  delivery_by_email BOOLEAN,
  delivery_by_phone BOOLEAN,
  CONSTRAINT required_fields_for_sale CHECK (
    (date_sold IS NULL
       AND buyer_id IS NULL
       AND delivery_by_email IS NULL
       AND delivery_by_phone IS NULL)
    OR (date_sold IS NOT NULL
      AND buyer_id IS NOT NULL
      AND delivery_by_email IS NOT NULL
      AND delivery_by_phone IS NULL)
    OR (date_sold IS NULL
      AND buyer_id IS NOT NULL
      AND delivery_by_email IS NULL
      AND delivery_by_phone IS NOT NULL)
    )
);