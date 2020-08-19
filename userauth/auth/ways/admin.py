from django.contrib import admin
from ways.models import bookshaaaa , CustomUser , auditentry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm , CustomUserChangeForm
#Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    #list_display = ('username','email',)
class auditentryadmin(admin.ModelAdmin):
    list_display = ('user_name','action','ip','time')
    search_fields = ('user_name',)


admin.site.register(bookshaaaa)
admin.site.register(CustomUser)
admin.site.register(auditentry,auditentryadmin)
#admin.site.register(CustomUser,CustomUserAdmin)
#admin.site.register(CustomUser,UserAdmin)