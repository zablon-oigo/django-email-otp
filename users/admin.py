from django.contrib import admin
from .forms import CustomerUserChangeForm,CustomuserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
class CutomUserAdmin(UserAdmin):
    add_form=CustomuserCreationForm
    form=CustomerUserChangeForm
    model=CustomUser
    list_display=["email","is_staff","is_active"]
    list_filter=["email","is_staff","is_active"]
    fieldsets=(
        (None,{"fields":("email","password")}),
        ("Permissions",{"fields":("is_staff","is_active","groups","user_permissions")}),

    )
    add_fieldsets=(
        (None,{
            "classes":("wide",),
            "fields":(
                "email","password1","password2","is_staff",
                "is_active","groups","user_permissions"
            ) 
        }
        ),
    )
    search_fields=("email",)
    ordering=("email",)
admin.site.register(CustomUser,CutomUserAdmin)

