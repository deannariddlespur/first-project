# 🐕 Dog Boarding Management System

A comprehensive web application for managing dog boarding operations, built with Django.

## 🚀 Features

- **Owner Management**: Register and manage dog owners
- **Dog Profiles**: Add dogs with photos and details
- **Booking System**: Calendar-based booking with availability
- **Kennel Management**: Track kennel assignments and sizes
- **Staff Dashboard**: Manage bookings, payments, and facility
- **Payment Tracking**: Monitor payments and invoices
- **Photo Uploads**: Store photos for each dog
- **Daily Logs**: Track activities and notes

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway/Render/Heroku ready

## 📋 Quick Start

### Local Development
```bash
# Clone repository
git clone <your-repo-url>
cd first-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Production Deployment
1. Set up environment variables
2. Configure database (PostgreSQL)
3. Deploy to Railway/Render/Heroku
4. Set up custom domain

## 🔗 URLs

- **Main App**: http://127.0.0.1:8000/
- **Staff Dashboard**: http://127.0.0.1:8000/staff/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
first-project/
├── dogboarding/          # Main Django project
├── core/                 # Main app
│   ├── models.py        # Database models
│   ├── views.py         # Page logic
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── media/               # Uploaded files
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment configuration
└── README.md           # This file
```

## 🐾 Business Rules

### Kennel Size Requirements
- **Large dogs**: Only large kennels ($100/night)
- **Medium dogs**: Medium or large kennels ($75/night)
- **Small dogs**: Any kennel ($50/night)

### Booking Status
- **Pending**: Awaiting confirmation
- **Confirmed**: Approved and scheduled
- **Cancelled**: Cancelled by owner or staff
- **Completed**: Stay is finished

## 🚀 Deployment

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 📞 Support

For issues or questions, check the troubleshooting guide in `QUICK_START.md`.

---

**Built with ❤️ for dog lovers everywhere!** 