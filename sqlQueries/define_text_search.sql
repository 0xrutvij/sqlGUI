CREATE VIRTUAL TABLE simplified_text_search USING fts5(
  contact_id, first_name, middle_name,
  last_name, address_type, address,
  city, state, zip, date_type, date,
  phone_type, area_code, number,
  tokenize = 'trigram'
);