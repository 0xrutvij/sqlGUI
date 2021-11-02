SELECT contact_id,
                group_concat(date_type) 
  FROM date
 GROUP BY contact_id
 ORDER BY contact_id;
