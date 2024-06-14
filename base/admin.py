from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Korisnik, Predmet, Upis

admin.site.register(Predmet)
admin.site.register(Upis)

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('', {'fields':('role', 'status',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('', {'fields':('email','role', 'status',)}),
    )

