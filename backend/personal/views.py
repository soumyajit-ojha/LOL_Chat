from django.shortcuts import render
from django.views import View
from friend.models import FriendList

class HomeScreenView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}

        if not user.is_authenticated:
            return render(request, 'personal/home.html',context)
        
        try:
            user_friends = FriendList.objects.get(user=user)
            context["friends"] = user_friends.friends.all()
        except FriendList.DoesNotExist:
            context["friends"] = []

        return render(request, 'personal/home.html',context)


