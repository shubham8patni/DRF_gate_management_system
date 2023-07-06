from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class MyUser(AbstractUser):
    # email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=10, null=False, db_index=True)
    aadhar_number = models.CharField(max_length=12)
    
    username = models.CharField(
       
        max_length=150,
        unique=False,
       
        # error_messages={"unique": _("A user with that username already exists."),},
    )
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'phone_number'
    # password = models.CharField(type=)

    class Meta:
        db_table = "gmsUsers"


class FamilyHeadAddresses(models.Model):
    family_head = models.ForeignKey(MyUser, on_delete = models.CASCADE, primary_key=True, to_field='phone_number')
    house_number = models.CharField(null=False, unique=True, max_length=10)
    floor_number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], null=False, unique=True)
    complete_address = models.CharField(null=False, unique=True, max_length=50)

    class Meta:
        db_table = "family_head_address"


class FamilyHeadtoMember(models.Model):
    family_head = models.ForeignKey(MyUser, null=False, on_delete= models.CASCADE, related_name= 'family_head', to_field='phone_number')
    family_members = models.ForeignKey(MyUser, null=False, on_delete= models.CASCADE, related_name= 'family_member', to_field='phone_number')
    
 
    class Meta:
        db_table = "head_to_member_relation"