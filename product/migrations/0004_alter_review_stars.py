# Generated by Django 5.0.3 on 2024-03-19 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_review_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=3),
        ),
    ]
