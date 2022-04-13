CREATE DATABASE vista_test_task_phone_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE vista_test_task_phone_book;

CREATE USER vista_phone_book_user IDENTIFIED by 'public_password';

-- *** Tables ***

CREATE TABLE users
(
    id         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(255) NOT NULL UNIQUE,
    email      VARCHAR(255) NOT NULL UNIQUE,
    password   CHAR(32)     NOT NULL,
    birth_date DATE         NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT now()
);

CREATE TABLE sessions
(
    id          INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id     INT      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    session_key CHAR(32) NOT NULL UNIQUE,
    created_at  DATETIME NOT NULL DEFAULT now()
);

CREATE TABLE contacts
(
    id           INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15)  NOT NULL,
    birth_date   DATE,
    owner_id     INT          NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE INDEX contact_uniq_within_user_data (name, phone_number, birth_date, owner_id)
);


-- *** Stored procedures ***

DELIMITER //
CREATE PROCEDURE check_session(session_key CHAR(32), OUT session_exists BOOL)
    NOT DETERMINISTIC
    READS SQL DATA
    COMMENT 'check whether a session exists'
    SET session_exists = EXISTS(SELECT 42
                                FROM sessions
                                WHERE sessions.session_key = session_key);
//

CREATE PROCEDURE register(username VARCHAR(255), email VARCHAR(255), birth_date DATE,
                          OUT result VARCHAR(255), OUT password CHAR(8))
    NOT DETERMINISTIC
    MODIFIES SQL DATA
    COMMENT 'create a new user'
    IF EXISTS(SELECT 42
              FROM users as u
              WHERE u.username = username) THEN
        SET result = 'username_already_exists';
    ELSEIF EXISTS(SELECT 42
                  FROM users as u
                  WHERE u.email = email) THEN
        SET result = 'email_already_exists';
    ELSE
        BEGIN
            SELECT SUBSTR(md5(rand()), 1, 8) INTO password;
            -- TODO: send a password by an email
            INSERT INTO users(username, email, password, birth_date)
            VALUES (username, email, md5(password), birth_date);
            IF EXISTS(SELECT 42 FROM users as u WHERE u.username = username) THEN
                SET result = 'registered_successfully';
            ELSE
                SET result = 'unknown_error';
            END IF;
        END;
    END IF;
//

CREATE PROCEDURE log_in(username_or_email VARCHAR(255), password VARCHAR(255), OUT session_key CHAR(32))
    NOT DETERMINISTIC
    MODIFIES SQL DATA
    COMMENT 'create a new session'
main:
BEGIN
    DECLARE user_id INT;
    SET user_id = (SELECT u.id
                   FROM users AS u
                   WHERE (u.username = username_or_email OR u.email = username_or_email)
                     AND u.password = md5(password)
                   LIMIT 1);
    IF user_id IS NULL THEN
        LEAVE main;
    END IF;
    SET session_key = md5(rand()); -- TODO: ensure the generated key is not a duplicate
    INSERT INTO sessions (user_id, session_key) VALUES (user_id, session_key);
END;
//

CREATE PROCEDURE log_out(session_key CHAR(32))
    NOT DETERMINISTIC
    MODIFIES SQL DATA
    COMMENT 'remove the passed session_key'
DELETE
FROM sessions
WHERE sessions.session_key = session_key;
//

CREATE PROCEDURE get_user_info(session_key CHAR(32), OUT username VARCHAR(255), OUT email VARCHAR(255))
    NOT DETERMINISTIC
    READS SQL DATA
    COMMENT 'select an username & an e-mail'
SELECT u.username, u.email
INTO username, email
FROM users as u
WHERE u.id = (SELECT user_id FROM sessions WHERE sessions.session_key = session_key LIMIT 1);
//

CREATE PROCEDURE get_all_contacts(session_key CHAR(32))
    NOT DETERMINISTIC
    READS SQL DATA
    COMMENT 'select all user\'s contacts'
SELECT id, name, phone_number, birth_date
FROM contacts
WHERE owner_id = (SELECT user_id FROM sessions WHERE sessions.session_key = session_key LIMIT 1);
//

CREATE PROCEDURE get_contacts(session_key CHAR(32), letter_set VARCHAR(255), exclude BOOL)
    NOT DETERMINISTIC
    READS SQL DATA
    COMMENT 'select user\'s contacts if a name (not) starting with one of given letters if exclude = (False) True'

SELECT id, name, phone_number, birth_date
FROM contacts
WHERE owner_id = (SELECT user_id FROM sessions WHERE sessions.session_key = session_key LIMIT 1)
  AND (name REGEXP CONCAT('(?i)^[', letter_set, ']') XOR exclude)
ORDER BY name;
//

CREATE PROCEDURE add_contact(session_key CHAR(32), name VARCHAR(255), phone_number VARCHAR(15), birth_date DATE,
                             OUT result VARCHAR(255), OUT contact_id INT)
    NOT DETERMINISTIC
    MODIFIES SQL DATA
    COMMENT 'create a new contact'
main:
BEGIN
    DECLARE owner_id INT;
    SET owner_id = (SELECT user_id FROM sessions WHERE sessions.session_key = session_key LIMIT 1);
    IF owner_id IS NULL THEN
        SET result = 'invalid_session_key';
        LEAVE main;
    END IF;
    SET contact_id = (SELECT id
                      FROM contacts as c
                      WHERE c.owner_id = owner_id
                        AND c.name = name
                        AND c.phone_number = phone_number
                        AND c.birth_date = birth_date
                      LIMIT 1);
    IF contact_id IS NOT NULL THEN
        SET result = 'contact_already_exists';
        LEAVE main;
    END IF;
    INSERT INTO contacts(name, phone_number, birth_date, owner_id) VALUES (name, phone_number, birth_date, owner_id);
    SET contact_id = (SELECT id
                      FROM contacts as c
                      WHERE c.owner_id = owner_id
                        AND c.name = name
                        AND c.phone_number = phone_number
                        AND c.birth_date = birth_date
                      LIMIT 1);
    IF contact_id IS NOT NULL THEN
        SET result = 'added_successfully';
    ELSE
        SET result = 'unknown_error';
    END IF;
END;
//

DELIMITER ;

GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.check_session TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.register TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.log_in TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.log_out TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.get_user_info TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.get_all_contacts TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.get_contacts TO 'vista_phone_book_user';
GRANT EXECUTE ON PROCEDURE vista_test_task_phone_book.add_contact TO 'vista_phone_book_user';