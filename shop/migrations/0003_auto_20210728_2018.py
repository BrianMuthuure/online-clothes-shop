# Generated by Django 3.2.5 on 2021-07-28 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210728_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('title',)},
        ),
        migrations.AlterIndexTogether(
            name='item',
            index_together={('id', 'slug')},
        ),
    ]