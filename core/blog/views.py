from django.shortcuts import render
from django.views import View


class PostListView(View):
    def get(self, request):
        return render(request, "blog/index.html")