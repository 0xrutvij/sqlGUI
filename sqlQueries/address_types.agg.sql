SELECT contact_id,
                group_concat(address_type) 
  FROM address
 GROUP BY contact_id
 ORDER BY contact_id;
