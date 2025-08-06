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

### **Step 1: Create Supabase Project**
1. Go to [supabase.com](https://supabase.com)
2. Sign in with GitHub
3. Create a new project named "dog-boarding-storage"
4. Set a database password and choose a region close to your Railway deployment

### **Step 2: Create Storage Bucket**
1. In Supabase dashboard, go to **Storage** in the left sidebar
2. Click **Create a new bucket**
3. Name it `dog-photos`
4. Set it as **Public** (so images can be accessed via URL)
5. Click **Create bucket**

### **Step 3: Configure Bucket Policies**
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

### **Step 4: Get Your Credentials**
1. Go to **Settings** → **API**
2. Copy your **Project URL** (looks like: `https://your-project.supabase.co`)
3. Copy your **anon public** key (starts with `eyJ...`)

### **Step 5: Add Environment Variables to Railway**
1. Go to your Railway project dashboard
2. Go to **Variables** tab
3. Add these environment variables:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### **Step 6: Test Your Setup**
1. Deploy your app to Railway
2. Try uploading a dog photo
3. Check the console logs for:
   - `✅ Photo uploaded to Supabase for [dog name]`
   - Or `⚠️ Photo upload failed, using local storage`

### **Benefits of Supabase Storage**
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

#### **Step 1: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

#### **Step 2: Connect Your Repository**
1. Click **"Deploy from GitHub repo"**
2. Select your dog boarding repository
3. Railway will automatically detect it's a Django app

#### **Step 3: Add PostgreSQL Database**
1. In your Railway project, click **"New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will automatically link it to your app

#### **Step 4: Set Environment Variables**
Go to **Variables** tab and add:
```
SECRET_KEY=your-super-secret-production-key-here
DEBUG=False
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

#### **Step 5: Deploy**
1. Railway will automatically build and deploy your app
2. Your app will be live at `your-app.railway.app`
3. Check the **Deployments** tab for build status

#### **Step 6: Setup Production Database**
1. Go to **Deployments** → **View Logs**
2. Run this command in the Railway console:
   ```bash
   python manage.py setup_production
   ```
3. This creates admin user and sample data

#### **Step 7: Test Your App**
- **Admin Panel**: `https://your-app.railway.app/admin/`
- **Staff Dashboard**: `https://your-app.railway.app/staff/`
- **Owner Login**: `https://your-app.railway.app/login/`

**Default Credentials:**
- **Admin**: `admin` / `admin123456`
- **Sample Owner**: `jane.doe` / `password123`

*For detailed Railway setup, see [RAILWAY_SETUP.md](RAILWAY_SETUP.md)*

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
- **Railway Setup**: See `RAILWAY_SETUP.md` for Railway-specific instructions
- **Supabase Setup**: See `SUPABASE_SETUP.md` for image storage setup
- **Debug Tools**: Use `/debug-production/` for production image troubleshooting
- **Issues**: Create an issue on GitHub
- **Email**: Contact support at support@yourdomain.com

### Common Deployment Issues

**"Images not displaying in production"**
- Check the production debug page: `https://your-domain.railway.app/debug-production/`
- Verify Supabase environment variables are set correctly
- Test image URLs directly in browser

**"Database connection failed"**
- Check Railway environment variables
- Verify PostgreSQL database is running
- Check database credentials in Railway dashboard

**"App won't deploy"**
- Check Railway build logs for errors
- Verify `requirements.txt` is up to date
- Ensure `Procfile` is present in repository

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
- **Railway** - Hosting platform for easy deployment
- **Supabase** - Database and storage platform for persistent data

---

**Built with ❤️ for dog lovers everywhere!**

*This application helps kennels and pet sitters manage their business efficiently while providing excellent service to dog owners.* 