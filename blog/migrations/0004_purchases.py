# Generated by Django 2.1 on 2021-11-17 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20211117_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='purchases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('full_image', models.ImageField(default='default.jpg', upload_to='art')),
                ('category', models.CharField(choices=[('Realism', 'Realism'), ('Surrealism', 'Surrealism'), ('Pop art', 'Pop art'), ('Tribal', 'Tribal'), ('Geometrical', 'Geometrical'), ('Cubism', 'Cubism'), ('Other', 'Other')], default='Other', max_length=20)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
