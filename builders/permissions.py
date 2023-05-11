from rest_framework import permissions
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS


class CustomForbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "custom error message"


class OnlyBuilderPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(request.user.role.name == 'manager')
        # print(request.user.status.name == 'active')
        # print(dir(view), 'viewssss')
        # print(dir(request), 'requestsssssss')
        message = 'Adding customers not allowed.'
        if bool(request.user and request.user.is_authenticated
                and request.user.role.name == 'builder'
                and request.user.status.name == 'active'
                ):
            return True


class OnlyManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.status_id)
        if bool(request.user and request.user.is_authenticated
                and request.user.role.name == 'manager'
                and request.user.status.name == 'active'
                ):
            return True


class OnlySaleManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(request.user.status_id)
        if bool(request.user and request.user.is_authenticated
                and request.user.role_id == 4
                and request.user.status_id == 1
                ):
            return True
