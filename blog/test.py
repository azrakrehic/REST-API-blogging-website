import requests
import unittest

class TestAPI(unittest.TestCase):
    URL="http://127.0.0.1:5000/api/posts"

    data={
"blogPost": {
"title": "Internet Trends 2020",
"description": "Let's begin!",
"body": "Everything is trending nowadays!",
"tagList": ["trends", "innovation", "2018"]
}
}

    def test_post_a_blog_post(self):
        resp = requests.post(self.URL,json=self.data)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 completed!")

if __name__ == "__main__":
    tester = TestAPI()

    tester.test_post_a_blog_post()