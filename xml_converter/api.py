from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from xml_converter.views import XMLConverterJSON


class ConverterViewSet(ViewSet):
    permission_classes = (AllowAny,)
    parser_classes = (XMLParser, MultiPartParser)
    renderer_classes = (XMLRenderer,)

    @action(methods=["POST"], detail=False, url_path="convert")
    def convert(self, request, **kwargs):
        myfile = request.data["file"]
        response = XMLConverterJSON(myfile).xml_to_json()
        response_msg = response.get("message")
        if response_msg:
            custom_message = {"message": response_msg}
        else:
            custom_message = response
        return JsonResponse(custom_message)

