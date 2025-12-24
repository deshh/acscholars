from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


class GroupRequiredMixin(AccessMixin):
    """
    Mixin to check if the user is in a required group or raise a PermissionDenied exception.
    """
    group_required = None  # Define the required group as a class variable

    def dispatch(self, request, *args, **kwargs):
        # Check if the required group is set
        if not self.group_required:
            raise ValueError("group_required must be set in the view or subclass.")

        # Check if the user is authenticated and belongs to the required group
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Check for group membership
        if isinstance(self.group_required, str):
            group_names = [self.group_required]
        else:
            group_names = self.group_required

        if not any(Group.objects.get(name=group_name) in request.user.groups.all() for group_name in group_names):
            raise PermissionDenied

        # If everything checks out, proceed with the normal view dispatch
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied
        # Redirect to login or a custom access denied page
        return redirect(reverse('access_denied'))
    

