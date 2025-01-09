# Generated by Django 5.1.1 on 2024-10-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_rating_product_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=100),
        ),
        migrations.RenameField(
            model_name='product',
            old_name='colors',
            new_name='code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='placement',
        ),
        migrations.AddField(
            model_name='product',
            name='applications',
            field=models.CharField(default='None', max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=600),
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.CharField(max_length=150),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
