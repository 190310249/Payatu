# Generated by Django 4.2.4 on 2023-09-26 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firmware_manager', '0005_alter_firmware_shared_orgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmware',
            name='root_dir',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='firmware_manager.directory'),
        ),
    ]
