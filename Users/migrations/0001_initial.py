# Generated by Django 4.2.10 on 2024-02-28 11:31

import Users.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', models.CharField(blank=True, max_length=10, null=True)),
                ('message', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('In Active', 'In Active')], default='Active', max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('role', models.CharField(choices=[('User', 'User'), ('Staff', 'Staff'), ('Admin', 'Admin')], default='User', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_number', models.IntegerField(blank=True, default=Users.models.generate_unique_number, null=True, unique=True)),
                ('category', models.CharField(blank=True, choices=[('2 Wheeler', '2 Wheeler'), ('4 Wheeler', '4 Wheeler'), ('Bus', 'Bus'), ('Truck', 'Truck')], max_length=100, null=True)),
                ('vehicle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_brand', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_reg_no', models.CharField(blank=True, max_length=100, null=True)),
                ('service_time', models.TimeField(blank=True, null=True)),
                ('service_date', models.DateField(blank=True, null=True)),
                ('pickup_address', models.CharField(blank=True, max_length=100, null=True)),
                ('need_delivery', models.BooleanField(blank=True, default=False, null=True)),
                ('service_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('other_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('parts_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('total_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('In Process', 'In Process'), ('Work Complete', 'Work Complete'), ('Completed', 'Completed'), ('Delivered', 'Delivered')], default='Pending', max_length=100, null=True)),
                ('request_date', models.DateField(auto_now_add=True, null=True)),
                ('complete_date', models.DateField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Booking Confirmed', 'Booking Confirmed'), ('In Process', 'In Process'), ('Payment', 'Payment'), ('Completed', 'Completed'), ('Delivered', 'Delivered')], default='Booking Confirmed', max_length=100)),
                ('created_on', models.TimeField(auto_now_add=True)),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.service')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
