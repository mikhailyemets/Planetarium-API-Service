# Generated by Django 5.0.6 on 2024-06-05 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0003_alter_ticket_options_alter_ticket_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="astronomyshow",
            options={
                "ordering": ["id"],
                "verbose_name": "Astronomy Show",
                "verbose_name_plural": "Astronomy Shows",
            },
        ),
    ]
