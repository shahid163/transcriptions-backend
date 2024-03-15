import requests
import time
import json
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from requests_toolbelt.multipart.encoder import MultipartEncoder

gladia_base_url = "https://api.gladia.io/v2"

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
    
        mp_encoder = MultipartEncoder(
            fields = {
                'audio': (file_obj.name, file_obj, file_obj.content_type)
            }
        )

        headers = {
            "x-gladia-key": settings.GLADIA_KEY,
            'Content-Type': mp_encoder.content_type
        }

        response = requests.post(f"{gladia_base_url}/upload", headers=headers, data=mp_encoder)
        response = response.json()

        response = generate_transcription(response.get("audio_url"))
        
        return Response({"id": response.get("id")}, status=200)

def generate_transcription(audio_url):
    headers = {
        "x-gladia-key": settings.GLADIA_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "audio_url": audio_url,
        "diarization": True,
        "diarization_config": {
            "number_of_speakers": 3,
            "min_speakers": 1,
            "max_speakers": 5
        },
        "translation": True,
        "translation_config": {
            "model": "base",
            "target_languages": ["en"]
        },
        "subtitles": False,
        "detect_language": True,
        "enable_code_switching": False
    }

    trasncription_response = requests.post(f"{gladia_base_url}/transcription", headers=headers, data=json.dumps(data))
    
    return trasncription_response.json()

class TranscriptionView(APIView):
    def get(self, request, id):
        headers = {
            "x-gladia-key": settings.GLADIA_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(f"{gladia_base_url}/transcription/{id}", headers=headers)
        response = response.json()

        if(response.get("status") == "done"):
            return Response(response.get("result", {}).get("transcription", {}), status=200)

        return Response(status=202)