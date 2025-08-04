# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_add_photo_url_working'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='photo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ] 