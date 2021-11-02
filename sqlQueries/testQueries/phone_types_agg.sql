SELECT DISTINCT contact_id,
                group_concat(phone_type) 
  FROM phone
 GROUP BY contact_id
 ORDER BY contact_id;
