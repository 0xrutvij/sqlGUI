Insert into simplified_text_search(
  contact_id, first_name, middle_name,
  last_name, address_type, address,
  city, state, zip, date_type, date,
  phone_type, area_code, number
)
SELECT
  contact.contact_id,
  first_name,
  middle_name,
  last_name,
  address_type,
  address,
  city,
  state,
  zip,
  date_type,
  date,
  phone_type,
  area_code,
  number
FROM
  contact
  LEFT JOIN (
    SELECT
      *
    FROM
      date
  ) AS dates ON contact.contact_id = dates.contact_id
  LEFT JOIN (
    SELECT
      *
    FROM
      address
  ) AS adds ON contact.contact_id = adds.contact_id
  LEFT JOIN (
    SELECT
      *
    FROM
      phone
  ) AS phs ON contact.contact_id = phs.contact_id;
