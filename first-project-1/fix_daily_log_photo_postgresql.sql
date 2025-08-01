-- PostgreSQL script to fix missing photo column in core_dailylog table
-- This script checks if the column exists and adds it if it doesn't

DO $$
BEGIN
    -- Check if the photo column exists in core_dailylog table
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'core_dailylog' 
        AND column_name = 'photo'
    ) THEN
        -- Add the photo column if it doesn't exist
        ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100);
        RAISE NOTICE 'Added photo column to core_dailylog table';
    ELSE
        RAISE NOTICE 'photo column already exists in core_dailylog table';
    END IF;
END $$; 