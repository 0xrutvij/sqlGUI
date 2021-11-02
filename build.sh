#!/Users/rutvijshah/PycharmProjects/sqlGUI/venv/bin/activate

files=($(ls ./ui))

for x in $files; do
  pyuic5 ./ui/"$x" > ./src/generated_views/"${x%%.*}".py
done
