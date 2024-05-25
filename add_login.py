import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
user = User.objects.create_user('admin', 'admin', 'admin')
user.save()
