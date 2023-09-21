from User.models import UserModel
from django.contrib.auth.models import Permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddAdmin(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {'message': 'user doesn\'t have permission'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        learning_center_approval_permission = Permission.objects.get(codename="learning_center_admin")
        data = request.data
        try:
            user = UserModel.objects.get(username=data.get('username', None))
        except:
            user = None
        
        if user is not None:
            user.user_permissions.add(learning_center_approval_permission)
            user.save()
            return Response(
                {'message': 'permission updated'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'cannot find username'},
            status=status.HTTP_400_BAD_REQUEST
        )