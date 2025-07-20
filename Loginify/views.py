# from django.http import HttpResponse

# def hello_world(request):
#     return HttpResponse("Hello, world!")

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import UserDetails
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "signup.html")

        user = UserDetails(username=username, email=email, password=password)
        user.save()
        return redirect("login")
    return render(request, "signup.html")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return render(request, "success.html", {"user": user})
            else:
                messages.error(request, "Incorrect password.")
        except UserDetails.DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, "login.html")


@csrf_exempt
def get_all_users(request):
    if request.method == "GET":
        users = list(UserDetails.objects.values())
        return JsonResponse(users, safe=False)

@csrf_exempt
def get_user_by_email(request, email):
    if request.method == "GET":
        try:
            user = UserDetails.objects.get(email=email)
            data = {
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }
            return JsonResponse(data)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt
def update_user(request, email):
    if request.method == "PUT":
        try:
            user = UserDetails.objects.get(email=email)
            data = json.loads(request.body)

            new_username = data.get("username")
            new_password = data.get("password")
            new_email = data.get("email")

            if new_username:
                user.username = new_username

            if new_password:
                user.password = new_password

            if new_email and new_email != email:
                if UserDetails.objects.filter(email=new_email).exists():
                    return JsonResponse({"error": "Email already in use"}, status=400)
                user.email = new_email

            user.save()
            return JsonResponse({"message": "User updated successfully"})

        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_user(request, email):
    if request.method == "DELETE":
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({"message": "User deleted successfully"})
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)