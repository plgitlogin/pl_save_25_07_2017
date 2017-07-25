# premierlangage
A first computer langage learning tool



## Installation 


mkdir server/serverpl/serverpl/tmp 
mkdir server/serverpl/serverpl/log
chmod g+w server/serverpl/serverpl/log server/serverpl/serverpl/tmp server/serverpl/db.sqlite3 
chown www-data:www-data server/serverpl/serverpl/log server/serverpl/serverpl/tmp server/serverpl/db.sqlite3 


python3 manage.py migrate 
python3 manage.py createsuperuser
python3 manage.py 

