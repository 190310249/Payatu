# Generated by Django 4.2.4 on 2023-10-02 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firmware_manager', '0009_firmware_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='firmware',
            name='failure_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='firmware',
            name='md5',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='firmware',
            name='sha1',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='firmware',
            name='sha256',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
