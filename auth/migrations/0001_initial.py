from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('height', models.FloatField(help_text='height in cm')),
                ('weight', models.FloatField(help_text='weight in km')),
                ('fitness_goal', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('picture_url', models.URLField(blank=True, null=True)),
                ('google_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={'db_table': 'auth_customerregister'},
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
