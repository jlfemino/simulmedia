
CREATE TABLE 'user' (
    user_id char(36) NOT NULL PRIMARY KEY,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name char(256) NOT NULL
);

-- TODO: Remove test data from DB migration file
INSERT INTO 'user' (user_id, name) VALUES
    ('e38c6813-5228-4f59-a250-c5948a054502', 'Nomi'),
    ('1007b32d-e692-454f-b1cb-acf1e7e6e01a', 'Baruta');

CREATE TABLE 'ad' (
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ad_id char(36) NOT NULL PRIMARY KEY,
    video_url char(2000) NOT NULL,
    country char(2) NOT NULL,
    lang char(2) NOT NULL,
    start_hour tinyint NOT NULL,
    end_hour tinyint NOT NULL
);

-- TODO: Remove test data from DB migration file
INSERT INTO 'ad' (ad_id, video_url, country, lang, start_hour, end_hour) VALUES
    ('111111', 'http://www.111111.ro/', 'RO', 'ro', 0, 24),
    ('222222', 'http://www.222222.ro/', 'RO', 'ro', 3, 21),
    ('333333', 'http://www.333333.ro/', 'RO', 'ro', 6, 18);


CREATE TABLE IF NOT EXISTS 'user_ad_view' (
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id char(36) NOT NULL,
    ad_id char(36) NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES user(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (ad_id)
        REFERENCES ad(ad_id)
        ON DELETE CASCADE
);
