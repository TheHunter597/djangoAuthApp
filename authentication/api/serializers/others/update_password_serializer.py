from rest_framework import serializers
from ....models import UserModel
class UpdateUserPassword(serializers.ModelSerializer):
    new_password=serializers.CharField(max_length=128,write_only=True)
    confirm_new_password=serializers.CharField(max_length=128,write_only=True)
    old_password=serializers.CharField(max_length=128,write_only=True)
    class Meta:
        model=UserModel
        fields=("old_password","new_password","confirm_new_password")
    def update(self,instance,validated_data):
        instance.set_password(validated_data.get("new_password",instance.password))
        instance.save()
        return instance
    def validate_new_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError(["Password must be at least 8 characters long"])
        return value
    def validate(self,attrs):
        if not attrs["old_password"] or not attrs["new_password"] or not attrs["confirm_new_password"]:
            raise serializers.ValidationError({"message":"Password change error","errors":{"password":["Old password wasnt provided"],"new_password":["New password wasnt provided"],"confirm_new_password":["Confirm new password wasnt provided"]}})
        if not self.instance.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password":"Old password is wrong"})
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError({"new_password":"New password and confirm new password must match","confirm_new_password":"New password and confirm new password must match"})
        return super().validate(attrs)
