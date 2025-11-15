from apps.authentication.permissions import IsSpecificGroup

class IsAdminGroup(IsSpecificGroup):
    allowed_groups = ['Admin']
