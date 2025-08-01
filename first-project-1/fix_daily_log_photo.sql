-- Add the missing photo column to core_dailylog table (PostgreSQL)
-- Check if column exists first
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'core_dailylog' 
        AND column_name = 'photo'
    ) THEN
        ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100) NULL;
    END IF;
END $$; 