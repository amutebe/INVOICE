# Generated by Django 3.0.14 on 2021-12-07 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20211207_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='approval_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='Approval status')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='completion',
            field=models.DateField(blank=True, null=True, verbose_name='Completion Date:'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='scheduled',
            field=models.DateField(blank=True, null=True, verbose_name='Rescheduled Date:'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='verification_failed',
            field=models.TextField(blank=True, help_text='If rejected, please give a reason', null=True, verbose_name='Reason for rejecting:'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='verification_status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.approval_status', verbose_name='Status:'),
        ),
    ]