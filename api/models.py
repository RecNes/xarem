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


class Customer(models.Model):
    """
    Customer model
    """
    phone_number_types = (
        (0, _("Mobile")), (1, _("Work")), (2, _("Fax")), (3, _("Home"))
    )

    name = models.CharField(max_length=256, verbose_name=_("Name"))
    company_title = models.CharField(max_length=256, verbose_name=_("Company Title"))
    email = models.EmailField(verbose_name=_("E-mail"))
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                             help_text="5xxxxxxxxx", verbose_name=_("Phone Nr"))
    lead = models.BooleanField(verbose_name=_("Lead"), default=False)

    def phone_number(self):
        part4, rest = self.phone[-2], self.phone[:-2]
        part3, rest = rest[-2], rest[:-2]
        part2, rest = rest[-3], rest[:-3]
        part1 = rest
        return "0 {}".format(" ".join((part1, part2, part3, part4)))

    def __str__(self):
        return self.company_title

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
