select contact.contact_id, first_name, middle_name, last_name, addresses, phones, dates
from contact
left join (select contact_id, group_concat(date_type || ' ' || date, ';' || char(10)) as dates from date group by contact_id) as gdate 
    on contact.contact_id = gdate.contact_id
left join (select contact_id, 
           group_concat(upper(address_type) || ': ' || address
           || ', ' || city
           || ', ' || state
           || ', ' || zip
           , ';' || char(10)) 
    as addresses from address group by contact_id) as gadd 
    on contact.contact_id = gadd.contact_id
left join (select contact_id, group_concat(phone_type
    || ': ' || area_code
    || '-'  || number, ';' || char(10))
    as phones from phone group by contact_id) as gph
    on contact.contact_id = gph.contact_id;
    