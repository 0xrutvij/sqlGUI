#! /bin/zsh


if command -v pyuic5 &> /dev/null
then
  for x in ./ui/*; do
    pyuic5 "$x" > ./src/generated_views/$(basename "$x" .ui).py
  done
else
  echo "pyuic5 not found, using exisiting UI -> .py conversions"
fi

rm -rf resources/contacts.db
python3 create_db.py
sqlite3 resources/contacts.db < ./sqlQueries/define_text_search.sql
sqlite3 resources/contacts.db < ./sqlQueries/populate_text_search.sql
sqlite3 resources/contacts.db < ./sqlQueries/triggers.sql