# Generated manually to add photo field to Dog model

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_add_dailylog_photo_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='dog_photos/'),
        ),
    ] 