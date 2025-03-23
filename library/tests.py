from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book
from rest_framework_simplejwt.tokens import RefreshToken

class AdminUserTests(TestCase):
    """
    Test cases for Admin user creation, authentication, and JWT validation.
    """
    
    def setUp(self):
        """
        Set up the test client and create a test admin user.
        """
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )
        self.student_user = get_user_model().objects.create_user(
            email='student@example.com',
            password='studentpassword'
        )

    def test_create_admin_user(self):
        """
        Test creating an admin user.
        """
        user = get_user_model().objects.create_user(
            email='testadmin@example.com',
            password='password123'
        )
        self.assertEqual(user.email, 'testadmin@example.com')
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        user = get_user_model().objects.create_superuser(
            email='superadmin@example.com',
            password='superpassword'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_admin_login(self):
        """
        Test logging in an admin and generating JWT tokens.
        """
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        """
        Test invalid login credentials.
        """
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """
        Test token refresh functionality.
        """
        # Obtain token first
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })
        
        refresh_token = response.data['refresh']

        # Refresh the token
        refresh_response = self.client.post(reverse('token_refresh'), {
            'refresh': refresh_token
        })

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)



### 📚 **Book CRUD Tests**

class BookTests(TestCase):
    """
    Test cases for Book model and API endpoints.
    """
    
    def setUp(self):
        """
        Set up the test client and authenticate admin.
        """
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )

        # Authenticate and get tokens
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create initial book
        self.book = Book.objects.create(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            description='A classic novel',
            published_date='1925-04-10'
        )

    def test_create_book(self):
        """
        Test book creation by an admin.
        """
        response = self.client.post(reverse('book-list'), {
            'title': 'New Book',
            'author': 'New Author',
            'description': 'A new book description',
            'published_date': '2025-03-22'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')

    def test_get_books(self):
        """
        Test retrieving book list.
        """
        response = self.client.get(reverse('book-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_book(self):
        """
        Test updating a book.
        """
        book = Book.objects.create(
            title='Old Title',
            author='Old Author',
            description='Old description',
            published_date='2020-01-01'
        )
        
        url = reverse('book-detail', args=[book.id])
        response = self.client.put(url, {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated description',
            'published_date': '2023-01-01'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_book(self):
        """
        Test deleting a book.
        """
        book = Book.objects.create(
            title='Book to Delete',
            author='Author',
            description='To be deleted',
            published_date='2020-01-01'
        )
        
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())



### 🔥 **Error Handling Tests**
class ErrorHandlingTests(TestCase):
    """
    Test cases for invalid input and error handling.
    """

    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )
        
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_invalid_book_creation(self):
        """
        Test creating a book with missing fields.
        """
        response = self.client.post(reverse('book-list'), {
            'title': '',   # Invalid title
            'author': '',
            'description': ''
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_duplicate_email_signup(self):
        """
        Test signup with a duplicate email.
        """
        response = self.client.post(reverse('admin-signup'), {
            'email': 'admin@example.com',
            'password': 'adminpassword123'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_unauthorized_access(self):
        """
        Test access without a valid JWT token.
        """
        self.client.credentials()  # Remove token
        response = self.client.get(reverse('book-list'))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
