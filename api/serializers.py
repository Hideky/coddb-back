from rest_framework import serializers

# from django.contrib.auth.models import User
from api.models import Artifact, User, Guide
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff"]


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
        )

    def validate(self, attrs):
        if User.objects.filter(username__iexact=attrs["username"]).count():
            raise serializers.ValidationError({"username": "Username already exist"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ArtifactSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    # main_stats_min = serializers.DecimalField(max_digits, decimal_places)

    class Meta:
        model = Artifact
        fields = [
            "id",
            "name",
            "main_stats",
            "main_stats_min",
            "main_stats_max",
            "secondary_stats",
            "secondary_stats_min",
            "secondary_stats_max",
            "img",
            "img_full",
            "categories",
            "quality",
            "cooldown",
            "rage_cost",
            "ability_name",
            "ability_description",
            "ability_upgrade",
        ]
        read_only_fields = fields

    def get_categories(self, obj):
        categories = [obj.category_1, obj.category_2, obj.category_3]
        return filter(lambda c: c != "", categories)


class GuideSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault())
    )

    class Meta:
        model = Guide
        fields = [
            "id",
            "title",
            "img_preview",
            "content",
            "write_date",
            "update_date",
            "author",
            "visible",
        ]
        read_only_fields = ("author", "write_date", "update_date")

    # def create(self, validated_data):
    #     super().create(validated_data)
    #     user = User.objects.create(
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #     )

    #     user.set_password(validated_data["password"])
    #     user.save()

    #     return user
