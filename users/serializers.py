from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import MyUser, FamilyHeadAddresses, FamilyHeadtoMember
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from .helper_function import aadharNumVerify
from django.core.exceptions import ValidationError

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name",)

class UserRegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, error_messages = {'required':'email necessary'})
    # groups = serializers.ChoiceField(choices=['Unverified guards', 'Unverified Residents'])
    class Meta:
        model = MyUser
        fields = ("phone_number", "password")
        extra_kwargs = {'password' : {'write_only' : True},
                        'phone_number' : {'error_messages' : {'required':'phone number necessary'}}}
        

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # group_name = validated_data.pop('groups', None)
        # group_name = group_name[0].id
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        # print(instance, group_name)
        instance.save()
        # unverified_group = Group.objects.get(name="unverified_cat")
        # instance.groups.add(group_name)
        return instance

class UserCompleteProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True, error_messages = {'required':'email necessary'})
    # groups = serializers.ChoiceField(choices=['Unverified Guards', 'Unverified Residents'])
    # aadhar_document = serializers.FileField()
    
    class Meta:
        model = MyUser
        fields = ("groups", "first_name", "last_name", "aadhar_number")#, "aadhar_document",   )
        extra_kwargs = {'password' : {'write_only' : True},
                        'phone_number' : {'error_messages' : {'required':'phone number necessary'}}}

    # uncomment aadhar verification
    # def validate(self, data):
    #     aadhar = data.get('aadhar_number')
    #     if aadharNumVerify(aadhar):
    #         return True
    #     else:
    #         raise Exception("An unexpected error occurred.")

class AddressVerificationSerializer(serializers.ModelSerializer):
    # house_no = serializers.CharField(max_length = 10, allow_null = False)
    floor_number = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], allow_null = False)
    # complete_address = serializers.CharField(max_length = 200, allow_null = False)
    # legal_document = serializers.FileField()
    class Meta:
        model = FamilyHeadAddresses
        fields = ['family_head', 'house_number', "floor_number", "complete_address"]#, 'legal_document']

    def create(self, validated_data):
        phone_number = validated_data.pop('family_head')
        user = MyUser.objects.get(phone_number=phone_number)
        validated_data['family_head'] = user
        return super().create(validated_data)
    
class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class MyUserSerializer(serializers.ModelSerializer):
    family_head_addresses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'phone_number', 'aadhar_number', 'username', 'family_head_addresses')
        read_only_fields = ('family_head_addresses',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        qs = instance.phone_number
        print(qs)
        qs2 = FamilyHeadAddresses.objects.get(family_head = qs)
        print(qs2.house_number, qs2.floor_number, qs2.complete_address)
        address = {"house_number" : qs2.house_number, "floor_number" : qs2.floor_number, "complete_address" : qs2.complete_address}
        data['family_head_addresses'] = address
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number", "aadhar_number", "groups") #"groups", 
        

class AddFamilyMemberSerializer(serializers.ModelSerializer):
    family_head_phone_number = serializers.CharField(max_length = 10)
    class Meta:
        model = MyUser
        fields = ("family_head_phone_number", "phone_number", "first_name", "last_name", "aadhar_number")



class UnverifiedView(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone_number") #"groups", 
        


class MemberRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyHeadtoMember
        fields = ("family_head", "family_members")



###################################SORTED###################################



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