# products/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TrendingProductSerializer
from .models import TrendingProduct

@api_view(["POST"])
def trending_api(request):
    serializer = TrendingProductSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()  # uses our custom create()
        TrendingProduct.objects.enforce_limit(limit=1000)
        return Response({"status": "success"}, status=201)
    return Response(serializer.errors, status=400)
