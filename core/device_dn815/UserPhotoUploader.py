import requests
import configparser

class UserPhotoUploader:
    def __init__(self, config):
        """
        Initializes the uploader with a configparser.ConfigParser object.
        """
        self.config = config
        self.file_base_url = config.get('API', 'file')
        self.iface_url = config.get('API', 'iface')

    def build_file_url(self, dir_codes, filename):
        """
        Constructs the full file URL based on directory codes and file name.
        """
        return f"{self.file_base_url}/{dir_codes[0]}/{dir_codes[1]}/{dir_codes[2]}/{filename}"

    def upload_photo(self, row, dir_codes):
        """
        Uploads the user's photo to the API.

        Parameters:
        - row: dictionary with keys 'Foto', 'CodigoFuncionario', and 'NomeCompleto'
        - dir_codes: list or tuple of 3 directory levels (e.g., ['2025', '05', '28'])

        Returns:
        - response.text if successful
        - None if an error occurs
        """


        try:
            file_url = self.build_file_url(dir_codes, row['photo'])
            api_url = f"{self.iface_url}/api/user/face"
            row['photo_url']=file_url
            response = requests.post(api_url, data=row)
            return response.text

        except Exception as e:
            print(f"Error uploading photo for user {row.get('id')}: {e}")
            return None
