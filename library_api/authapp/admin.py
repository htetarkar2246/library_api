from django.contrib import admin
from .models import CustomUser, OTP

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ("name", "age", "email", "ph_num", "is_staff", "is_active", "created_at", "updated_at",)
  search_fields = ("name", "email", "ph_num") 
  list_filter = ("is_staff", "is_active", "created_at")
  
admin.site.register(CustomUser, CustomUserAdmin)

class OTPAdmin(admin.ModelAdmin):
  list_display = ("user", "otp_code","created_at")

  def has_add_permission(self, request, obj = ...):
    return False
  
  def has_change_permission(self, request, obj = ...):
    return False
      
admin.site.register(OTP, OTPAdmin)