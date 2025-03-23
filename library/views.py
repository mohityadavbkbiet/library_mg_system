from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Book, AdminUser
from .serializers import BookSerializer, AdminUserSerializer

# -----------------------------------------------------------------------------
# Template Views for Accounts and Books
# -----------------------------------------------------------------------------

def home(request):
    """Render the homepage template."""
    return render(request, 'library/home.html')

def dashboard(request):
    """Render the admin dashboard template."""
    return render(request, 'library/dashboard.html')

def admin_signup(request):
    """Render and process the admin signup form."""
    if request.method == "POST":
        serializer = AdminUserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('admin-login')
        # If signup fails, re-render with error messages.
        return render(request, 'library/signup.html', {'errors': serializer.errors})
    return render(request, 'library/signup.html')

def admin_login(request):
    """Render and process the admin login form."""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        # On failure, show an error message.
        return render(request, 'library/login.html', {'error': 'Invalid credentials'})
    return render(request, 'library/login.html')

def admin_logout(request):
    """Log out the admin and redirect to the homepage."""
    logout(request)
    return redirect('home')

# --- Account Views ---
def account_profile(request):
    """
    Render the profile page for the logged-in admin user.
    """
    if not request.user.is_authenticated:
        return redirect('admin-login')
    return render(request, 'library/profile.html', {'user': request.user})

def account_update(request):
    """
    Render and process the form to update the admin's profile.
    """
    if not request.user.is_authenticated:
        return redirect('admin-login')
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.save()
        return redirect('account-profile')
    return render(request, 'library/profile_update.html', {'user': user})

# --- Book CRUD Template Views ---
class BookListTemplateView(LoginRequiredMixin, ListView):
    """Display the list of books in the admin panel."""
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    login_url = '/admin/login/'

class BookDetailTemplateView(LoginRequiredMixin, DetailView):
    """Display details of a specific book."""
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'
    login_url = '/admin/login/'

class BookCreateTemplateView(LoginRequiredMixin, CreateView):
    """Display a form to add a new book."""
    model = Book
    fields = ['title', 'author', 'description', 'published_date']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')
    login_url = '/admin/login/'

class BookUpdateTemplateView(LoginRequiredMixin, UpdateView):
    """Display a form to edit an existing book."""
    model = Book
    fields = ['title', 'author', 'description', 'published_date']
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')
    login_url = '/admin/login/'

class BookDeleteTemplateView(LoginRequiredMixin, DeleteView):
    """Delete a book and redirect to the book list."""
    model = Book
    template_name = 'library/book_list.html'
    success_url = reverse_lazy('book-list')
    login_url = '/admin/login/'

# --- Book Search View (Extra Functionality) ---
def book_search(request):
    """
    Render a page to search for books.
    """
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) if query else []
    return render(request, 'library/book_search.html', {'books': books, 'query': query})

# -----------------------------------------------------------------------------
# API Views
# -----------------------------------------------------------------------------
class BookViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on Book."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class StudentBookListView(APIView):
    """Public API endpoint for students to view the list of books."""
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
