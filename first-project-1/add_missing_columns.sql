-- Add missing columns to database tables
-- This script adds the photo_base64 column to core_dog and photo column to core_dailylog

-- Add photo_base64 column to core_dog table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'core_dog' 
        AND column_name = 'photo_base64'
    ) THEN
        ALTER TABLE core_dog ADD COLUMN photo_base64 TEXT;
        RAISE NOTICE 'Added photo_base64 column to core_dog table';
    ELSE
        RAISE NOTICE 'photo_base64 column already exists in core_dog table';
    END IF;
END $$;

-- Add photo column to core_dailylog table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'core_dailylog' 
        AND column_name = 'photo'
    ) THEN
        ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100);
        RAISE NOTICE 'Added photo column to core_dailylog table';
    ELSE
        RAISE NOTICE 'photo column already exists in core_dailylog table';
    END IF;
END $$; 