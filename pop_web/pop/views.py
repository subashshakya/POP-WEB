from rest_framework import viewsets
from django.contrib.auth import login
from rest_framework.response import Response
from utils.pagination_defination import Pagination
from serializers.serializers import UserSerializers
from models import User
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
import logging

USER_MODEL_REQUIRED_FIELDS = [
    "username",
    "password",
    "email",
    "phone_number",
    "country_code",
    "first_name",
    "last_name",
]


logger = logging.getLogger("pop")


class UserViews(viewsets.ModelViewSet):
    @action(
        detail=False,
        url_path="users",
        url_name="user_list",
        methods=["GET"],
        authentication_classes=[IsAuthenticated],
        permission_classes=[SessionAuthentication],
    )
    def list(self, request):
        try:
            users = User.objects.all()
            paginator = Pagination()
            paginated_user = paginator.paginate_queryset(users, request)
            user_serializer = UserSerializers(paginated_user, many=True)
            return paginator.get_paginated_response(user_serializer.data)
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=["POST"],
    )
    def create(self, request):
        user_serializer = UserSerializers
        request_data = request.data
        valid_user_data = user_serializer(data=request_data)
        try:
            if valid_user_data.is_valid():
                username = request_data.get("username")
                password = request_data.get("password")
                user, created = User.objects.get_or_create(username=username)
                if created:
                    _ = user_serializer.save()
                    return Response(
                        {"success": False, "message": "Sign-up successful"},
                        status=status.HTTP_201_CREATED,
                    )
                if user and password == user.password:
                    login(request, user)
                    return Response(
                        {"success": True, "message": "Login Successful"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"success": False, "message": "Invalid Credentials."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                raise Exception("Invalid request data. Could not parse the data.")
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["GET"])
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as e:
            return Response(
                {"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND
            )
        deserialized_user = UserSerializers(user)
        return Response(
            {"success": True, "data": deserialized_user.data}, status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["PATCH", "PUT"],
        authentication_classes=[IsAuthenticated],
        permission_classes=[SessionAuthentication],
    )
    def update(self, request, pk=None):
        user_serializer = UserSerializers(request.data)
        if user_serializer.is_valid():
            try:
                user = User.objects.get(id=pk)
                for field in USER_MODEL_REQUIRED_FIELDS:
                    user[field] = user_serializer.data[field]
                if user_serializer.data["middle_name"]:
                    user["middle_name"] = user_serializer.data["middle_name"]
                user.save()
            except User.DoesNotExist:
                return Response(
                    {"success": False, "message": "Could not find user."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"success": False, "message": "Could not parse values."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=True,
        methods=["DELETE"],
        authentication_classes=[IsAuthenticated],
        permission_classes=[SessionAuthentication],
    )
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            deleted_count, _ = user.delete()
            if deleted_count == 1:
                return Response(
                    {"success": True, "message": "Deleted user successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"success": False, "message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        except User.DoesNotExist as e:
            logger.error("COULD NOT FIND USER: %s", str(e), exc_info=True)
            return Response(
                {"success": False, "message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True,
        methods=["GET"],
        authentication_classes=[IsAuthenticated],
        permission_classes=[SessionAuthentication],
    )
    def logout(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as e:
            return Response(
                {"success": False, "message": str(e)}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"success": True, "message": "Logout Successful"}, status=status.HTTP_200_OK
        )
