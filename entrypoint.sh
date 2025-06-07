#!/bin/sh

echo "🔁 Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "👤 Creating normal user if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DJANGO_NORMAL_USERNAME}').exists():
    User.objects.create_user(
        username='${DJANGO_NORMAL_USERNAME}',
        password='${DJANGO_NORMAL_PASSWORD}',
        email='user@example.com'
    )
END

if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚀 Starting Gunicorn for production..."
    gunicorn employee_management_system.wsgi:application --bind 0.0.0.0:8000 --workers 4
else
    echo "🚀 Starting Django development server..."
    python manage.py runserver 0.0.0.0:8000
fi
