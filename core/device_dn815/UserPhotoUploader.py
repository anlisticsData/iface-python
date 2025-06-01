import json
import traceback

import requests
import configparser

import core.Core


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
            api_url_delete= f"{self.iface_url}/api/user/{row['id']}/delete"
            row['photo_url']=file_url
            response = requests.post(api_url, data=row,timeout=30)
            response_data=json.loads(response.text)
            if response_data.get('error') =='create-user-face':
                return response_data['error']
            else:
               try:
                   response = requests.post(api_url_delete, data=row,timeout=30)
                   response_data = json.loads(response.text)
                   response = requests.post(api_url, data=row,timeout=30)
                   response_data = json.loads(response.text)
                   return response.text
               except Exception as e:
                   core.Core.register_event("UserPhotoUploader",traceback.format_exc())







        except Exception as e:
            print(f"Error uploading photo for user {row.get('id')}: {e}")
            core.Core.register_event("UserPhotoUploader",traceback.format_exc())
            return None
