import requests

class UserLogFetcher:
    def __init__(self, base_url):
        """
        Initializes the log fetcher with a base URL.
        """
        self.base_url = base_url.rstrip('/')

    def fetch_logs(self, params=None):
        """
        Fetches logs from the API.

        Parameters:
        - params: Optional dictionary to include as query parameters (e.g., {'user_id': 4517})

        Returns:
        - response.json() if successful
        - None if an error occurs
        """
        try:
            url = f"{self.base_url}/api/logs"
            response = requests.get(url, params=params)
            response.raise_for_status()
            print("Logs fetched successfully.")
            return response.json()
        except Exception as e:
            print(f"Failed to fetch logs: {e}")
            return None
