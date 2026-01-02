from rest_framework.serializers import ModelSerializer

from api.models import Task, Brigade, User, Specialization

class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class UserSerializer(ModelSerializer):
    specialization = SpecializationSerializer()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "telegram_id", "middle_name", "phone_number", "specialization", "role"]


class BrigadeSerializer(ModelSerializer):
    foreman = UserSerializer()
    workers = UserSerializer(many=True)

    class Meta:
        model = Brigade
        fields = "__all__"


class TaskSerializer(ModelSerializer):
    brigades = BrigadeSerializer(many=True)

    class Meta:
        model = Task
        fields = "__all__"
