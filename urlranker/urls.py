# In your Django views file (e.g., views.py)
from django.urls import path
from .app import create_app

controller = create_app()

urlpatterns = [
    path('process_html', controller.process_html, name='process_html'),
]
