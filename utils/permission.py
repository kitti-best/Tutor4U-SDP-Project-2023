from ..User.models import UserModel
from django.contrib.auth.models import Permission


learning_center_approval_permission = Permission.objects.get(codename="approvable")

admin = ['asdfasd', 'asdnl']
for username in admin:
  user = UserModel.objects.get(username=username)
  user.user_permissions.add(learning_center_approval_permission)