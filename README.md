# Library Management System

![License](https://img.shields.io/badge/license-MIT-green)
![Django](https://img.shields.io/badge/Django-4.2-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)

A modern library management system with admin authentication, book management, and API access using Django and MySQL.

## Features

✅ **Admin Management**  
- Email-based authentication with custom user model  
- Profile management with bio field  
- JWT token authentication  

✅ **Book Management**  
- CRUD operations for books  
- Search functionality  
- Admin dashboard with Bootstrap UI  

✅ **API Access**  
- RESTful endpoints for book management  
- Student-accessible book listing  
- Token-based authentication (JWT)  

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework  
- **Database**: MySQL 8.0 (Docker container)  
- **Auth**: Simple JWT, Django Allauth  
- **Frontend**: Bootstrap 5.3  

## Getting Started

### Prerequisites
- Docker Desktop (for MySQL container)
- Python 3.11+
- MySQL client (optional)

### Setup Instructions

1. **Clone the repository**  
   \`\`\`bash
   git clone https://github.com/your-repo/library-management.git
   cd library-management
   \`\`\`

2. **Set up virtual environment**  
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**  
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Start MySQL container**  
   \`\`\`bash
   docker compose up --build -d
   \`\`\`

5. **Database configuration**  
   *settings.py already configured to connect to Docker MySQL instance:*
   \`\`\`python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'my_app_db',
           'USER': 'my_app_user',
           'PASSWORD': 'my_app_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   \`\`\`

6. **Run migrations**  
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

7. **Create admin user**  
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

8. **Start development server**  
   \`\`\`bash
   python manage.py runserver
   \`\`\`

9. **Access the application**  
   Open browser at:  
   - Admin panel: http://localhost:8000/admin  
   - API documentation: http://localhost:8000/api/  
   - Frontend: http://localhost:8000  

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| \`/api/books/\` | GET | List all books | Yes |
| \`/api/books/\` | POST | Create new book | Yes |
| \`/api/books/{id}/\` | GET | Book details | Yes |
| \`/api/student/books/\` | GET | Public book list | No |
| \`/api/token/\` | POST | Obtain JWT token | No |
| \`/api/token/refresh/\` | POST | Refresh token | No |

## Project Structure

\`\`\`
library-management/
├── library/               # Main app
│   ├── migrations/        # Database migrations
│   ├── static/            # CSS/JS assets
│   ├── templates/         # HTML templates
│   ├── admin.py           # Admin configurations
│   ├── models.py          # Database models
│   └── views.py           # View logic
├── docker-compose.yml     # MySQL container configuration
└── requirements.txt       # Python dependencies
\`\`\`

## Security Considerations

1. **Production readiness**  
   - Set \`DEBUG=False\` in production [[2]]
   - Use strong database credentials [[5]]
   - Store secrets in \`.env\` file [[7]]

2. **Database**  
   - MySQL container uses healthchecks for stability
   - Data persistence via Docker volumes

3. **Authentication**  
   - JWT tokens with 30-minute expiration
   - Password hashing with PBKDF2

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
