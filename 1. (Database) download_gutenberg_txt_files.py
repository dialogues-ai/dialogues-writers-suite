# Get Gutenberg .txt files
# 

for i in {1..1000}; do echo $i; wget "http://www.gutenberg.org/files/${i}/${i}.txt"; done