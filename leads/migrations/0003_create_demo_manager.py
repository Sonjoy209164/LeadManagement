from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_demo_manager(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.update_or_create(
        username="manager",
        defaults={
            "email": "manager@example.com",
            "is_staff": True,
            "is_superuser": True,
            "password": make_password("manager123"),
        },
    )


def remove_demo_manager(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="manager").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0002_assignedwork_teamlead_delete_lead_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_demo_manager, remove_demo_manager),
    ]
