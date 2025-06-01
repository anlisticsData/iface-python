import requests

class DeletedEmpleyeeSender:
    def __init__(self, base_url):
        """
        Initializes the log sender with a base URL.
        """
        self.base_url = base_url.rstrip('/')

    def send_deleted_employees(self, employees_code):
        """
        Sends deleted log data to the API via POST.

        Parameters:
        - log_data: Dictionary containing the log fields (e.g., {'user_id': 4517, 'reason': 'removed manually'})

        Returns:
        - response.text if successful
        - None if an error occurs
        """
        try:
            url = f"{self.base_url}/api/user/{employees_code}/delete"
            response = requests.post(url)
            response.raise_for_status()
            print("Deleted User sent successfully.")
            return response.text
        except Exception as e:
            print(f"Failed User send deleted log: {e}")
            return None
