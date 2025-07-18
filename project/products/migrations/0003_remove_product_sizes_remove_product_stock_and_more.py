# Generated by Django 5.2 on 2025-07-03 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_description_remove_product_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AddField(
            model_name='productgroup',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='product_groups', to='products.size'),
        ),
        migrations.CreateModel(
            name='ProductSizeStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.size')),
            ],
        ),
    ]
