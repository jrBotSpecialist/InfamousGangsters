import requests
import json

class MultiSession:
    def __init__(self, session_cookie_file):
        self.session_cookie_file = session_cookie_file
        self.sessions = self.load_sessions()

    def load_sessions(self):
        with open(self.session_cookie_file, "r") as file:
            session_cookies = json.load(file)

        sessions = []

        for cookie in session_cookies:
            session = requests.Session()
            session.cookies.update(cookie)
            sessions.append(session)

        return sessions

    def get(self, url, **kwargs):
        responses = []
        for session in self.sessions:
            response = session.get(url, **kwargs)
            responses.append(response)
        return responses

    def post(self, url, data=None, json=None, **kwargs):
        responses = []
        for session in self.sessions:
            response = session.post(url, data=data, json=json, **kwargs)
            responses.append(response)
        return responses