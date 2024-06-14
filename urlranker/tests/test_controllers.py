import json
from django.test import TestCase, Client
from unittest.mock import patch
from urlranker.controllers import HTMLProcessingController
from urlranker.use_cases import GPTService

class HTMLProcessingControllerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.gpt_service = GPTService('test_api_key')
        self.controller = HTMLProcessingController(self.gpt_service)

    @patch('openai.ChatCompletion.create')
    def test_process_html(self, mock_create):
        mock_response = {
            'choices': [
                {'message': {'content': 'URL: http://example.com\nColor Code: green'}}
            ]
        }
        mock_create.return_value = mock_response

        html_content = '''
        <html>
            <body>
                <a href="http://example.com">Valid Link</a>
            </body>
        </html>
        '''
        response = self.client.post('/process_html', data=json.dumps({
            'htmlContent': html_content,
            'url': 'http://test.com'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        expected_result = {"http://example.com": "green"}
        self.assertEqual(response.json(), expected_result)
