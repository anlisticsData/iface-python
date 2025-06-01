import configparser
import json
import traceback

import core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.dao.SettingsDAO import SettingsDAO
from core.dao.employee_dao import EmployeeDAO
from core.device_dn815.UserPhotoUploader import UserPhotoUploader
from core.constantes import __IS_DEVICE_PROCESSING__


class DeviceUploadUseCase(object):
    def __init__(self):
        self.cfg = core.Core.settings()
        self.server = RemoteConnect()
        self.authenticate = self.server.authenticate()

        if self.authenticate.get('status') == 200:
            self.company = Company(self.cfg.get('CUSTOMER', 'code'),
                                   self.cfg.get('CUSTOMER', 'company'),
                                   self.cfg.get('CUSTOMER', 'branch'), 0)






    def execute(self):
        try:
            if SettingsDAO.is_block(__IS_DEVICE_PROCESSING__):
                SettingsDAO.block(__IS_DEVICE_PROCESSING__)
                config = configparser.ConfigParser()
                config.read('config.ini')
                faces_not_device = EmployeeDAO.device_not_faces()
                for row in faces_not_device:
                    try:
                        if row.get('photo') is not None:
                            dirs = row['remote_uuid'].split('-')
                            dir_codes = [dirs[0], dirs[1], dirs[2]]
                            row = {
                                'id': row['id'],
                                'name': row['fullname'],
                                'enabled': True,
                                'photo': row['photo'],

                            }
                            uploader = UserPhotoUploader(config)
                            i = uploader.upload_photo(row, dir_codes)
                            response = json.loads(i)
                            if response.get('create-user-face'):
                                EmployeeDAO.enabled(row['id'])
                            else:
                                EmployeeDAO.enabled(row['id'])

                    except Exception as e:
                        print(f"[Erro] {e}")
                        core.Core.register_event("DeviceUploadUseCase", traceback.format_exc())





        except Exception as e:
            print(f"[Erro] {e}")
            core.Core.register_event("DeviceUploadUseCase", traceback.format_exc())

        finally:
            SettingsDAO.unblock(__IS_DEVICE_PROCESSING__)
