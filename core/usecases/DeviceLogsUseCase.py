import configparser
import json
import traceback

import core
from core import Core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.dao.EmployeesHistoryDAO import EmployeesHistoryDAO
from core.dao.SettingsDAO import SettingsDAO
from core.dao.employee_dao import EmployeeDAO
from core.device_dn815.DeletedLogSender import DeletedLogSender
from core.device_dn815.UserLogFetcher import UserLogFetcher
from core.device_dn815.UserPhotoUploader import UserPhotoUploader
from core.constantes import __IS_DEVICE_PROCESSING__


class DeviceLogsUseCase(object):
    def __init__(self):
        self.cfg = core.Core.settings()
        self.server = RemoteConnect()
        self.authenticate = self.server.authenticate()
        self.delete_logs = 1

        if self.authenticate.get('status') == 200:
            self.company = Company(self.cfg.get('CUSTOMER', 'code'),
                                   self.cfg.get('CUSTOMER', 'company'),
                                   self.cfg.get('CUSTOMER', 'branch'), 0)






    def execute(self):
        try:

            p=SettingsDAO.is_block(__IS_DEVICE_PROCESSING__)
            if SettingsDAO.is_block(__IS_DEVICE_PROCESSING__):
                SettingsDAO.block(__IS_DEVICE_PROCESSING__)
                config = configparser.ConfigParser()
                config.read('config.ini')
                typesaccepted = config.get('SETTINGS', 'typesaccepted')

                log_fetcher = UserLogFetcher(config.get('API', 'iface'))
                log_sender_delete = DeletedLogSender(config.get('API', 'iface'))
                # Buscar todos os logs
                logs = log_fetcher.fetch_logs()
                for log in logs:
                    print(log)
                    accepted = typesaccepted.split("|")
                    if log['action'] in accepted:
                        employees_iface_id = log['user_id']
                        employees_data = EmployeeDAO.read(employees_iface_id)
                        if employees_data is not None:
                            new_history = {
                                'employees_iface_id': employees_iface_id,
                                'employees_remote_code': employees_data['employees_code'],
                                'remote_event_code': employees_data['remote_uuid'],
                                'remote_uud': employees_data['remote_uuid'],
                                'fullname': employees_data['fullname'],
                                'company_join': config.get('CONSTRUCTION', 'code'),
                                'readding': None,
                                'recordType': None,
                                'process': Core.parse_http_date(log['time']),
                                'upload': 'N'
                            }
                            employee_data = EmployeesHistoryDAO.has_time(new_history['employees_iface_id'],
                                                                         new_history['process'])
                            if employee_data is not None and len(employee_data) == 0:
                                EmployeesHistoryDAO.create(new_history)
                                print('save Employee data')
                                if len(logs) >= int(self.delete_logs):
                                    # Enviar um log deletado
                                    log_data = {
                                        'log_id': log['log_id'],
                                        'reason': '',
                                        'timestamp': '0000-00-00T00:00:00'
                                    }
                                    print(log_sender_delete.send_deleted_log(log_data))

                    else:
                        print("nao processado" + log['action'])

        except Exception as e:
            traceback.print_exc()
        finally:
            SettingsDAO.unblock(__IS_DEVICE_PROCESSING__)
