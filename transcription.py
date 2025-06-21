import os
import django
from django.conf import settings

#  DJANGO SETTINGS 
settings.configure(
    DEBUG=True,
    SECRET_KEY='devkey',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'rest_framework',
    ],
    REST_FRAMEWORK={
        'UNICODE_JSON': False,
        'UNAUTHENTICATED_USER': None,
    }
)

django.setup()

# ------------------ IMPORTS ------------------
import requests
from django.http import JsonResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

#  CONFIG 
DEEPGRAM_API_KEY = "499028f1b2aa70fded74f7cc3f300cf87b09cdeb"

#  API VIEW 
@csrf_exempt
@api_view(['POST'])
def transcribe_audio(request):
    # Get any audio file regardless of field name
    if not request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)
    
    # Take the first file uploaded (whatever the name)
    audio_file = list(request.FILES.values())[0]
    
    try:
        headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
        params = {"punctuate": "true", "diarize": "true", "detect_language": "true"}
        files = {"file": ("audio", audio_file.read())}
        
        response = requests.post("https://api.deepgram.com/v1/listen", headers=headers, params=params, files=files)
        
        if response.status_code != 200:
            return JsonResponse({"error": response.text}, status=500)
        
        result = response.json()
        detected_lang = result["results"]["channels"][0]["detected_language"]
        words = result["results"]["channels"][0]["alternatives"][0].get("words", [])
        
        if not words:
            transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
            return JsonResponse({
                "language": detected_lang,
                "transcript": transcript,
                "speakers": []
            })
        
        # Group by speakers
        speakers = []
        current_speaker = words[0]["speaker"]
        text = []
        
        for word in words:
            if word["speaker"] != current_speaker:
                speakers.append({
                    "speaker": f"Speaker {current_speaker}",
                    "text": " ".join(text)
                })
                text = [word["word"]]
                current_speaker = word["speaker"]
            else:
                text.append(word["word"])
        
        if text:
            speakers.append({
                "speaker": f"Speaker {current_speaker}",
                "text": " ".join(text)
            })
        
        full_transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
        
        return JsonResponse({
            "language": detected_lang,
            "transcript": full_transcript,
            "speakers": speakers
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

#  URL CONFIGURATION 
urlpatterns = [
    path('transcribe/', transcribe_audio),
]

# SERVER STARTUP 
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    execute_from_command_line(["manage.py", "runserver", "8000"])