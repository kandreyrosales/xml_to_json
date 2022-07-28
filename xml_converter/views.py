import xmltodict
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class XMLConverterJSON:
    """
    Class to save file uploaded and convert from XML to JSON
    """
    def __init__(self, myfile):
        self.myfile = myfile
        self.filename_saved = None
        self.filename_path = None

    def custom_json_format(self, obj) -> dict:
        root = obj.get("Root")
        if not root:
            obj["Root"] = ""
            return obj
        new_list_dict = []
        for key, value in root.items():
            for item in value:
                new_list_dict.append({key: [{key_: value_} for key_, value_ in item.items()]})
        obj["Root"] = new_list_dict
        return obj

    def generic_xml_save_file(self):
        fs = FileSystemStorage()
        filename = fs.save(self.myfile.name, self.myfile)
        self.filename_saved = filename
        self.filename_path = f"{settings.MEDIA_ROOT}/{filename}"

    def xml_to_json(self) -> dict:
        """
        Function to convert XML files to dict
        message var is used like error response
        """
        self.generic_xml_save_file()
        if not self.filename_saved.endswith(".xml"):
            return {"message": f"File {self.filename_saved} is not a XML file"}
        with open(self.filename_path, "r") as xml_file:
            try:
                obj = xmltodict.parse(xml_file.read())
                obj = self.custom_json_format(obj)
                return obj
            except json.decoder.JSONDecodeError as err:
                return {"message": err}


def upload_page(request):
    """
    This view is showing errors when is not a valid file or content
    and returning JSON Response of XML file when is a valid XML
    """
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        response = XMLConverterJSON(myfile).xml_to_json()
        response_msg = response.get("message")
        if response_msg:
            return render(request, "upload_page.html", {"message": response_msg})
        return JsonResponse(response)
    return render(request, "upload_page.html")

