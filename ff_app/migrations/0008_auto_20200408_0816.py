# Generated by Django 3.0.5 on 2020-04-08 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_app', '0007_auto_20200408_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='harnessID',
            field=models.CharField(blank=True, default=1, max_length=100),
            preserve_default=False,
        ),
    ]
