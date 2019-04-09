# code: utf-8
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Django User model has been overridden due to create custom user model.
    With doing this, using email addresses as user name.
    """
    username = models.CharField(verbose_name=_("User Name"), max_length=64, null=True, blank=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserProfile(models.Model):
    """
    User Profile
    """
    user = models.OneToOneField(User, verbose_name=_("User"), null=True, blank=True,
                                related_name='profile', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("Title"), max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


# COMPANY RELATED ABSTRACT MODELS

class CompanyCommon(models.Model):
    """
    Company Abstract Model
    """
    company_description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    company_title = models.CharField(max_length=256, verbose_name=_("Company Title"))
    tax_office = models.CharField(max_length=32, verbose_name=_("Tax Office"))
    tax_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                                  verbose_name=_("Tax ID"), null=True, blank=True)
    citizen_id = models.CharField(max_length=11, validators=[MinLengthValidator(11)],
                                  verbose_name=_("Social SecID"), null=True, blank=True)

    class Meta:
        abstract = True


class Address(models.Model):
    """
    Address Abstract Model
    """
    street = models.CharField(max_length=128, verbose_name=_("Street"), null=True, blank=True)
    building = models.CharField(max_length=16, verbose_name=_("Door Nr"), null=True, blank=True)
    county = models.CharField(max_length=16, verbose_name=_("Province"))
    city = models.CharField(max_length=16, verbose_name=_("City"))
    postcode = models.CharField(max_length=5, validators=[MinLengthValidator(5)], verbose_name=_("Postal Code"))
    country = models.CharField(max_length=16, verbose_name=_("Country"), default='Turkey', editable=False)

    class Meta:
        abstract = True


class Phone(models.Model):
    """
    Phone Abstract Model
    """
    phone_number_types = (
        (0, _("Mobile")), (1, _("Work")), (2, _("Fax")), (3, _("Home"))
    )

    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                             help_text="5xxxxxxxxx", verbose_name="Phone Nr")
    type = models.PositiveSmallIntegerField(choices=phone_number_types, verbose_name=_("Type"))
    extension = models.CharField(max_length=8, verbose_name=_("Ext."), null=True, blank=True)
    default = models.BooleanField(default=False, verbose_name=_("Primary"))

    def __str__(self):
        part4, rest = self.phone[-2], self.phone[:-2]
        part3, rest = rest[-2], rest[:-2]
        part2, rest = rest[-3], rest[:-3]
        part1 = rest
        return "0 {}".format(" ".join((part1, part2, part3, part4)))

    class Meta:
        abstract = True


class Email(models.Model):
    """
    E-mail Abstract Model
    """
    mail = models.EmailField(verbose_name=_("E-mail"))
    default = models.BooleanField(default=False, verbose_name=_("Primary"))

    class Meta:
        abstract = True


class WebSite(models.Model):
    """
    Web Site Abstract Model
    """
    website = models.TextField(verbose_name=_("Web Site Address"))

    class Meta:
        abstract = True


# END OF ABSTRACT MODELS

# Customer Models
class Customer(CompanyCommon):
    """
    Customer model extended with CompanyCommon abstract model
    """
    headquarter = models.ForeignKey('self', verbose_name=_("Headquarter"), null=True, blank=True,
                                    on_delete=models.CASCADE)
    lead = models.BooleanField(verbose_name=_("Lead"), default=False)
    staff = models.ManyToManyField(User, related_name="customer", verbose_name=_("Staff"))

    def __str__(self):
        tax_number = self.tax_number if self.tax_number else self.citizen_id if self.citizen_id else ""
        return " - ".join((self.company_title, tax_number))

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class CustomerAddress(Address):
    """
    CustomerAddress model extended with Address abstract model
    """
    company = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="address", verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Customer Address")
        verbose_name_plural = _("Customer Addresses")


class CustomerPhone(Phone):
    """
    CustomerPhone model extended with Phone abstract model
    """
    company = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="phone", verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Customer Phone")
        verbose_name_plural = _("Customer Phones")


class CustomerMail(Email):
    """
    CustomerMail model extended with Email abstract model
    """
    company = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="email", verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Customer E-mail")
        verbose_name_plural = _("Customer E-mails")


class CustomerWebSite(WebSite):
    """
    CustomerWebSite model extended with WebSite abstract model
    """
    company = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="website", verbose_name=_("Customer"))

    class Meta:
        verbose_name = _("Customer Web Site")
        verbose_name_plural = _("Customer Web Sites")
