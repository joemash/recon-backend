from src.account.models.user import User
from src.common.serializers.common import BaseModelSerializer


class UserSerializer(BaseModelSerializer):

    class Meta:
        model = User
        exclude = [
            "created",
            "updated",
            "active",
            "created_by",
            "updated_by",
            "is_active",
        ]
