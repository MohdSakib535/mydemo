from django.shortcuts import render
from base.serlizers import UserSerializer,SnippetSerlizers,ResourceSerializer,snippetser
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import Snippet, Resource, Movie
from drf_yasg.utils import swagger_auto_schema
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class Data_view(APIView):
    def get(self,request,format=None):
        user_data=User.objects.all()
        serlizer_data=UserSerializer(user_data,many=True,context={'request': request})
        return Response({"Response":serlizer_data.data})
       


class snippet_view(APIView):
    # user_data=User.objects.all().exist()
    # if user_data:



    def get(self,request):
        # snipped_data=Snippet.objects.filter(user_data=request.user)
        snipped_data=Snippet.objects.all()
        ser=SnippetSerlizers(snipped_data,many=True)
        return Response({"Response":ser.data})

    @swagger_auto_schema(request_body=snippetser)
    def post(self,request):
        try:
            params=request.data
            usr_Data=User.objects.filter(id=params.get('user_data'))
            if not usr_Data:
                return Response({"MSG":"user data doesnot exist"})
            serlizers_data=snippetser(data=params)
            if serlizers_data.is_valid():

                serlizers_data.save()
                print('data save')
            else:
                print('---------------error')
            return Response({"mess":serlizers_data.data,"status":"Created"})
        except Exception as err:
            return Response({"response":err})



class snippet_details(APIView):
    def get(self,request,pk,format=None):
        try:
            s1=Snippet.objects.get(pk=pk)
        except Exception as err:
            from sentry_sdk import capture_message
            from sentry_sdk import a
            capture_message({"MSG":"error from sentry","error":err}, level="error")

            logger.warning(f"Error in Get request in Snippet details .....GET {err}")
            return Response({"error":err})
        ser1=SnippetSerlizers(s1)
        logger.info(f"Get request for a particular data ")
        return Response({"Response":ser1.data})


    def put(self,request,pk):
        s1=Snippet.objects.get(pk=pk)
        sre1=SnippetSerlizers(s1,request.data)
        if sre1.is_valid():
            sre1.save()
            return Response({"Reponse":sre1.data,"status":"Updated"})
        




class Resource_view(APIView):
    def get(self,request,format=None):
        user_data=Resource.objects.all()
        print('user-data---',user_data2)
        sleep(2)
        serlizer_data=ResourceSerializer(user_data,many=True,context={'request': request})
        return Response({"Response":serlizer_data.data})
    
    def post(self,request):
        r_data=ResourceSerializer(data=request.data)
        if r_data.is_valid():
            r_data.save()
            return Response({"response":r_data.data})