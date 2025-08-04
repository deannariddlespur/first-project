# Generated manually to fix daily log photo column

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_add_missing_columns_final'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailylog',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='daily_logs/'),
        ),
    ] 