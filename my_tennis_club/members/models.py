from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile_phone = models.CharField(max_length=20)

    def __str__(self):
        return f'Name: %s %s; Email: %s;' % (self.name, self.surname, self.email)
