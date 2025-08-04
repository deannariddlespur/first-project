# Generated manually to add missing columns

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20250801_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='photo_base64',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dailylog',
            name='photo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ] 