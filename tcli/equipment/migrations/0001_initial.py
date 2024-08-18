# Generated by Django 3.0.8 on 2020-09-06 18:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(default='N/A', max_length=100, verbose_name='description')),
                ('category', models.CharField(default='N/A', max_length=50, verbose_name='category')),
                ('band', models.CharField(default='N/A', max_length=50, verbose_name='band')),
                ('vendor', models.CharField(max_length=50, null=True, verbose_name='vendor')),
                ('model', models.CharField(max_length=50, verbose_name='Model')),
                ('comments', models.CharField(max_length=200, null=True, verbose_name='comments')),
                ('image_file', models.CharField(max_length=20, null=True, verbose_name='Image_file')),
                ('status', models.CharField(max_length=50, null=True, verbose_name='status')),
                ('last_update', models.DateField(default=django.utils.timezone.now)),
                ('inventory_id', models.IntegerField(null=True)),
                ('photo', models.ImageField(blank=True, upload_to='Images/')),
            ],
        ),
    ]
