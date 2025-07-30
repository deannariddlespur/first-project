# 🚀 Railway Production Database Setup

## 📋 Quick Setup Guide

Your dog boarding app is now live on Railway! Here's how to set up the production database with initial users and data.

## 🔧 Step 1: Access Railway Console

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Find your `first-project` service
3. Click on the service to open the console

## 🗄️ Step 2: Run Database Setup Command

In the Railway console, run this command:

```bash
python manage.py setup_production
```

This will create:
- ✅ **Admin user** (username: `admin`, password: `admin123456`)
- ✅ **Sample owner** (username: `jane.doe`, password: `password123`)
- ✅ **6 kennels** (2 small, 2 medium, 2 large)

## 🔐 Step 3: Test Your Login Credentials

### **Admin Access:**
- **URL:** https://first-project-production-6e00.up.railway.app/admin/
- **Username:** `admin`
- **Password:** `admin123456`

### **Staff Dashboard:**
- **URL:** https://first-project-production-6e00.up.railway.app/staff/login/
- **Username:** `admin`
- **Password:** `admin123456`

### **Owner Access:**
- **URL:** https://first-project-production-6e00.up.railway.app/login/
- **Username:** `jane.doe`
- **Password:** `password123`

## 🎯 Step 4: Test Your App

1. **Homepage:** https://first-project-production-6e00.up.railway.app/
2. **Register new owners:** Use the beautiful registration page
3. **Add dogs:** Log in as an owner and add dog profiles
4. **Create bookings:** Use the booking calendar
5. **Manage everything:** Use the staff dashboard

## 🔒 Security Note

**Change the default passwords** after first login:
- Admin password: `admin123456` → Your secure password
- Owner password: `password123` → Your secure password

## 📞 Need Help?

If you encounter any issues:
1. Check Railway logs for error messages
2. Verify the command ran successfully
3. Test the login credentials above

## 🎉 Success!

Once you've run the setup command, your production app will have:
- ✅ Working admin access
- ✅ Sample owner account
- ✅ Kennels for bookings
- ✅ Beautiful UI for registration/login
- ✅ Full booking system functionality

Your dog boarding app is now fully operational! 🐕✨ 