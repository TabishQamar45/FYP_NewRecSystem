# Generated by Django 3.1.2 on 2021-12-08 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nexus_360', '0006_auto_20211209_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news_post',
            name='dateOfExtraction',
            field=models.DateField(),
        ),
    ]
