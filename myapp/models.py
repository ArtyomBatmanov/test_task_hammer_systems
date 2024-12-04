from django.db import models
import random
import string


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    activated_invite_code = models.CharField(max_length=6, blank=True, null=True)

    def generate_auth_code(self):
        self.auth_code = str(random.randint(1000, 9999))

    def generate_invite_code(self):
        self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
