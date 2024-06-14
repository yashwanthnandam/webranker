class Link:
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def is_valid(self):
        invalid_keywords = [
            'google.com', 'past week', 'past month', 'past year',
            'news', 'images', 'videos', 'shopping', 'books',
            'web', 'flights', 'finance', 'more results'
        ]
        text_lower = self.text.lower()
        return all(keyword not in text_lower for keyword in invalid_keywords) and 'google.com' not in self.url.lower()
