from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    mobile_phone = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'Name: %s %s; Email: %s; Mobile Phone: %s; Sex: %s' % (self.name, self.surname, self.email,
                                                                       self.mobile_phone, self.sex)
