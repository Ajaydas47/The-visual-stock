# your_app/tasks.py
from celery import shared_task
from .alpha import AlphaAssistant  # Import your assistant module here

@shared_task
def celery_speak(text):
    obj=AlphaAssistant()
    obj.tts(text)
