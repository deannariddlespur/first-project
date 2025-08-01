-- Add the missing photo column to core_dailylog table
ALTER TABLE core_dailylog ADD COLUMN photo VARCHAR(100) NULL; 