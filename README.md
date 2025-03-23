# Library Management System

![License](https://img.shields.io/badge/license-MIT-green)
![Django](https://img.shields.io/badge/Django-4.2-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)

A modern library management system with admin authentication, book management, and API access using Django and MySQL.

## Features

✅ **Admin Management**  
- Custom admin user model with email authentication  
- Profile management with bio field  
- JWT token-based authentication  

✅ **Book Management**  
- CRUD operations for books with author/published date tracking  
- Search functionality with template views  
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
- **Infrastructure**: Docker, Nginx  

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.11+
- MySQL client (optional)

### Setup Instructions

1. **Clone repository**
   \`\`\`bash
   git clone https://github.com/mohityadavbkbiet/library_mg_system.git
   cd library_mg_system
   \`\`\`

2. **Set up virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Start MySQL container**
   \`\`\`bash
   docker compose up --build -d
   \`\`\`

5. **Run database migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

6. **Create admin user**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

7. **Start development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

### Access Application
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
library_mg_system/
├── library/               # Core application
│   ├── migrations/        # Database migrations
│   ├── static/            # CSS/JS assets
│   ├── templates/         # HTML templates
│   ├── admin.py           # Admin configurations
│   ├── models.py          # Database models
│   └── views.py           # View logic
├── docker-compose.yml     # Container configuration
└── requirements.txt       # Python dependencies
\`\`\`

## Testing

Run test suite:
\`\`\`bash
python manage.py test
\`\`\`

## Security Considerations

1. **Production Setup**  
   - Set \`DEBUG=False\` in production [[2]]  
   - Use strong database credentials [[5]]  
   - Store secrets in \`.env\` file [[7]]  

2. **Authentication**  
   - JWT tokens with 30-minute expiration  
   - Password hashing with PBKDF2  

3. **Database**  
   - MySQL container with healthchecks  
   - Data persistence via Docker volumes  

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
