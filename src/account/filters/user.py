from src.account.models.user import User
from src.common.filters.base import BaseFilter


class UserFilter(BaseFilter):

    class Meta:
        model = User
        fields = ["id", "email", "is_active"]
