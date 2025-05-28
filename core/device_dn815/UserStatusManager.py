import requests

class UserStatusManager:
    def __init__(self, base_url):
        """
        Initializes the manager with a base URL.
        """
        self.base_url = base_url.rstrip('/')

    def disable_user(self, user_id):
        """
        Disables a user by sending a POST request.
        """
        return self._post(f"/api/user/{user_id}/disable", user_id, "disable")

    def enable_user(self, user_id):
        """
        Enables a user by sending a POST request.
        """
        return self._post(f"/api/user/{user_id}/enable", user_id, "enable")

    def _post(self, path, user_id, action):
        """
        Internal method to send a POST request without body.
        """
        try:
            url = f"{self.base_url}{path}"
            response = requests.post(url)
            response.raise_for_status()
            print(f"User {user_id} {action}d successfully.")
            return response.text
        except Exception as e:
            print(f"Failed to {action} user {user_id}: {e}")
            return None
