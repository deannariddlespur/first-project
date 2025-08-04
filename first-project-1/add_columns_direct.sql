-- Add missing columns directly to the database
-- This script adds the photo_base64 column to core_dog and photo column to core_dailylog

-- Add photo_base64 column to core_dog table
ALTER TABLE core_dog ADD COLUMN IF NOT EXISTS photo_base64 TEXT;

-- Add photo column to core_dailylog table  
ALTER TABLE core_dailylog ADD COLUMN IF NOT EXISTS photo VARCHAR(100); 