from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager


# Case Insensitive User Model
class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        By default, Django does a case-sensitive check on usernames. This is Wrong™.
        Overriding this method fixes it.
        """
        return self.get(**{self.model.USERNAME_FIELD + "__iexact": username})


class User(AbstractUser):
    objects = CaseInsensitiveUserManager()

    class Meta:
        db_table = "auth_user"


class Artifact(models.Model):
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

    RARITY_CHOICES = [
        (UNCOMMON, "Uncommon"),
        (RARE, "rare"),
        (EPIC, "epic"),
        (LEGENDARY, "legendary"),
    ]

    name = models.CharField(max_length=50)
    img = models.CharField(max_length=70)
    img_full = models.CharField(max_length=70)
    category_1 = models.CharField(max_length=20, blank=True)
    category_2 = models.CharField(max_length=20)
    category_3 = models.CharField(max_length=20)
    quality = models.CharField(max_length=10, choices=RARITY_CHOICES)
    main_stats = models.CharField(max_length=40)
    main_stats_min = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    main_stats_max = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    secondary_stats = models.CharField(max_length=40)
    secondary_stats_min = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    secondary_stats_max = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    cooldown = models.CharField(max_length=10)
    rage_cost = models.IntegerField(default=0)
    ability_name = models.CharField(max_length=40)
    ability_description = models.TextField(null=False)
    ability_upgrade = models.TextField(null=False)

    def __str__(self):
        return f"[{self.quality[0].upper()}] {self.name}"


class Guide(models.Model):
    title = models.CharField(max_length=80)
    img_preview = models.CharField(max_length=70, null=True, blank=True, default="")
    visible = models.BooleanField(default=False)
    content = models.TextField(default="", blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    write_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
