from django.contrib import admin
from .models import AdminUser, Book

# ✅ Admin configuration for better display and management
@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for AdminUser model.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Book model.
    """
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('published_date',)
    ordering = ('title',)
