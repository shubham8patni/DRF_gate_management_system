from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, FamilyHeadtoMember

# Register your models here.

class MyUserAdmin(UserAdmin):
    
    model = MyUser
    list_display = ('phone_number', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    fieldsets = (
        ('Credentials', {'fields': ('phone_number', 'password')}),
        ('User Info', {'fields': ('first_name', 'last_name')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
        ('Pernissions', {'fields': ('is_staff','is_active')}),
        ('Groups and Permissions', {'fields' : ('groups','user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'groups', 'is_staff', 'is_active'),
        }),
    )
    
    search_fields = ('phone_number',)
    ordering=('date_joined',)


# class FamilyRelationAdmin(UserAdmin):
    
#     model = FamilyHeadtoMember
#     list_display = ('family_head', 'family_members')

#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('family_head', 'family_members'),
#     #     }),
#     # )




admin.site.register(MyUser, MyUserAdmin)
# admin.site.register(FamilyHeadtoMember,FamilyRelationAdmin )

# admin.site.register(MyUser)