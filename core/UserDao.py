import json
from typing import Optional

class UserDao:
    def __init__(self, name: str, email: str, jwt: str, user: str, access: str, state: str):
        self.name = name
        self.email = email
        self.jwt = jwt
        self.user = user
        self.access = access
        self.state = state

    @staticmethod
    def from_json(json_data: str) -> 'UserDao':
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        return UserDao(
            name=data.get('name', ''),
            email=data.get('email', ''),
            jwt=data.get('jwt', ''),
            user=data.get('user', ''),
            access=data.get('access', ''),
            state=data.get('state', '')
        )

    def to_json(self) -> str:
        return json.dumps({
            'name': self.name,
            'email': self.email,
            'jwt': self.jwt,
            'user': self.user,
            'access': self.access,
            'state': self.state
        })

    def __repr__(self):
        return f"ControllerInfo(name={self.name}, email={self.email}, user={self.user})"
