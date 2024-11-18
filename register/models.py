from django.db import models
import bcrypt, re # type: ignore


class UserManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        current_email = get_user_by_email(data['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(current_email) > 0:
            errors['current_email'] = "This mail already exists!"
        if len(data['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters!"
        if len(data['last_name']) < 2:
            errors['last_name'] = "First Name should be at least 2 characters!"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "E-mail address should be valid!"
        if len(data['password']) < 8:
            errors['password_len'] = "Password should be at least 8 characters!"
        if data['re_password'] != data['password'] and len(data['password']) >= 8:
            errors['password_match'] = "Password not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def create_user(data):
    password =data['password']
    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        password = hashed_pwd
    )

def is_user_exist(data):
    users = User.objects.filter(email = data['email'])
    if len(users) == 0:
        return False
    else:
        return True

def get_user_by_email(email):
    return User.objects.filter(email=email)

def is_password_match(entered_email, entered_password):
    user = User.objects.filter(email = entered_email)
    password = user[0].password
    return bcrypt.checkpw(entered_password.encode() , password.encode())

def check_login(data):
    entered_email = data['email']
    entered_password = data['password']
    return is_password_match(entered_email,entered_password)
