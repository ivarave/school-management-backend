from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("get_last_name", "get_first_name", "get_email", "is_active", "hired_date")
    search_fields = ("user__first_name", "user__last_name", "user__email")
    list_filter = ("is_active", "hired_date")

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = "user__first_name"
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = "user__last_name"
    get_last_name.short_description = "Last Name"

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = "user__email"
    get_email.short_description = "Email"