#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
# adicione linhas abaixo
python manage.py makemigrations accounts
python manage.py makemigrations ranking
python manage.py migrate
python manage.py loaddata bandecos

# create superuser if missing
cat <<EOF | python manage.py shell
import os
from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists() or \
    User.objects.create_superuser(os.environ["DJANGO_SUPERUSER_USERNAME"], os.environ["DJANGO_SUPERUSER_EMAIL"], os.environ["DJANGO_SUPERUSER_PASSWORD"])
EOF
