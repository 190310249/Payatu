# Generated by Django 4.2.4 on 2023-10-02 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firmware_manager', '0008_rename_size_firmware_file_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmware',
            name='admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
