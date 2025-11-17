# Django Library Management System

A comprehensive library management system built with Django that allows librarians to manage books, authors, and user orders, while visitors can browse books and place orders.

## Features

### User Management
- **Two-tier role system**: Visitors and Librarians
- Email-based authentication
- User profile management
- Admin panel for user administration

### Book Management (Librarian Only)
- Add, edit, and delete books
- Upload book cover images
- Track book availability
- Associate multiple authors with books
- Search and filter books

### Author Management (Librarian Only)
- Create and delete authors
- Automatic validation to prevent deletion of authors with books
- View books by author

### Order/Reservation System
- Visitors can order/reserve available books
- 14-day default loan period
- Track active and returned orders
- Automatic overdue detection
- Librarians can manage all orders and close them

## Technical Stack

- **Framework**: Django 5.2.6
- **Database**: PostgreSQL (via psycopg 3.2.10)
- **WebSocket Support**: Django Channels with Redis
- **REST API**: Django REST Framework 3.16.1
- **Testing**: pytest, Selenium
- **Image Processing**: Pillow

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for WebSocket support)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd Django-project-library
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` and configure your settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
```

5. **Run database migrations**
```bash
cd library
python manage.py migrate
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Project Structure

```
Django-project-library/
├── library/
│   ├── authentication/      # User authentication and management
│   ├── author/             # Author management
│   ├── book/               # Book management
│   ├── order/              # Order/reservation system
│   ├── templates/          # HTML templates
│   ├── static/             # Static files (CSS, JS, images)
│   ├── media/              # Uploaded files (book covers)
│   └── library/            # Project settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Usage

### For Visitors
1. Register an account
2. Browse available books
3. Place orders for books
4. View your active and past orders
5. Return books when done

### For Librarians
1. All visitor privileges
2. Add, edit, and delete books
3. Manage authors
4. View all orders and user information
5. Close/complete orders
6. Access Django admin panel

## API Endpoints

The project includes Django REST Framework for potential API usage. Main URLs:
- `/auth/` - Authentication and user management
- `/book/` - Book browsing and management
- `/author/` - Author management
- `/order/` - Order management

## Recent Improvements

### Bug Fixes
1. **Fixed undefined variable in Book.delete_by_id()** - Resolved critical bug where book object wasn't properly retrieved before deletion
2. **Fixed bare except clauses** - Replaced generic except blocks with specific exception handling for better error tracking
3. **Removed incorrect tkinter import** - Cleaned up unused import from book views
4. **Completed Author.to_dict() method** - Added missing return statement

### Code Quality Improvements
1. **Removed unreachable WebSocket code** - Cleaned up dead code in order views
2. **Added admin registration** - Created admin panels for Author and Order models
3. **Improved exception handling** - Specific exception types (DoesNotExist, OSError, ValueError)

### Security Enhancements
1. **Environment variables support** - Migrated sensitive settings to environment variables using python-decouple
2. **Updated requirements.txt** - Added missing dependencies (channels, channels-redis, Pillow, python-decouple, django-mathfilters)
3. **Database credentials** - Removed hardcoded credentials in favor of environment variables
4. **SECRET_KEY protection** - Moved to environment variable with fallback

## Testing

Run tests using pytest:
```bash
pytest
```

For Selenium tests (browser automation):
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please create an issue in the repository.
