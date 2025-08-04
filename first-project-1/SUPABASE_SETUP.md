# 🚀 Supabase Storage Setup Guide

This guide will help you set up Supabase Storage for persistent image uploads on Railway.

## 📋 Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Railway Project**: Your Django app should be deployed on Railway

## 🔧 Step-by-Step Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub
4. Create a new project
5. Choose a name (e.g., "dog-boarding-storage")
6. Set a database password
7. Choose a region close to your Railway deployment

### 2. Create Storage Bucket

1. In your Supabase dashboard, go to **Storage** in the left sidebar
2. Click **Create a new bucket**
3. Name it `dog-photos`
4. Set it as **Public** (so images can be accessed via URL)
5. Click **Create bucket**

### 3. Configure Bucket Policies

1. Go to **Storage** → **Policies**
2. For the `dog-photos` bucket, add these policies:

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

### 4. Get Your Credentials

1. Go to **Settings** → **API**
2. Copy your **Project URL** (looks like: `https://your-project.supabase.co`)
3. Copy your **anon public** key (starts with `eyJ...`)

### 5. Add Environment Variables to Railway

1. Go to your Railway project dashboard
2. Go to **Variables** tab
3. Add these environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### 6. Deploy Your Changes

The code is already set up to use Supabase! Just push your changes:

```bash
git add .
git commit -m "Add Supabase storage support"
git push
```

## 🎯 How It Works

- **Upload**: When users upload dog photos, they're stored in Supabase Storage
- **Display**: Images are served from Supabase's CDN (fast and reliable)
- **Fallback**: If Supabase isn't configured, it falls back to local storage
- **Persistence**: Images survive Railway container restarts

## 🔍 Testing

1. Deploy your app
2. Try uploading a dog photo
3. Check the console logs for:
   - `✅ Photo uploaded to Supabase for [dog name]`
   - Or `⚠️ Photo upload failed, using local storage`

## 🛠️ Troubleshooting

### Images not uploading?
- Check Railway environment variables are set correctly
- Verify Supabase bucket is public
- Check bucket policies are configured

### Images not displaying?
- Verify the photo_url field is populated in the database
- Check Supabase bucket permissions
- Look for console errors in browser dev tools

## 📈 Benefits

- ✅ **Persistent storage**: Images survive Railway restarts
- ✅ **Fast CDN**: Global content delivery
- ✅ **Free tier**: 2GB storage, 1GB bandwidth/month
- ✅ **Reliable**: Managed by Supabase
- ✅ **Fallback**: Works with or without Supabase

## 🎉 Success!

Once configured, your dog photos will be:
- Uploaded to Supabase Storage
- Served from their CDN
- Persistent across Railway deployments
- Fast and reliable worldwide

Your app will now have professional image handling! 🐕✨ 