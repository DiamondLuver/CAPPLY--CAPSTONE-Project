from django.contrib import admin
from .models import  Country, Scholarship, Reply, Comment, Favorited, Level
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields =['id','name'] 
    list_display_links = ('id','name')

class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('id','level', 'school', 'deadline','more_info', 'country')
    search_fields =['id','level', 'school', 'deadline','more_info', 'country'] 
    list_display_links = ('id','level', 'school', 'deadline','more_info', 'country')
    prepopulated_fields = {"slug": ("school","level")}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'scholarship', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'content', 'scholarship')
    list_display_links = ('user', 'content', 'scholarship')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'content')
    list_display_links = ('user', 'content')
    actions = ['approve_reply']

    def approve_reply(self, request, queryset):
        queryset.update(active=True)
 
 
# @admin.register(ScholarshipEdit)
# class ScholarshipEditAdmin(admin.ModelAdmin):
#     list_display = ('user', 'scholarship', 'updated_on','approved')
#     list_filter = ('approved', 'updated_on')
#     search_fields = ('user', 'scholarship', 'updated_on')
#     list_display_links = ('user', 'scholarship', 'updated_on')
#     actions = ['approve_edit_scholarship']

#     def approve_edit_scholarship(self, request, queryset):
#         queryset.update(approved=True)
     
# favorite 
from .models import FavoriteScholarship
admin.site.register(FavoriteScholarship)
admin.site.register(Favorited)
admin.site.register(Level)

# end of favorite   
admin.site.register(Country, CountryAdmin)
admin.site.register(Scholarship, ScholarshipAdmin)