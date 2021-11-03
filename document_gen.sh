#! /bin/zsh

pandoc docs/DesignDoc.md --pdf-engine=xelatex -o docs/DesignDoc.pdf
pandoc docs/README.md --pdf-engine=xelatex -o docs/README.pdf
pandoc docs/README.md --from markdown --to plain -o README.txt
pandoc docs/Quickstart.md --pdf-engine=xelatex -o docs/Quickstart.pdf
