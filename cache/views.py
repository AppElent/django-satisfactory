from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from .permissions import IsAdmin
from django.core.cache import cache
from .serializers import CacheSerializer

class CacheRequest(viewsets.GenericViewSet):
    """
    Class to imcorporate method to make a Cache request
    """
    permission_classes = [IsAdmin]
    serializer_class = CacheSerializer

    def get_queryset(self):
        return None

class Cache(CacheRequest):
    """
    Get Cache
    """
    """
    List all cache keys
    """
    def list(self, request):
        return Response(cache.keys("*"), status=status.HTTP_200_OK)
        #return Response(cache.get_keys(), status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        return Response(cache.get(pk), status=status.HTTP_200_OK)

    def create(self, request):
        cache.set(request.data['key'], request.data['value'], int(request.data['timeout']) if request.data['timeout'] else None)
        return Response(status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        cache.set(pk, request.data['value'])
        return Response(status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        cache.delete(pk)
        return Response(status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def listdetails(self, request):
        allkeys = cache.keys("*")
        array = []
        for key in allkeys:
            try:
                value = cache.get(key)
                if value is not None:
                    dicti = {
                        "key": key,
                        "value": value,
                        "ttl": cache.ttl(key)
                    }
                    array.append(dicti)
            except:
                pass

        return Response(array, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def flush(self, request):
        cache.clear()
        return Response(status.HTTP_200_OK)
