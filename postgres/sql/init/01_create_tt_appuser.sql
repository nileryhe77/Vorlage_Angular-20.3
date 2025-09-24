CREATE TABLE IF NOT EXISTS tt_appuser (
    appuser_id UUID NOT NULL DEFAULT uuid_generate_v4(),
    keycloak_id VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    display_name VARCHAR(255),
    active_ BOOLEAN NOT NULL DEFAULT TRUE,
    since_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT appuser_pkey PRIMARY KEY (appuser_id, since_)
);
