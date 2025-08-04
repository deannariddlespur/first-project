# Generated manually to add photo column to DailyLog

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_fix_daily_log_photo_final'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailylog',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='daily_logs/'),
        ),
    ] 