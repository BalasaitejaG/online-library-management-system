from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_alter_bookrequest_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrequest',
            name='loan_duration',
            field=models.IntegerField(default=14, help_text='Duration in days'),
        ),
        migrations.AddField(
            model_name='bookrequest',
            name='approved_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ] 