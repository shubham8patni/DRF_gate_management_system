from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import MyUser
from django.contrib.auth.models import Group


class UserCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, error_messages = {'required':'email necessary'})
    class Meta:
        model = MyUser
        fields = ("groups", "first_name", "last_name", "phone_number", "password")
        extra_kwargs = {'password' : {'write_only' : True},
                        'phone_number' : {'error_messages' : {'required':'phone number necessary'}}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        group_name = validated_data.pop('groups', None)
        group_name = group_name[0].id
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        print(instance, group_name)
        instance.save()
        # unverified_group = Group.objects.get(name="unverified_cat")
        instance.groups.add(group_name)
        return instance
    
class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number", "groups") #"groups", 
        


class UnverifiedView(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number") #"groups", 
        


###################################SORTED###################################

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name",)

class UserProfileInfoSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many = True)
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number", "groups")


class UserProfileCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, error_messages = {'required':'email necessary'})
    class Meta:
        model = MyUser
        fields = ("groups", "first_name", "last_name", "phone_number", "password")
        extra_kwargs = {'password' : {'write_only' : True},
                        'phone_number' : {'error_messages' : {'required':'phone number necessary'}}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        group_name = validated_data.pop('groups', None)
        group_name = group_name[0].id
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        print(instance, group_name)
        instance.save()
        # unverified_group = Group.objects.get(name="unverified_cat")
        instance.groups.add(group_name)
        return instance


class UserStateSerializer(serializers.ModelSerializer):
    current_category = GroupSerializer(many = True)
    to_update_category = GroupSerializer(many = True)
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number", "current_category", "to_update_category")