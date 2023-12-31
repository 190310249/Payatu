# Generated by Django 4.2.4 on 2023-09-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmware_manager', '0006_firmware_root_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='directory',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
