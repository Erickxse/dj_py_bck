from apps.authentication.permissions import IsSpecificGroup

class IsSuperAdminGroup(IsSpecificGroup):
    allowed_groups = ['Superadmin']
