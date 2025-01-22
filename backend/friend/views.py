from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import FriendRequest
from account.models import Account
from .utils import get_friend_request

class SendFriendRequest(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'message': 'You must be logged in to send a friend request.'}, status=401)

        user_id = request.POST.get('receiver_user_id')
        print(user_id)
        if not user_id:
            return JsonResponse({'message': 'Unable to send request. Missing receiver ID.'}, status=400)

        try:
            receiver = Account.objects.get(pk=user_id)

            # Check for existing friend request
            if FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True).exists():
                return JsonResponse({'message': 'You have already sent them a friend request.'}, status=400)

            # Create a new friend request
            FriendRequest.objects.create(sender=user, receiver=receiver, is_active=True)
            return JsonResponse({'message': 'Friend request sent successfully.'}, status=200)

        except Account.DoesNotExist:
            print("Accout not found")
            return JsonResponse({'message': 'Account not found.'}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'message': str(e)}, status=500)

class AllFriendRequest(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}

        if not user.is_authenticated:
            return redirect("login")
        account_id = kwargs.get('user_id')
        try:
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return HttpResponse({"message":"Account doesn't exist"}, status=404)
        if user != account:
            HttpResponse({"message":"You can't see others friends"}, status=403)

        context["friend_requests"] = get_friend_request(user=user)

        return render(request, "friend/friend_requests.html", context)
        