from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    # email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=10, null=False, db_index=True)
    username = models.CharField(
       
        max_length=150,
        unique=False,
       
        # error_messages={"unique": _("A user with that username already exists."),},
    )
    # REQUIRED_FIELDS = ['phone_number']
    USERNAME_FIELD = 'phone_number'
    # password = models.CharField(type=)

    class Meta:
        db_table = "gmsUsers"


class FamilyHeadAddresses(models.Model):
    family_head = models.ForeignKey(MyUser, on_delete = models.CASCADE, primary_key=True)
    house_number = models.CharField(null=False, unique=True, max_length=20)
    address = models.CharField(null=False, unique=True, max_length=50)

    class Meta:
        db_table = "family_head_address"


class FamilyHeadtoMember(models.Model):
    family_head = models.CharField(null=False)
    family_members = models.CharField(unique=True, null=False)
    
 
    class Meta:
        db_table = "head_to_member_relation"