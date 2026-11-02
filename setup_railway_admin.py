import os
import sys

# Setup Django environment
os.environ['DATABASE_URL'] = "postgresql://postgres:omAopoIwisNQMXjOrhSmljZXiMBhSfOE@reseau.proxy.rlwy.net:16743/railway"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dokan_backend.settings')

import django
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import UserProfile

def setup_superadmin():
    print("Connected to Railway PostgreSQL via Django successfully.")
    
    # 1. List existing users
    existing_users = User.objects.all()
    print(f"Total existing users in database: {existing_users.count()}")
    for u in existing_users:
        profile = getattr(u, 'profile', None)
        role = profile.role if profile else 'no profile'
        print(f" - ID: {u.id}, Username: '{u.username}', Email: '{u.email}', Superuser: {u.is_superuser}, Staff: {u.is_staff}, Active: {u.is_active}, Role: {role}")

    # 2. Desired superadmin credentials
    username = "admin"
    email = "admin@gmail.com"
    password = "admin123"

    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.filter(email=email).first()

    if user:
        print(f"\nUpdating existing user '{user.username}' (ID: {user.id}) to Super Admin...")
        user.username = username
        user.email = email
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
    else:
        print(f"\nCreating new Super Admin '{username}'...")
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

    # 3. Update or create UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'developer'  # highest privilege
    profile.full_name = 'Super Admin'
    profile.is_active = True
    profile.save()

    # 4. Generate Auth Token
    token, _ = Token.objects.get_or_create(user=user)

    print("\n==========================================")
    print(" SUPER ADMIN CREATED/UPDATED SUCCESSFULLY ")
    print("==========================================")
    print(f"Username : {username}")
    print(f"Email    : {email}")
    print(f"Password : {password}")
    print(f"Role     : {profile.role} (Developer - Full Access)")
    print(f"Token    : {token.key}")
    print("==========================================")

if __name__ == '__main__':
    setup_superadmin()
