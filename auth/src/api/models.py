from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(
        max_length=100, unique=True, null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    zipcode = models.CharField(max_length=7, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    telephone = models.CharField(max_length=15, null=False, blank=False)
    status = models.CharField(max_length=1, null=False, blank=False, default=0)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class UserUtil(models.Model):
    token = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_utils'
