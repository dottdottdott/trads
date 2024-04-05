from django.shortcuts import render
from solidsocial.util.cache import get_feed

def FeedView(request):
    posts_data, authors_data, reactions_data, responded_data = get_feed()
    return render(request, "feed.html", {
        "current": "Feed", 
        "posts": posts_data, 
        "authors": authors_data,
        "responded": responded_data, 
        "reactions": reactions_data,
        })
