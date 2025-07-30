# 🚀 Complete Dog Boarding App Guide

## 📱 **How to Start Your App (Copy & Paste)**

### **Step 1: Open Terminal**
```bash
# Press Cmd + Space, type "Terminal", press Enter
```

### **Step 2: Navigate to Project**
```bash
cd /Users/deannariddlespur/Desktop/first-project
```

### **Step 3: Activate Virtual Environment**
```bash
source venv/bin/activate
```
*You should see `(venv)` at the start of your prompt*

### **Step 4: Start the Server**
```bash
python manage.py runserver
```

### **Step 5: Open in Browser**
Go to: `http://127.0.0.1:8000/`

---

## 🔗 **Quick Access Links**

### **Owner Side:**
- **Register:** `http://127.0.0.1:8000/register/`
- **Login:** `http://127.0.0.1:8000/login/`
- **Dashboard:** `http://127.0.0.1:8000/dashboard/`
- **Book Calendar:** `http://127.0.0.1:8000/booking/calendar/`
- **My Bookings:** `http://127.0.0.1:8000/booking/list/`

### **Staff Side:**
- **Staff Login:** `http://127.0.0.1:8000/staff/login/`
- **Staff Dashboard:** `http://127.0.0.1:8000/staff/`
- **Staff Calendar:** `http://127.0.0.1:8000/staff/calendar/`
- **All Bookings:** `http://127.0.0.1:8000/staff/bookings/`
- **Kennel Management:** `http://127.0.0.1:8000/staff/kennels/`
- **Payments:** `http://127.0.0.1:8000/staff/payments/`

### **Admin:**
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

---

## 🛠️ **Complete Troubleshooting Guide**

### **If you get "ModuleNotFoundError: No module named 'django'"**
```bash
source venv/bin/activate
```

### **If you get "Error: That port is already in use"**
```bash
# Kill the existing process
pkill -f runserver

# Then start again
python manage.py runserver
```

### **If you need to install dependencies**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### **If you need to create a superuser**
```bash
source venv/bin/activate
python manage.py createsuperuser
```

### **If you get "SystemCheckError: (fields.E210) Cannot use ImageField because Pillow is not installed"**
```bash
source venv/bin/activate
pip install Pillow
```

### **If you get "Page not found (404) No Owner matches the given query"**
- This means you're logged in as admin but don't have an Owner profile
- Go to `http://127.0.0.1:8000/register/` to create an owner account
- Or link your admin user to an Owner in the admin panel

### **If you get "ValueError at /booking/calendar/ month must be in 1..12"**
- This is a calendar navigation bug that was fixed
- Just refresh the page and try again

### **If you get "AttributeError: 'BookingForm' object has no attribute 'cleaned_data'"**
- This was a form validation bug that was fixed
- Just refresh the page and try again

### **If you get "RelatedObjectDoesNotExist: Booking has no dog"**
- This was a model relationship bug that was fixed
- Just refresh the page and try again

---

## 📋 **Complete Copy-Paste Commands**

### **Full Startup Sequence:**
```bash
cd /Users/deannariddlespur/Desktop/first-project
source venv/bin/activate
python manage.py runserver
```

### **If Port is Busy:**
```bash
cd /Users/deannariddlespur/Desktop/first-project
source venv/bin/activate
pkill -f runserver
python manage.py runserver
```

### **If Virtual Environment Not Activated:**
```bash
cd /Users/deannariddlespur/Desktop/first-project
source venv/bin/activate
```

### **To Stop the Server:**
```bash
# Press Ctrl+C in the terminal
```

---

## 🔧 **Complete Setup Instructions**

### **Initial Setup (if starting fresh):**
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install Django
pip install django

# 4. Install Pillow for images
pip install Pillow

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

### **If you need to reset the database:**
```bash
# Delete the database file
rm db.sqlite3

# Delete migration files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Recreate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 🎯 **Complete Test Checklist**

Once your app is running, test these features:

### **Owner Features:**
- [ ] Register new account at `http://127.0.0.1:8000/register/`
- [ ] Login at `http://127.0.0.1:8000/login/`
- [ ] Add a dog from dashboard
- [ ] Book a stay from calendar
- [ ] View booking list
- [ ] Upload dog photos
- [ ] Check booking status

### **Staff Features:**
- [ ] Staff login at `http://127.0.0.1:8000/staff/login/`
- [ ] View dashboard at `http://127.0.0.1:8000/staff/`
- [ ] Manage calendar at `http://127.0.0.1:8000/staff/calendar/`
- [ ] Edit bookings at `http://127.0.0.1:8000/staff/bookings/`
- [ ] Manage kennels at `http://127.0.0.1:8000/staff/kennels/`
- [ ] Track payments
- [ ] Add staff notes

### **Admin Features:**
- [ ] Admin login at `http://127.0.0.1:8000/admin/`
- [ ] View all data
- [ ] Manage users
- [ ] Check database

---

## 🐾 **App Features & Rules**

### **What Your App Can Do:**
- ✅ **Dog owners** can register and book stays
- ✅ **Staff** can manage bookings and kennels
- ✅ **Calendar** shows availability and conflicts
- ✅ **Pricing** is automatic based on kennel size
- ✅ **Photos** can be uploaded for dogs
- ✅ **Payments** can be tracked
- ✅ **Notifications** for booking status
- ✅ **Kennel size validation** prevents wrong assignments
- ✅ **Date format** is consistent (mm/dd/yyyy)
- ✅ **Staff calendar** for facility management

### **Kennel Size Rules:**
- **Large dogs:** Only large kennels ($100/night)
- **Medium dogs:** Medium or large kennels ($75/night)
- **Small dogs:** Any kennel ($50/night)

### **Booking Status Types:**
- **Pending:** Awaiting confirmation
- **Confirmed:** Approved and scheduled
- **Cancelled:** Cancelled by owner or staff
- **Completed:** Stay is finished

---

## 📁 **Project Structure**

```
first-project/
├── dogboarding/          # Main Django project
├── core/                 # Main app
│   ├── models.py        # Database models
│   ├── views.py         # Page logic
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── venv/                # Virtual environment
├── manage.py            # Django management
├── requirements.txt     # Python dependencies
├── QUICK_START.md      # This guide
└── DEPLOYMENT_GUIDE.md # How to go live
```

---

## 🔍 **Common Issues & Solutions**

### **"No save button when adding a dog"**
- Fixed: Submit button is now included in forms

### **"CSS elements hanging over border"**
- Fixed: Overflow and layout issues resolved

### **"Date format is wrong"**
- Fixed: All dates now use mm/dd/yyyy format

### **"Can't select kennel"**
- Fixed: Kennel dropdown now shows availability

### **"Pricing is wrong"**
- Fixed: Pricing now correctly based on kennel size

### **"Calendar navigation errors"**
- Fixed: Month/year calculations corrected

### **"Icons not showing/hiding"**
- Fixed: Edit/delete icons now work properly

---

## 💡 **Pro Tips**

1. **Bookmark these URLs** in your browser for quick access
2. **Keep terminal open** while using the app
3. **Use Cmd+C** in terminal to stop the server
4. **Check terminal** for error messages if something doesn't work
5. **Save this file** to Google Docs for easy reference
6. **Test all features** before going live
7. **Backup your data** regularly

---

## 🚀 **Next Steps**

### **For Development:**
- Test all features thoroughly
- Add more dogs and bookings
- Try different scenarios

### **For Production:**
- Read `DEPLOYMENT_GUIDE.md`
- Choose a hosting platform
- Set up domain name
- Configure SSL certificate

---

## 📞 **Support**

If you encounter issues:
1. Check the terminal for error messages
2. Try refreshing the page
3. Restart the server
4. Check this troubleshooting guide
5. Look at the Django error pages for clues

---

**🎉 Your dog boarding app is ready to use!**

**Copy this entire file to Google Docs for easy access!** 