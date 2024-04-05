from datetime import datetime, timedelta
from django.template.loader import render_to_string
from rest_framework.views import APIView
from solidsocial.models import Author
from solidsocial.util.cache import get_feed
from solidsocial.solidclient.social import background_update
from django.http import JsonResponse

class FeedUpdateAPI(APIView):
    def get(self, request, format=None):
        update_dates = list(Author.objects.filter(followed = True).values_list("last_check",flat=True))
        #rdate = timezone.make_aware(datetime.fromisoformat(request.GET.get('date')))
        rdate = datetime.fromisoformat(request.GET.get('date'))
        if max(update_dates) > rdate:

            # All check dates are newer, update has finished
            if min(update_dates) > rdate:
                posts_data, authors_data, reactions_data, responded_data = get_feed(updatedate=rdate)
                if posts_data:
                    html = render_to_string("blocks/feedblock.html", {
                        "posts": posts_data, 
                        "authors": authors_data,
                        "reactions": reactions_data,
                        "responded": responded_data,
                        })
                else:
                    html = None
                return JsonResponse({'status': "updated", 'data': html})

            # Some check dates are newer, update still in progress
            else:
                return JsonResponse({'status': "in progress"})

        # All check dates are older, starting cache update
        else:
            if max(update_dates) > ( rdate + timedelta(minutes=5) ):
                return JsonResponse({'status': "current"})
            background_update()
            return JsonResponse({'status': "started"})

