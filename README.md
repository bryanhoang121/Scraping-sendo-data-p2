All data will be in intext format because all data on e-commerce platforms are text.
I added reset_table function to reset table everytime we run code (you can control it by adjust True or False in the main file)
All product information will be save in tupe instead of list because Postgres doesn't accept list. Beside that everything must be in double quotes (") which accepted by postgres
I already hided config file which contains private data (DB_HOST= yourlocalhost, DB_DATABASE = postgres (I put 'postgres' hehe),DB_USERNAME = your username on postgres, DB_PASSWORD= your password on postgres, DB_PORT = your port number on postgres)
Other files I hided just output files, I want to make it clean.