# Generated by Django 4.2.1 on 2023-05-21 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('previous_hash', models.CharField(max_length=64)),
                ('nonce', models.PositiveIntegerField(null=True)),
                ('hash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=256)),
                ('private_key', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blockchain_app.block')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='transactions',
            field=models.ManyToManyField(related_name='blocks', to='blockchain_app.transaction'),
        ),
    ]
