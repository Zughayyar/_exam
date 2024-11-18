from django.db import models
from register.models import User

class PieManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        entered_pie = Pie.objects.filter(name = data['name'])
        if len(entered_pie) != 0:
            errors['name_duplicate'] = "Pie name should be unique!"
            return errors
        if len(data['name']) == 0:
            errors['name_len'] = "Please add Pie name!"
        if len(data['filing']) == 0:
            errors['filing'] = "Please Include Filing!"
        return errors


class Pie(models.Model):
    name = models.CharField(max_length=255)
    filing = models.CharField(max_length=255)
    crust = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    baker = models.ForeignKey(User, related_name="pies", on_delete=models.DO_NOTHING)
    objects = PieManager()
    voters = models.ManyToManyField(User, related_name="voted_pie")

def get_user_by_email(email):
    return User.objects.filter(email=email)

def get_all_pies():
    return Pie.objects.all()

def get_pie_by_id(id):
    return Pie.objects.get(id=id)

def create_pie(data, user):
    Pie.objects.create(
        name = data['name'], 
        filing = data['filing'],
        crust = data['crust'],
        baker = user
    )

def delete_pie(data, user):
    pie_id = data['pie_id']
    pie = Pie.objects.get(id = pie_id)
    if pie.baker == user:
        pie.delete()

def edit_pie(id, data):
    pie = Pie.objects.get(id=id)
    pie.name = data['name']
    pie.filing = data['filing']
    pie.crust = data['crust']
    pie.save()

def vote_user_pie(data, user):
    pie = get_pie_by_id(data['pie_id'])
    pie.voters.add(user)

def remove_vote_user_pie(data, user):
    pie = get_pie_by_id(data['pie_id'])
    pie.voters.remove(user)