from rest_framework.views import APIView
from reviews_app.models import Review
from user_auth.models import Seller
from offer_app.models import Offer
from rest_framework.response import Response
from django.db.models import Avg


class BaseInfoView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "review_count": Review.objects.count(),
            "average_rating": round(Review.objects.aggregate(Avg("rating"))["rating__avg"] or 0, 1),
            "business_profile_count": Seller.objects.count(),
            "offer_count": Offer.objects.count(),
        }
        return Response(data)
