# Generated by Django 3.0.8 on 2020-09-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('address', models.CharField(default='N/A', max_length=100, verbose_name='address')),
                ('city', models.CharField(default='N/A', max_length=50, verbose_name='city')),
                ('state', models.CharField(default='N/A', max_length=25, verbose_name='state')),
                ('zip_code', models.CharField(default='N/A', max_length=25, verbose_name='zip_code')),
                ('phone', models.CharField(default='N/A', max_length=15, verbose_name='Phone')),
                ('email', models.CharField(default='N/A', max_length=50, verbose_name='email')),
                ('website', models.CharField(default='N/A', max_length=60, verbose_name='website')),
                ('active', models.BooleanField(default=True, null=True, verbose_name='active')),
                ('image_file', models.CharField(max_length=50, null=True, verbose_name='image')),
                ('created_on', models.DateField()),
                ('last_entry', models.DateField()),
                ('inventory_id', models.IntegerField(null=True)),
                ('lat', models.FloatField(null=True, verbose_name='lat')),
                ('lng', models.FloatField(null=True, verbose_name='lng')),
                ('shelf', models.CharField(default='N/A', max_length=25, verbose_name='shelf')),
            ],
        ),
    ]
