# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_add_photo_url_simple'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='photo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ] 