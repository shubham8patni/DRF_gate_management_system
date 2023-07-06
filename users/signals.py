from django.dispatch import receiver
from .models import MyUser, FamilyHeadtoMember
from django.dispatch import Signal
# from .serializers import MemberRelationSerializer
from rest_framework.response import Response
from django.contrib.auth.models import Group

member_added = Signal()

@receiver(member_added)
def member_added_handler(sender, instance, *args, **kwargs):
    print(instance, "============", kwargs['group'])
    user_new = MyUser.objects.get(phone_number = instance['phone_number'])
    user_new.groups.add(kwargs['group'])
    member_group = Group.objects.get(name = "Family Member")
    user_new.groups.add(member_group.id)
    famil_head = MyUser.objects.get(phone_number = kwargs['family_head'])
    try:
        FamilyHeadtoMember.objects.create(family_head =famil_head, family_members= user_new)
    except Exception as e:
        print(str(e))
        return Response({"status" : 401,
                            "message":"Something Went Wrong!",
                            "error" : str(e)
                            })
    return True
    


