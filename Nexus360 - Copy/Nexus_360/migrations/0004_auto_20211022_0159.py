# Generated by Django 3.1.4 on 2021-10-21 20:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nexus_360', '0003_useraccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news_post',
            name='News_content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
