from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from playexo.models import PLUser, Role, Activity, Course, Answer



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=('role',)
    can_delete = False

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display=('__str__', 'strategy', 'pltp')
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('__str__', 'name', 'id')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=('user', 'pl', 'date')

class PLUserInline(admin.StackedInline):
    model = PLUser
    filter_horizontal = ('role',)
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    inlines = (PLUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
