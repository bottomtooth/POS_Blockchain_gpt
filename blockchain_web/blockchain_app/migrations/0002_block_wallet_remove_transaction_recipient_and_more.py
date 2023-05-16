# Generated by Django 4.2.1 on 2023-05-16 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('previous_hash', models.CharField(max_length=64)),
                ('nonce', models.PositiveIntegerField()),
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
        migrations.RemoveField(
            model_name='transaction',
            name='recipient',
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.CharField(default='default_receiver', max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AddField(
            model_name='transaction',
            name='block',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blockchain_app.block'),
        ),
    ]
