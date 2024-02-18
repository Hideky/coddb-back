from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Artifact
import re

import csv


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs):
        Artifact.objects.all().delete()
        with open(
            "Call of Dragons Database - Artifacts.csv", newline="", encoding="utf-8"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Keep only legendary for now
                _, created = Artifact.objects.update_or_create(
                    name=row["Name"],
                    defaults={
                        "name": row["Name"],
                        "img": row["Name"].lower().replace(" ", "_").replace("'", "")
                        + ".png",
                        "img_full": row["Name"]
                        .lower()
                        .replace(" ", "_")
                        .replace("'", "")
                        + "_full.png",
                        "main_stats": row["Main Stats"],
                        "main_stats_min": row["MS Min"].replace(",", ".").rstrip("0"),
                        "main_stats_max": row["MS Max"].replace(",", ".").rstrip("0"),
                        "secondary_stats": row["Secondary Stats"],
                        "secondary_stats_min": row["SS Min"]
                        .replace(",", ".")
                        .rstrip("0"),
                        "secondary_stats_max": row["SS Max"]
                        .replace(",", ".")
                        .rstrip("0"),
                        "category_1": row["Category 1"],
                        "category_2": row["Category 2"].replace("/", ""),
                        "category_3": row["Category 3"].replace("/", ""),
                        "quality": row["Quality"],
                        "cooldown": row["Cooldown"],
                        "rage_cost": int(
                            re.sub("\W+", " ", row["Rage Cost"]).replace(" ", "")
                        ),
                        "ability_name": row["Ability Name"],
                        "ability_description": row["Ability Description"],
                        "ability_upgrade": row["Ability Upgrade"],
                    },
                )
                print(f"{row['Name']} - Create: {created}")
