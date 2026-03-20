# Generated migration for QuoteImage model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motivational_quotes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload an image to be randomly attached to quotes', upload_to='quote_images/')),
                ('title', models.CharField(blank=True, help_text='Optional title for this image', max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, help_text='Use this image for random selection')),
            ],
            options={
                'verbose_name_plural': 'Quote Images',
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
