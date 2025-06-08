from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS or request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
        return False
