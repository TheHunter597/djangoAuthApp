from rest_framework import serializers
from ....models import UserModel


class UpdateUserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "country",
            "interests",
            "avatar",
            "phone_number",
            "zip_code",
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.address = validated_data.get("country", instance.address)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        interests = validated_data.get("interests", instance.interests)
        try:
            instance.interests.clear()
            for interest in interests:
                instance.interests.add(interest)
        except:
            pass
        instance.save()
        return instance
