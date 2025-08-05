# 🐕 Dog Boarding Management System

A comprehensive web application for managing dog boarding operations, built with Django. Perfect for kennels, pet sitters, and dog boarding facilities.

![Dog Boarding App](https://img.shields.io/badge/Django-4.2+-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Live Demo

**Coming Soon!** - This app will be deployed to Railway/Render with a live URL.

## ✨ Features

### 🏠 **Owner Management**
- **Registration & Login** - Secure owner accounts
- **Dog Profiles** - Add multiple dogs with photos and details
- **Booking System** - Calendar-based booking with real-time availability
- **Payment Tracking** - Monitor payments and invoices
- **Photo Uploads** - Store photos for each dog

### 🏢 **Staff Dashboard**
- **Booking Management** - View, edit, and manage all bookings
- **Kennel Assignment** - Smart kennel allocation based on dog size
- **Payment Processing** - Track payments and generate invoices
- **Facility Calendar** - Manage availability, vacations, and maintenance
- **Daily Logs** - Record activities and notes for each dog

### 📊 **Business Intelligence**
- **Revenue Tracking** - Monitor income and payment status
- **Occupancy Reports** - Track kennel utilization
- **Customer Management** - Owner and dog database
- **Staff Notes** - Internal communication system

### 🔧 **Debug & Troubleshooting**
- **Production Debug Tools** - Built-in image troubleshooting
- **Database Health Checks** - Monitor database status
- **Environment Validation** - Verify configuration settings

## 🛠️ Technology Stack

- **Backend**: Django 4.2+ (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway/Render/Heroku ready
- **File Storage**: Supabase Storage (persistent) / Local storage (fallback)

## 📋 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/dog-boarding-app.git
cd dog-boarding-app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser (admin account)
python manage.py createsuperuser

# 7. Start development server
python manage.py runserver
```

### Access the Application

- **Main App**: http://127.0.0.1:8000/
- **Staff Dashboard**: http://127.0.0.1:8000/staff/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🚀 Supabase Storage Setup (Recommended)

For persistent image storage that survives Railway container restarts, set up Supabase Storage:

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign in with GitHub
3. Create a new project named "dog-boarding-storage"
4. Set a database password and choose a region

### 2. Create Storage Bucket
1. In Supabase dashboard, go to **Storage**
2. Click **Create a new bucket**
3. Name it `dog-photos`
4. Set it as **Public**
5. Click **Create bucket**

### 3. Configure Bucket Policies
Go to **Storage** → **Policies** and add:

**For INSERT (upload):**
```sql
CREATE POLICY "Allow authenticated uploads" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'dog-photos' AND auth.role() = 'authenticated');
```

**For SELECT (download):**
```sql
CREATE POLICY "Allow public downloads" ON storage.objects
FOR SELECT USING (bucket_id = 'dog-photos');
```

### 4. Get Credentials
1. Go to **Settings** → **API**
2. Copy your **Project URL** and **anon public** key

### 5. Add Environment Variables
Add to your Railway project or `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### Benefits of Supabase Storage
- ✅ **Persistent images** that survive Railway restarts
- ✅ **Fast global CDN** for image delivery
- ✅ **Free tier** (2GB storage, 1GB bandwidth/month)
- ✅ **Professional reliability** managed by Supabase
- ✅ **Graceful fallback** to local storage if not configured

*For detailed setup instructions, see [SUPABASE_SETUP.md](SUPABASE_SETUP.md)*

## 🐾 Business Rules

### Kennel Size Requirements
- **Large dogs** (50+ lbs): Only large kennels ($100/night)
- **Medium dogs** (25-50 lbs): Medium or large kennels ($75/night)
- **Small dogs** (<25 lbs): Any kennel ($50/night)

### Booking Status Flow
1. **Pending** - Awaiting staff confirmation
2. **Confirmed** - Approved and kennel assigned
3. **Cancelled** - Cancelled by owner or staff
4. **Completed** - Stay finished

### Pricing Structure
- **Small Kennel**: $50/night
- **Medium Kennel**: $75/night
- **Large Kennel**: $100/night
- **Multi-night discounts** available

## 📁 Project Structure

```
dog-boarding-app/
├── dogboarding/              # Main Django project
│   ├── settings.py          # Development settings
│   ├── settings_production.py # Production settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── core/                     # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── urls.py              # URL routing
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin interface
│   └── templates/           # HTML templates
├── media/                   # Uploaded files (photos)
├── static/                  # Static files (CSS, JS)
├── requirements.txt         # Python dependencies
├── Procfile                # Deployment configuration
├── manage.py               # Django management
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration

**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## 🚀 Deployment

### Railway (Recommended)

1. **Create Railway account** at [railway.app](https://railway.app)
2. **Connect GitHub repository**
3. **Add PostgreSQL database**
4. **Set environment variables**:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ```
5. **Deploy!** Your app will be live at `your-app.railway.app`

### Render (Alternative)

1. **Sign up at [render.com](https://render.com)**
2. **Connect GitHub repository**
3. **Configure build settings**
4. **Set environment variables**
5. **Deploy to Render**

### Custom Domain

1. **Purchase domain** (e.g., `mydogboarding.com`)
2. **Configure DNS** to point to your hosting provider
3. **Add domain** to hosting platform settings
4. **SSL certificate** will be automatic

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing Checklist
- [ ] Owner registration and login
- [ ] Dog profile creation
- [ ] Booking creation and management
- [ ] Staff dashboard functionality
- [ ] Payment tracking
- [ ] Photo uploads
- [ ] Kennel size validation
- [ ] Calendar functionality

## 🔒 Security Features

- **HTTPS enforcement** in production
- **CSRF protection** on all forms
- **SQL injection prevention** via Django ORM
- **XSS protection** with automatic escaping
- **Secure file uploads** with validation
- **Environment variable** management

## 📈 Performance Optimization

- **Database indexing** on frequently queried fields
- **Static file compression** with WhiteNoise
- **Caching** for improved response times
- **Image optimization** for uploaded photos
- **Lazy loading** for large datasets

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**"ModuleNotFoundError: No module named 'django'"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Error: That port is already in use"**
```bash
pkill -f runserver
python manage.py runserver
```

**"Database connection failed"**
- Check environment variables
- Verify database is running
- Check database credentials

**"Images not displaying in production"**
- Check the production debug page: `https://your-domain.railway.app/debug-production/`
- Verify Railway volume plugin is mounted correctly
- Check Supabase environment variables are set
- Test image URLs directly in browser

### Getting Help

- **Documentation**: Check `QUICK_START.md` for detailed setup
- **Deployment**: See `DEPLOYMENT_GUIDE.md` for production setup
- **Debug Tools**: Use `/debug-production/` for production image troubleshooting
- **Issues**: Create an issue on GitHub
- **Email**: Contact support at support@yourdomain.com

## 🎯 Roadmap

### Phase 1 (Current)
- [x] Basic booking system
- [x] Owner and dog management
- [x] Staff dashboard
- [x] Payment tracking
- [x] Photo uploads

### Phase 2 (Next)
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Payment processing (Stripe)
- [ ] Mobile app
- [ ] Advanced reporting

### Phase 3 (Future)
- [ ] Multi-location support
- [ ] Inventory management
- [ ] Customer portal
- [ ] API for integrations
- [ ] Advanced analytics

## 🙏 Acknowledgments

- **Django** - The web framework for perfectionists
- **Bootstrap** - Frontend framework for responsive design
- **Font Awesome** - Icons for better UX
- **Railway/Render** - Hosting platforms for easy deployment

---

**Built with ❤️ for dog lovers everywhere!**

*This application helps kennels and pet sitters manage their business efficiently while providing excellent service to dog owners.* 