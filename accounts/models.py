from django.db import models
from django.contrib.auth.models import User


# class User(AbstractBaseUser):
#     photo = models.ImageField()
#     data_of_brith = models.DateTimeField()
#     address = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,)
    photo = models.ImageField(upload_to='users/',blank=True,null=True)
    data_of_birth = models.DateField(blank=True,null=True)
    def __str__(self):
        return f"{self.user.username} profili"