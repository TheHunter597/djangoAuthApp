sleep 5
python manage.py makemigrations
sleep 5
echo "migrations done"
python manage.py migrate
sleep 5
echo "migrate done"
python manage.py create_default_interests
echo "create_default_interests done"
python manage.py runserver 0.0.0.0:8000
