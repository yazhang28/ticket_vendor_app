/* ------- buyer_type ------- */
  CREATE TABLE IF NOT EXISTS buyer_referral_type (
    id SERIAL,
    type VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
  );

/* ------- buyer ------- */
  CREATE TABLE IF NOT EXISTS buyer (
    email_address VARCHAR(50) CONSTRAINT email_address CHECK (email_address ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9-]+[.][A-Za-z]+$'),
    buyer_referral_type_id BIGINT NOT NULL REFERENCES buyer_referral_type,
    first_name VARCHAR(50) NOT NULL CONSTRAINT first_name CHECK (first_name ~* '[a-zA-Z]+'),
    last_name VARCHAR(50) NOT NULL CONSTRAINT last_name CHECK ( last_name ~* '[a-zA-Z]+'),
    phone_number VARCHAR(50) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (email_address)
  );

/* ------- payment_method ------- */
  CREATE TABLE IF NOT EXISTS payment_method (
    id SERIAL,
    buyer_email_address VARCHAR(50) NOT NULL REFERENCES buyer,
    billing_address VARCHAR(100) CONSTRAINT billing_address CHECK (billing_address ~ '[\sA-Za-z0-9.]+'),
    city VARCHAR(100),
    postal_code VARCHAR(10) CONSTRAINT postal_code CHECK (postal_code ~ '[0-9]'),
    credit_card_number VARCHAR(20) UNIQUE,
    security_code VARCHAR(4) CONSTRAINT security_code CHECK (security_code ~ '[0-9]'),
    month_exp INT CONSTRAINT month_exp CHECK (month_exp <=12 AND month_exp >= 1),
    year_exp INT,
    internal_payment_method BOOLEAN NOT NULL DEFAULT FALSE,
    external_payment_method BOOLEAN NOT NULL DEFAULT FALSE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id)
  );

/* ------- city_type ------- */
  CREATE TABLE IF NOT EXISTS city_type (
    id SERIAL,
    city VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
  );

/* ------- event ------- */
  CREATE TABLE IF NOT EXISTS event (
    id SERIAL,
    date DATE NOT NULL,
    time TIME WITH TIME ZONE NOT NULL,
    PRIMARY KEY (id)
  );

