from django.test import TestCase
from urlranker.use_cases import HTMLProcessor

class HTMLProcessorTestCase(TestCase):
    def test_process_html(self):
        html_content = '''
        <html>
            <body>
                <a href="http://example.com">Valid Link</a>
                <a href="http://google.com">Google Link</a>
                <a href="#">Empty Link</a>
                <a href="http://example.com">Past week</a>
            </body>
        </html>
        '''
        processor = HTMLProcessor()
        valid_links = processor.process_html(html_content)
        
        self.assertEqual(len(valid_links), 2)
        self.assertEqual(valid_links[0].text, "Valid Link")
        self.assertEqual(valid_links[0].url, "http://example.com")
