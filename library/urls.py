from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Template views
    home, dashboard, admin_signup, admin_login, admin_logout,
    account_profile, account_update, book_search,
    BookListTemplateView, BookDetailTemplateView, BookCreateTemplateView,
    BookUpdateTemplateView, BookDeleteTemplateView,
    # API views
    BookViewSet, StudentBookListView
)

# -----------------------------------------------------------------------------
# API Routing (with /api/ prefix)
# -----------------------------------------------------------------------------
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

api_patterns = [
    # Public API for students to list books
    path('student/books/', StudentBookListView.as_view(), name='student-books'),
    # API endpoints for Book CRUD operations
    path('', include(router.urls)),
]

# -----------------------------------------------------------------------------
# Template Routing (clean URLs)
# -----------------------------------------------------------------------------
template_patterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin/signup/', admin_signup, name='admin-signup'),
    path('admin/login/', admin_login, name='admin-login'),
    path('admin/logout/', admin_logout, name='admin-logout'),
    # Account routes
    path('account/profile/', account_profile, name='account-profile'),
    path('account/update/', account_update, name='account-update'),
    # Book management templates
    path('books/', BookListTemplateView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailTemplateView.as_view(), name='book-detail'),
    path('books/add/', BookCreateTemplateView.as_view(), name='book-form'),
    path('books/edit/<int:pk>/', BookUpdateTemplateView.as_view(), name='book-edit'),
    path('books/delete/<int:pk>/', BookDeleteTemplateView.as_view(), name='book-delete'),
    # Book search view
    path('books/search/', book_search, name='book-search'),
]

urlpatterns = [
    path('api/', include(api_patterns)),   # API endpoints (with /api/ prefix)
    path('', include(template_patterns)),    # Template endpoints (clean URLs)
]
