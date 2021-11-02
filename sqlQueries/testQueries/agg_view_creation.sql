CREATE VIEW contact_book (
    cid,
    fname,
    mname,
    lname,
    addresses,
    phones,
    dates
)
AS
    SELECT contact.contact_id,
           first_name,
           middle_name,
           last_name,
           addresses,
           phones,
           dates
      FROM contact
           LEFT JOIN
           (
               SELECT contact_id,
                      group_concat(date_type || ' ' || date, ';' || char(10) ) AS dates
                 FROM date
                GROUP BY contact_id
           )
           AS gdate ON contact.contact_id = gdate.contact_id
           LEFT JOIN
           (
               SELECT contact_id,
                      group_concat(upper(address_type) || ': ' || address || ', ' || city || ', ' || state || ', ' || zip, ';' || char(10) ) AS addresses
                 FROM address
                GROUP BY contact_id
           )
           AS gadd ON contact.contact_id = gadd.contact_id
           LEFT JOIN
           (
               SELECT contact_id,
                      group_concat(phone_type || ': ' || area_code || '-' || number, ';' || char(10) ) AS phones
                 FROM phone
                GROUP BY contact_id
           )
           AS gph ON contact.contact_id = gph.contact_id;
