# Generated by Django 3.2.7 on 2021-09-26 06:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buildable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=4)),
                ('displayname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[-0-9a-zA-Z ]*$', 'Only alphanumeric characters, spaces or dashes are allowed.')])),
                ('image_link', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('tier', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('subcategory', models.CharField(blank=True, max_length=200, null=True)),
                ('power_usage', models.FloatField(blank=True, null=True)),
                ('overclockable', models.BooleanField(blank=True, null=True)),
                ('inputs_conveyer', models.IntegerField(blank=True, null=True)),
                ('outputs_conveyer', models.IntegerField(blank=True, null=True)),
                ('inputs_pipeline', models.IntegerField(blank=True, null=True)),
                ('outputs_pipeline', models.IntegerField(blank=True, null=True)),
                ('size_width', models.IntegerField(blank=True, null=True)),
                ('size_length', models.IntegerField(blank=True, null=True)),
                ('size_height', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('version', 'displayname')},
            },
        ),
        migrations.CreateModel(
            name='NodeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[-0-9a-zA-Z ]*$', 'Only alphanumeric characters, spaces or dashes are allowed.')])),
                ('type', models.CharField(choices=[('Node', 'Node'), ('Well', 'Well')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=4)),
                ('displayname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[-0-9a-zA-Z ]*$', 'Only alphanumeric characters, spaces or dashes are allowed.')])),
                ('image_link', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('tier', models.CharField(blank=True, max_length=200, null=True)),
                ('blueprint_path', models.CharField(blank=True, max_length=200, null=True)),
                ('stack_size', models.IntegerField(blank=True, null=True)),
                ('sink_value', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=4)),
                ('displayname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[-0-9a-zA-Z ]*$', 'Only alphanumeric characters, spaces or dashes are allowed.')])),
                ('type', models.CharField(blank=True, choices=[('default', 'Default'), ('alternate', 'Alternate')], default='default', max_length=20)),
                ('machine_seconds', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('amount_min', models.FloatField(blank=True, null=True)),
                ('mj', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='satisfactory.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='satisfactory.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('amount_min', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='satisfactory.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='satisfactory.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients_for', through='satisfactory.RecipeInput', to='satisfactory.Product'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='satisfactory.buildable'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(related_name='recipes', through='satisfactory.RecipeOutput', to='satisfactory.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='default_recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_recipe_products', to='satisfactory.recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together={('version', 'displayname')},
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('version', 'displayname')},
        ),
    ]
