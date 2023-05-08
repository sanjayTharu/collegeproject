# Generated by Django 4.2 on 2023-05-07 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('genre', models.CharField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('Horror', 'Horror'), ('Documentary', 'Dcoumentary'), ('Science Fiction', 'Science Fiction'), ('Romantic', 'Romantic'), ('Drama', 'Drama'), ('Western', 'Western'), ('Thriller', 'Thriller'), ('Animation', 'Animation'), ('Adventure', 'Adventure'), ('Romantic comedy', 'Romantic Comedy'), ('Crime Film', 'Crime Film'), ('Fantasy', 'Fantasy'), ('Film Noir', 'Film Noir'), ('War', 'War'), ('Experimental', 'Experimental'), ('Mystery', 'Mystery'), ('Biographical', 'Biographichal'), ('Dark Comedy', 'Dark Comedy'), ('Historical Film', 'Historical Film'), ('Short', 'Short'), ('Spy', 'Spy'), ('Musical', 'Musical')], default='ACTION', max_length=50)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('posterurl', models.URLField(blank=True)),
                ('poster', models.ImageField(upload_to='movie_images/')),
                ('recommended_movies', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.PositiveIntegerField()),
                ('seat_number', models.PositiveIntegerField()),
                ('is_booked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Theatre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('QFX Cinemas Jalma', 'QFX Cinemas Jalma'), ('Chitwan cineplex', 'Chitwan cineplex'), ('Indradev Cinema', 'Indredev cinema'), ('Ganesh Filmhall', 'Ganesh Filmhall')], default='QFX Cinemas Jalma', max_length=100)),
                ('location', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_date', models.DateField()),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.seat')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.show')),
            ],
        ),
        migrations.AddField(
            model_name='show',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.theatre'),
        ),
        migrations.AddField(
            model_name='seat',
            name='theater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.theatre'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Esewa', 'Esewa'), ('Khalti', 'Khalti'), ('Others', 'Others')], default='khanti', max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.ticket')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('theater', 'row_number', 'seat_number')},
        ),
    ]
