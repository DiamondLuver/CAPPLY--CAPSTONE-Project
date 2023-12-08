from django.contrib import admin
from .models import Profile , ModeratorRequest
from django.contrib import admin
from .models import ModeratorRequest

class ProfileAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        # Loop through each Profile instance in the queryset
        for profile in queryset:
            # Delete the associated User instance
            user = profile.user
            user.delete()

        # Call the parent class's delete_queryset() method
        super().delete_queryset(request, queryset)
class ModeratorRequestAdmin(admin.ModelAdmin):
    # Register your other admin options for ModeratorRequest model
    pass
    

admin.site.register(ModeratorRequest, ModeratorRequestAdmin)
admin.site.register(Profile, ProfileAdmin)

