
from django.contrib import admin
from .models import Profile, Shares, Order


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

# Re-register UserAdmin
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Shares)
admin.site.register(Order)
# admin.site.register(OrderItem)