from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .use_cases import HTMLProcessor, GPTService

# Initialize OpenAI API with your API key

class HTMLProcessingController:
    def __init__(self, gpt_service):
        self.gpt_service = gpt_service
        self.html_processor = HTMLProcessor()

    @csrf_exempt
    def process_html(self, request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                html_content = body.get('htmlContent', '')
                url = body.get('url', '')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

            valid_links = self.html_processor.process_html(html_content)
            gpt_output = self.gpt_service.evaluate_links(url, valid_links)

            return JsonResponse(gpt_output)
        return JsonResponse({'error': 'POST method required'}, status=400)
