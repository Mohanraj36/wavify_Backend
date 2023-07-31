
from . models import Song, Playlist
from .serializers import SongSerializer, PlaylistSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from knox.views import LoginView as knoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


def index(request):
    page = Song.objects.all()
    serializer = SongSerializer(page, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required(login_url='login'))
@api_view(['POST'])
def search(request):
    if request.method == 'POST':
        data = request.POST.get('search_query')
        songs_list = Song.objects.filter(
            song_title__startswith=data) | Song.objects.filter(song_movie__startswith=data)
        if songs_list is not None:
            serializer = SongSerializer(songs_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "song not found"}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required(login_url='login'))
@api_view(['GET', 'DELETE', 'PUT'])
def songs(request, id=None):
    if request.user.is_authenticated:
        if request.method == 'GET' and id == None:
            songs_list = Song.objects.all()
            serializer = SongSerializer(songs_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'GET':
            single_song = Song.objects.get(pk=id)
            serializer = SongSerializer(single_song)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            song = Song.objects.get(pk=id)
            serializer = SongSerializer(song, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            try:
                song = Song.objects.get(pk=id)
            except Song.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            song.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class PlayListAPI(APIView):
    # pk is act as userId in get
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk=None):
        if pk is not None:
            obj = Playlist.objects.filter(user=pk)
            serializer = PlaylistSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        data = request.data
        if not Playlist.objects.filter(user=data['user'], songs=data['songs']):
            serializer = PlaylistSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # pk is act as songId in delete
    @method_decorator(login_required(login_url='login'))
    def delete(self, request, pk):
        if pk is not None:
            if Playlist.objects.filter(user=request.user.id, songs=pk).delete():
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(knoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
