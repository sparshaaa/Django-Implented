import os
import django
from django.conf import settings

# DJANGO SETTINGS
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

# IMPORTS 
from django.http import JsonResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# MODEL INITIALIZATION 
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
kw_model = KeyBERT(model)

# API VIEW 
@csrf_exempt
@api_view(['POST'])
def generate_titles(request):
    text = request.data.get("text", "")
    if not text:
        return JsonResponse({"error": "Text is required."}, status=400)
    
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=5,
        use_maxsum=True,
        nr_candidates=20
    )
    
    titles = [kw[0].title() for kw in keywords if len(kw[0].split()) <= 3][:3]
    return JsonResponse({"titles": titles})

# URL CONFIGURATION 
urlpatterns = [
    path('generate-titles/', generate_titles),
]

# SERVER STARTUP
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    execute_from_command_line(["manage.py", "runserver", "8000"])