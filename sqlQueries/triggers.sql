-- Phone Triggers
CREATE TRIGGER ph_insert_search_sync
AFTER
  INSERT ON phone BEGIN INSERT INTO simplified_text_search (
    contact_id, phone_type, area_code,
    number
  )
VALUES
  (
    new.contact_id, new.phone_type, new.area_code,
    new.number
  );
END;

CREATE TRIGGER ph_update_search_sync
AFTER
UPDATE
  ON phone FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  (old.number = number);
INSERT INTO simplified_text_search (
  contact_id, phone_type, area_code,
  number
)
VALUES
  (
    new.contact_id, new.phone_type, new.area_code,
    new.number
  );
END;

CREATE TRIGGER ph_delete_search_sync
AFTER
  DELETE ON phone FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  old.contact_id = contact_id
  AND old.number = number;
END;

-- Date Triggers
CREATE TRIGGER date_insert_search_sync
AFTER
  INSERT ON date FOR EACH ROW BEGIN INSERT INTO simplified_text_search (contact_id, date_type, date)
VALUES
  (
    new.contact_id, new.date_type, new.date
  );
END;

CREATE TRIGGER date_delete_search_sync
AFTER
  DELETE ON date FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  old.contact_id = contact_id
  AND old.date_type = date_type;
END;

CREATE TRIGGER date_update_search_sync
AFTER
UPDATE
  ON date FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  old.contact_id = contact_id
  AND old.date_type = date_type;
INSERT INTO simplified_text_search (contact_id, date_type, date)
VALUES
  (
    new.contact_id, new.date_type, new.date
  );
END;

-- Address Triggers
CREATE TRIGGER address_insert_search_sync
AFTER
  INSERT ON address FOR EACH ROW BEGIN INSERT INTO simplified_text_search (
    contact_id, address_type, address,
    city, state, zip
  )
VALUES
  (
    new.contact_id, new.address_type,
    new.address, new.city, new.state,
    new.zip
  );
END;

CREATE TRIGGER address_update_search_sync
AFTER
UPDATE
  ON address FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  old.contact_id = contact_id
  AND old.address = address;
INSERT INTO simplified_text_search (
  contact_id, address_type, address,
  city, state, zip
)
VALUES
  (
    new.contact_id, new.address_type,
    new.address, new.city, new.state,
    new.zip
  );
END;

CREATE TRIGGER address_delete_search_sync
         AFTER DELETE
            ON address
      FOR EACH ROW
BEGIN
    DELETE FROM simplified_text_search
          WHERE old.contact_id = contact_id AND
                old.address = address;
END;

-- Contact Triggers
CREATE TRIGGER contact_insert_search_sync
AFTER
  INSERT ON contact FOR EACH ROW BEGIN INSERT INTO simplified_text_search (
    contact_id, first_name, middle_name,
    last_name
  )
VALUES
  (
    new.contact_id, new.first_name, new.middle_name,
    new.last_name
  );
END;

CREATE TRIGGER contact_update_search_sync
AFTER
UPDATE
  ON contact BEGIN
UPDATE
  simplified_text_search
SET
  first_name = new.first_name,
  middle_name = new.middle_name,
  last_name = new.last_name
WHERE
  contact_id = old.contact_id;
END;

CREATE TRIGGER contact_delete_search_sync
AFTER
  DELETE ON contact FOR EACH ROW BEGIN
DELETE FROM
  simplified_text_search
WHERE
  old.contact_id = contact_id;
END;
