# Generated by Django 2.1 on 2021-11-17 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20211115_2332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='full_image',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Realism', 'Realism'), ('Surrealism', 'Surrealism'), ('Pop art', 'Pop art'), ('Tribal', 'Tribal'), ('Geometrical', 'Geometrical'), ('Cubism', 'Cubism'), ('Other', 'Other')], default='Other', max_length=20),
        ),
        migrations.AddField(
            model_name='post',
            name='preview_image',
            field=models.ImageField(default='default.jpg', upload_to='art'),
        ),
    ]
