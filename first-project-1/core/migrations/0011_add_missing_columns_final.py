# Generated manually to add missing columns

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20250801_2248'),
    ]

    operations = [
        migrations.RunSQL(
            # Add photo_base64 column to core_dog table
            "ALTER TABLE core_dog ADD COLUMN IF NOT EXISTS photo_base64 TEXT;",
            # Reverse SQL (if needed)
            "ALTER TABLE core_dog DROP COLUMN IF EXISTS photo_base64;"
        ),
        migrations.RunSQL(
            # Add photo column to core_dailylog table
            "ALTER TABLE core_dailylog ADD COLUMN IF NOT EXISTS photo VARCHAR(100);",
            # Reverse SQL (if needed)
            "ALTER TABLE core_dailylog DROP COLUMN IF EXISTS photo;"
        ),
    ]
