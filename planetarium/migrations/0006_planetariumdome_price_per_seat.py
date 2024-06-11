# Generated by Django 5.0.6 on 2024-06-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0005_alter_planetariumdome_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="planetariumdome",
            name="price_per_seat",
            field=models.DecimalField(decimal_places=2, default=5, max_digits=6),
            preserve_default=False,
        ),
    ]