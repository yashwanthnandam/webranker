# use_cases.py
from bs4 import BeautifulSoup
from .entities import Link
from .models import URLResult
import openai
from django.core.cache import cache

class HTMLProcessor:
    def process_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a', href=True)
        link_details = [
            Link(link.get_text(strip=True), link['href'])
            for link in links
            if link.get_text(strip=True) and link['href']
        ]
        valid_links = [link for link in link_details if link.is_valid()]
        return valid_links

class GPTService:
    def __init__(self, api_key, model='gpt-3.5-turbo'):
        openai.api_key = api_key
        self.model = model
        
    def evaluate_links(self, url, links):
        link_info = "\n\nExtracted Links:\n" + "\n".join(
            [f"Text: {link.text}, URL: {link.url}" for link in links]
        )
        return self.get_or_create_result(url, link_info)

    def get_or_create_result(self, url, processed_html):
        cache_key = f"url_result_{url}"
        result = cache.get(cache_key)
        
        if not result:
            try:
                result = URLResult.objects.get(url=url)
                cache.set(cache_key, result.result)
                result = result.result
            except URLResult.DoesNotExist:
                result = self.call_gpt(url, processed_html)
                if 'error' not in result:
                    URLResult.objects.create(url=url, result=result)
                    cache.set(cache_key, result)

        return result

    def call_gpt(self, url, processed_html):
        try:
            extra_prompt = "\n\nEvaluate the legitimacy of each URL and assign a color code (green for high, yellow for medium, red for low). Format the response as 'URL: [url]\\nColor Code: [color code]' for each URL."
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an assistant that processes HTML content."},
                    {"role": "system", "content": extra_prompt},
                    {"role": "user", "content": f"Process the following HTML content from the URL: {url}\n\n{processed_html}"}
                ],
                max_tokens=300
            )
            gpt_output = response['choices'][0]['message']['content'].strip()
            return self.parse_gpt_output(gpt_output)
        except openai.OpenAIError as e:
            return {'error': f"Error calling GPT service: {str(e)}"}

    def parse_gpt_output(self, gpt_output):
        link_color_map = {}
        lines = gpt_output.split('\n\n')
        for line in lines:
            if 'URL:' in line and 'Color Code:' in line:
                parts = line.split('\n')
                url_part = parts[0].split('URL: ')[1].strip()
                color_code = parts[1].split('Color Code: ')[1].strip()
                link_color_map[url_part] = color_code
        return link_color_map
