#!/Users/rutvijshah/PycharmProjects/sqlGUI/venv/bin/activate

files=($(ls ./ui))

for x in $files; do
  pyuic5 ./ui/"$x" > ./src/generated_views/"${x%%.*}".py
done

rm -rf contacts.db
python3 create_db.py
sqlite3 contacts.db < ./sqlQueries/define_text_search.sql
sqlite3 contacts.db < ./sqlQueries/populate_text_search.sql
sqlite3 contacts.db < ./sqlQueries/triggers.sql