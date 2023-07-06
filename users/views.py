from django.shortcuts import render
from rest_framework import generics, views
from .serializers import UserRegisterSerializer, UserCompleteProfileSerializer, AddressVerificationSerializer, MyUserSerializer, UnverifiedView, UserLoginSerializer, UserProfileSerializer, UserProfileInfoSerializer, UserProfileCreateSerializer, UserStateSerializer, AddFamilyMemberSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser, FamilyHeadAddresses
from django.contrib.auth.models import Group
from .helper_function import password_generate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from .signals import member_added


# ========================================FOUR VIEW METHODS========================================
# class UserCreate(APIView): #generics.CreateAPIView
#     def post(self, request):
#         serializer_class = UserCreateSerializer
#         return Response(serializer_class.data)

# class UserCreate(mixins.CreateModelMixin, generics.GenericAPIView): #generics.CreateAPIView
#     serializer_class = UserCreateSerializer

#     def post(self, request):
#         return self.create(request)
    
# @api_view(['POST'])
# def UserCreatef(request):
#     serializer_class = UserCreateSerializer
#     return Response(serializer_class.data)

# @api_view(['POST'])
# def UserCreatef(request):
#     serializer_class = UserCreateSerializer
#     return Response(serializer_class.data)

# class UserCompleteProfile(generics.CreateAPIView): #generics.CreateAPIView
#     serializer_class = UserCompleteProfileSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer_class = UserCompleteProfileSerializer(data=request.data)
#             if serializer_class.is_valid():
#                 serializer_class.save()
#                 user = MyUser.objects.get(phone_number = serializer_class.data['phone_number'])
#                 # refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'status' : 200,
#                     'data': serializer_class.data,
#                     # 'refresh' : str(refresh),
#                     # 'access' : str(refresh.access_token),
#                     'message' : "Profile Updated Successfull!",

#                 })
            
#             return Response({
#                     'status' : 400,
#                     'message' : "Something Went Wrong!",
#                     'data' : serializer_class.errors,

#                 })
#         except Exception as e:
#             print(e)
#             return Response({
#                 'error': e,
#                              })


class UserRegister(generics.CreateAPIView): #generics.CreateAPIView
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer_class = UserRegisterSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                user = MyUser.objects.get(phone_number = serializer_class.data['phone_number'])
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status' : 200,
                    'data': serializer_class.data,
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                    'message' : "Registration Successfull!",

                })
            
            return Response({
                    'status' : 400,
                    'message' : "Something Went Wrong!",
                    'data' : serializer_class.errors,

                })
        except Exception as e:
            print(e)
            return Response({
                'error': e,
                             })

class UserCompleteProfile(generics.UpdateAPIView): #generics.CreateAPIView
    serializer_class = UserCompleteProfileSerializer
    queryset = MyUser.objects.all()
    http_method_names = ['patch']
    lookup_field = 'phone_number'
    
    
class AddressVerification(generics.CreateAPIView):
    serializer_class = AddressVerificationSerializer
    queryset = FamilyHeadAddresses.objects.all()

    # lookup_field = 'family'
    # def post(self, request):
    #     serializer_class = AddressVerificationSerializer(data=request.data)
    #     if serializer_class.is_valid():
    #         serializer_class.save()
    #         return Response({
    #             'status' : 201,
    #             'message' : "Address Details Updated! verification Pending"
    #         })
    #     else:
    #         return Response({
    #             'status' : 400,
    #             'message' : "Something Went Wrong!",
    #             'data' : serializer_class.errors,
    #         })


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        try:
            if serializer_class.is_valid():
                phone_number = serializer_class.data['phone_number']
                password = serializer_class.data['password']
                # db_info = MyUser.objects.get(phone_number = serializer_class.data['phone_number'])

                user_db_info = authenticate(phone_number = phone_number, password= password)
                if user_db_info is None:
                    return Response({
                        'status' : 400,
                        'message' : "Invalid Credentials!",
                        'data' : {},

                    })
                
                refresh = RefreshToken.for_user(user_db_info)
                return Response({
                    'status' : 200,
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                })
            return Response({
                        'status' : 400,
                        'message' : "Invalid Credentials!",
                    })
        except Exception as e:
            print(e)
            return Response({
                'error': e,
                             })
                

class UserProfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    serializer_class = UserProfileSerializer
    lookup_field = "phone_number"
    # def get_queryset(self):
    #     return MyUser.objects.filter(phone_number = self.kwargs['phone_number'])
    def get(self, request, phone_number):
        if (request.user.groups.filter(name='Verified Residents').exists() and request.user.groups.filter(name='Family Head').exists()) or (request.user.groups.filter(name='Management').exists()):
            user1 = MyUser.objects.get(phone_number = phone_number)
            serializer_class = MyUserSerializer(user1) #FamilyHeadViewSerializer(user1)
            print(serializer_class.data, "========================")
            return Response(serializer_class.data)
        elif (request.user.phone_number == phone_number):
            user1 = MyUser.objects.get(phone_number = phone_number)
            serializer_class = UserProfileSerializer(user1)
            return Response(serializer_class.data)
        return Response({
                        'status' : 400,
                        'message' : "Invalid Command!",
                    })


class AddFamilyMembers(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddFamilyMemberSerializer

    def post(self, request):
        print(request.user.groups.filter(name = "Verified Residents").exists() , request.user.groups.filter(name = "Family Head").exists())
        if request.user.groups.filter(name = "Verified Residents").exists() and request.user.groups.filter(name = "Family Head").exists():
            family_head_phone_number = request.data['family_head_phone_number']
            user_info = request.data
            password = password_generate(user_info['phone_number'], user_info['first_name'])
            group_info = Group.objects.get(name = "Verified Residents")
            register_user = {"phone_number" : user_info['phone_number'], "password" : password}
            register_user_serializer = UserRegisterSerializer(data = register_user)
            
            if register_user_serializer.is_valid():
                register_user_serializer.save()
            else:
                return Response({"status" : 401,
                            "message":"Something Went Wrong!",
                            })
            member_added.send(sender=MyUser, instance=register_user_serializer.data, group = group_info.id, family_head = family_head_phone_number)
            # reg_user = MyUser.objects.get(phone_number = register_user['phone_number'])
            # reg_user.groups.add(group_info.id)
            # profile_complete = {"groups": group_info.id, "first_name" : user_info['first_name'], "last_name" : user_info['last_name'], "aadhar_number" : user_info["aadhar_number"]}
            
            # complete_profile_serializer = UserCompleteProfileSerializer(data = profile_complete)
            try:
                complete_profile_info = MyUser.objects.filter(phone_number =register_user['phone_number']).update(first_name = user_info['first_name'], last_name = user_info['last_name'], aadhar_number = user_info["aadhar_number"])
                # complete_profile_serializer.is_valid()
                # complete_profile_serializer.save()
            except Exception as e:
                print(str(e))
                return Response({"status" : 401,
                            "message":"Something Went Wrong!",
                            "error" : str(e)
                            })
            # add_member = Signal(instance=register_user_serializer, group = group_info.id, family_head = family_head_phone_number)
            # member_aaded(sender=MyUser, instance=register_user_serializer, group = group_info.id, family_head = family_head_phone_number)
            return Response({"status" : 200,
                            "message":"User Created Successfully!",
                            "data" : f"{complete_profile_info}, {register_user_serializer.data}",
                            "group" : str(group_info)
                            })
        return Response({"status" : 401,
                            "message":"Something Went Wrong!",
                            })

            


# class FamilyMembersInfo(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     # authentication_classes = [JWTAuthentication]
#     serializer_class = FamilyMembersInfoSerializer
#     lookup_field = "phone_number"
#     # def get_queryset(self):
#     #     return MyUser.objects.filter(phone_number = self.kwargs['phone_number'])
#     def get(self, request, phone_number):
#         if (request.user.groups.filter(name='Verified Residents').exists() and request.user.groups.filter(name='Family Head').exists()) or (request.user.groups.filter(name='Management').exists()):
#             user1 = MyUser.objects.get(phone_number = phone_number)
#             serializer_class = MyUserSerializer(user1) #FamilyHeadViewSerializer(user1)
#             print(serializer_class.data, "========================")
#             return Response(serializer_class.data)
#         return Response({
#                         'status' : 400,
#                         'message' : "Invalid Command!",
#                     })
    
class UnverifiedUsers(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnverifiedView
    lookup_field = "type" #phone_number"

    # def get_queryset(self):
    #     if self.kwargs['type'] == 'residents':
    #         Gname = 'Unverified Residents'
    #     elif self.kwargs['type'] == 'guards':
    #         Gname = 'Unverified Guards'
    #     else: 
    #         return "Error"
    #     group = Group.objects.get(name=Gname)
    #     return MyUser.objects.filter( groups = group)

    def get(self, request, type):
        if request.user.groups.filter(name='Management').exists():
            print(request.user)
            if type == 'residents':
                Gname = 'Unverified Residents'
            elif type == 'guards':
                Gname = 'Unverified Guards'
            else: 
                return "Error"
            group = Group.objects.get(name=Gname)
            queryset =  MyUser.objects.filter( groups = group)
            serializer_class = UnverifiedView(queryset, many = True)
            return Response(serializer_class.data)
        return Response({
            'status' : 402,
            "message" : "Something Went Wrong!"
        })


# class VerifyResidents(generics.CreateAPIView):
class VerifyResidents(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    group_name_updated = 'Verified Residents'
    def patch(self, request): #, phone_number
        if request.user.groups.filter(name='Management').exists():
            # print(request.data['phone_number'], request.user, request.user)
            user = MyUser.objects.filter(phone_number = request.data['phone_number'])
            group_name = Group.objects.get(name = self.group_name_updated)
            group_remove = Group.objects.get(name = "Unverified Residents")
            # print(user[0], group_remove[0], group_name[0])
            user[0].groups.add(group_name)
            user[0].groups.remove(group_remove)
            if user[0].groups.filter(name='Verified Residents').exists():
                return Response({
                    'status' : 201,
                    'message': "Resident Successfully Verified"
                    
                })
            
            return Response({
                    'status' : 401,
                    'message': "Something went wrong"
                    
                })
        return Response({
                    'status' : 401,
                    'message': "Invalid Operation!"
                    
                })
    


# class VerifyResidents(generics.CreateAPIView):
class VerifyGuards(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    group_name_updated = 'Verified Residents'
    def patch(self, request): #, phone_number
        if request.user.groups.filter(name='Management').exists():
            print(request.data['phone_number'], request.user, request.user)
            user = MyUser.objects.filter(phone_number = request.data['phone_number'])
            group_name = Group.objects.get(name = self.group_name_updated)
            group_remove = Group.objects.get(name = "Unverified Residents")
            # print(user[0], group_remove[0], group_name[0])
            user[0].groups.add(group_name)
            user[0].groups.remove(group_remove)
            if user[0].groups.filter(name='Verified Residents').exists():
                return Response({
                    'status' : 201,
                    'message': "Resident Successfully Verified"
                    
                })
            
            return Response({
                    'status' : 401,
                    'message': "Something went wrong"
                    
                })
        return Response({
                    'status' : 401,
                    'message': "Invalid Operation!"
                    
                })
    

# class AddFamilyMembers()




###################################SORTED###################################
class Users(APIView):

    def get(self, request):
        try:    
            # request.user
            user = request.user # request provides phone number/pk of user making the request
            # print(request.user)
            serializer_class = UserProfileInfoSerializer(user) # using user phone number the serializer fetches information and serializes it for response
            return Response({
                'status' : 200,
                'body' : serializer_class.data # .data gets the data transformed for view i.e. JSON
                }) 
        except Exception as e:
            print(e)
            return Response({
                'error' : str(e),
            })

        
    def post(self, request):
        serializer_class = UserProfileCreateSerializer(data = request.data)
        try :
            if serializer_class.is_valid():
                serializer_class.save()
                user = MyUser.objects.get(phone_number = serializer_class.data['phone_number'])
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    'status' : 200,
                    'refresh_token' : str(refresh_token),
                    'access_token' : str(refresh_token.access_token),
                    'message' : "Registration Successful!"
                })
            return Response({
                    'status' : 401,
                    'message' : "Something Went Wrong!"
                })
        except Exception as e:
            print(e)
            return Response({
                'error' : e,
            })
        
    get.permission_classes = [IsAuthenticated]


class UserState(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, type):
        if type == "unverified_guards":
            group_name = "Unverified Guards"
        elif type == "unverified_residents":
            group_name = "Unverified Residents"
        elif type == "verified_residents":
            group_name = "Verified Residents"
        elif type == "verified_guards":
            group_name = "Verified Guards"
        else:
            return Response({
                'status' : 404,
                "message" : "Invalid Command!"
            })
        group_id = Group.objects.get(name = group_name)
        query_set = MyUser.objects.filter(groups = group_id)
        print(query_set.values())
        serializer_class = UserProfileInfoSerializer(query_set, many = True)
        return Response({
            'status' : 200,
            "data" : serializer_class.data
        })

    def patch(self, request):
        if request.data:
            user_phone = request.data['phone_number']
            print(user_phone)
            user_profile = MyUser.objects.get(phone_number = user_phone)
            current_group_info = Group.objects.get(user = user_profile.id)
            # print(type(current_group_info), current_group_info.name, current_group_info.id, str(current_group_info),"-============")
            if str(current_group_info) == "Unverified Guards":
                updated_group = Group.objects.get(name = "Verified Guards")
            elif str(current_group_info) == "Unverified Residents":
                updated_group = Group.objects.get(name = "Verified Residents")
            else:
                print("Unverified Residents", current_group_info )
                return Response({
                'status' : 404,
                "message" : "Invalid Command!",
            })
            user_profile.groups.add(updated_group)
            user_profile.groups.remove(current_group_info)
            if user_profile.groups.filter(name=updated_group).exists():
                return Response({
                    'status' : 201,
                    'message': f"User Successfully Verified to {updated_group}"
                })
            else:
                return Response({
                'status' : 404,
                "message" : "Something Went Wrong!"
            })

        return Response({
                'status' : 404,
                "message" : "Invalid Operation!"
            })

    # get.permission_classes = [IsAuthenticated]


class adminProfileView(APIView):

    def get(self, request, phone_number):
        try:
            if request.user.groups.filter(name = "Management").exists():
                user = MyUser.objects.get(phone_number = phone_number)
                serializer_class = UserProfileInfoSerializer(user)
                return Response({
                    'status' : 200,
                    'body' : serializer_class.data # .data gets the data transformed for view i.e. JSON
                    })   
            else:
                return Response({
                    'status' : 401,
                    'body' : "Invalid Operation!" # .data gets the data transformed for view i.e. JSON
                    })   
            
        except Exception as e:
            return Response({
                'error' : str(e)
            })

# class AdminView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, type):
#         if type == "unverified_guards":
#             group_name = "Unverified Guards"
#         elif type == "unverified_residents":
#             group_name = "Unverified Residents"
#         elif type == "verified_residents":
#             group_name = "Verified Residents"
#         elif type == "verified_guards":
#             group_name = "Verified Guards"
#         else:
#             return Response({
#                 'status' : 404,
#                 "message" : "Invalid Command!"
#             })
#         group_id = Group.objects.get(name = group_name)
#         query_set = MyUser.objects.filter(groups = group_id)
#         print(query_set.values())
#         serializer_class = UserProfileInfoSerializer(query_set, many = True)
#         return Response({
#             'status' : 200,
#             "data" : serializer_class.data
#         })