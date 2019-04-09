from django.contrib import admin
from django.contrib.admin import register
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserProfile, CustomerAddress, CustomerPhone, CustomerMail, CustomerWebSite, Customer


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserProfileInline, )


class AddressInline(admin.TabularInline):
    pass


class CustomerAddressInline(AddressInline):
    model = CustomerAddress
    extra = 1


class PhoneInline(admin.TabularInline):
    pass


class CustomerPhoneInline(PhoneInline):
    model = CustomerPhone
    extra = 1


class EmailInline(admin.TabularInline):
    pass


class CustomerEmailInline(EmailInline):
    model = CustomerMail
    extra = 1


class WebSiteInline(admin.TabularInline):
    pass


class CustomerWebSiteInline(WebSiteInline):
    model = CustomerWebSite
    extra = 1


@register(Customer)
class CompanyAdmin(admin.ModelAdmin):
    inlines = (CustomerAddressInline, CustomerPhoneInline, CustomerEmailInline, CustomerWebSiteInline)
