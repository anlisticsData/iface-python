import configparser
import json
import time
import threading
import traceback
from datetime import datetime
import requests
from configparser import ConfigParser

import core.RemoteConnect as rpc
from core import Core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.UserDao import UserDao
from core.dao.EmployeeUpdate import EmployeeUpdateAPIResponse
from core.dao.EmployeesHistoryDAO import EmployeesHistoryDAO
from core.dao.SettingsDAO import SettingsDAO
from core.dao.employee_dao import EmployeeDAO
from core.device_dn815.DeletedLogSender import DeletedLogSender
from core.device_dn815.UserLogFetcher import UserLogFetcher
from core.device_dn815.UserPhotoUploader import UserPhotoUploader
from core.device_dn815.UserStatusManager import UserStatusManager
from core.usecases.ByEmployeeActiveUseCase import ByEmployeeActiveUseCase
from core.usecases.ByEmployeeDesactiveUseCase import ByEmployeeDesactiveUseCase
from core.usecases.ByEmployyesUseCase import ByEmployyesUseCase
from core.usecases.NewEmployyesUseCase import NewEmployyesUseCase
from ifaces import settings, load_config, faces_in_device, process_user

# Constantes de operação
__STATE_INSERT = 'I'
__STATE_DELETED = 'E'
__STATE_UPDATE = 'A'
__CONSTANT_OPERATION__ = "Operacao"
__IS_DEVICE_PROCESSING__="__IS_PROCESSING_DEVICE__"
__IGNORE_LOGS_CARD__="CD"
__STATE_FACE_DEVICE__="1"
__STATE_DELETE_LOG_DEVICE__="2"


__DURACAO_SECONDS__=60







import time
import traceback

# Todas as importações originais permanecem aqui
# ...

def main_loop():
    print("Iniciando aplicação...")
    settings()
    config = load_config()

    # Instanciar o remote fora do loop
    remote = RemoteConnect()
    by_use_case = ByEmployyesUseCase()

    while True:
        try:
            # Worker de download e processamento de rostos
            face_download_worker_cycle(config, by_use_case, remote)

            # Worker de busca de logs
            get_device_logs_cycle(config)

            # Worker de upload de movimentações
            upload_movements_cycle(config, remote)

        except KeyboardInterrupt:
            print("Encerrando aplicação manualmente...")
            break
        except Exception as e:
            print(f"[Erro geral no loop principal] {e}")
            traceback.print_exc()

        time.sleep(1)  # Pequeno intervalo entre ciclos para evitar uso excessivo de CPU

# Ajuste nas funções para rodarem em ciclo único (não contínuo)

def face_download_worker_cycle(config, by_use_case, remote):
    try:
        print("[Ciclo: face_download_worker]")
        setting_device = SettingsDAO.by_description(__IS_DEVICE_PROCESSING__)
        delete_logs = config.get('SETTINGS', 'delete_logs')
        typesaccepted = config.get('SETTINGS', 'typesaccepted')

        if setting_device['json'] == __STATE_FACE_DEVICE__:
            faces_in_device()
            SettingsDAO.update(setting_device['id'], {'json': '0'})

        elif setting_device['json'] == __STATE_DELETE_LOG_DEVICE__:
            log_fetcher = UserLogFetcher(config.get('API', 'iface'))
            log_sender_delete = DeletedLogSender(config.get('API', 'iface'))
            logs = log_fetcher.fetch_logs()
            for log in logs:
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
                        employee_data = EmployeesHistoryDAO.has_time(
                            new_history['employees_iface_id'], new_history['process'])
                        if employee_data is not None and len(employee_data) == 0:
                            EmployeesHistoryDAO.create(new_history)
                            print('save Employee data')
                            if len(logs) >= int(delete_logs):
                                log_data = {
                                    'log_id': log['log_id'],
                                    'reason': '',
                                    'timestamp': '0000-00-00T00:00:00'
                                }
                                log_sender_delete.send_deleted_log(log_data)
                else:
                    print("nao processado" + log['action'])
            SettingsDAO.update(setting_device['id'], {'json': '0'})

        else:
            server = rpc.RemoteConnect()
            response = server.authenticate()
            if response.get('status') == 200:
                user_logged = UserDao.from_json(response['data'])
                company = Company(config.get('CUSTOMER', 'code'),
                                  config.get('CUSTOMER', 'company'),
                                  config.get('CUSTOMER', 'branch'), 0)

                users = server.request_face_download_all(company, config.get('CONSTRUCTION', 'code'))
                response_users = json.loads(users) if isinstance(users, str) else users

                if response_users.get('data') is not None:
                    response_obj = EmployeeUpdateAPIResponse.from_json(users)
                    uniques = [process_user(row.to_dict(), config, by_use_case) for row in response_obj.data]
                    if len(uniques) > 0:
                        response_update = server.update_employee(uniques)
                        if response_update and response_update.get('status') == 200:
                            print('Atualização concluída:', response_update)
                            SettingsDAO.update(setting_device['id'], {'json': '1'})

        time.sleep(float(config.get('SETTINGS', 'download')))

    except Exception:
        traceback.print_exc()

def get_device_logs_cycle(config):
    try:
        print("[Ciclo: get_device_logs]")
        setting_device = SettingsDAO.by_description(__IS_DEVICE_PROCESSING__)
        if setting_device['json'] != "2":
            SettingsDAO.update(setting_device['id'], {'json': '2'})
            print("[Agendada coleta de logs]")
        time.sleep(config.getint('SETTINGS', 'logs_search'))
    except Exception:
        traceback.print_exc()

def upload_movements_cycle(config, remote):
    try:
        print("[Ciclo: upload_movements]")
        moviments = EmployeesHistoryDAO.get_pending_movements()
        for row in moviments:
            if row['remote_uuid'] is not None:
                dirs = row['remote_uuid'].split('-')
                company_join = "{}|{}|{}|{}".format(dirs[0], dirs[1], dirs[2], dirs[4])
                mv = {
                    "branchCompanyCustomerConstruct": company_join,
                    "employeeCode": row['employees_code'],
                    "readding": row['process'],
                    "recordType": 1,
                    "nsr": row['employees_code_id']
                }
                response = remote.register_return(mv)
                upload_remote_moviment = json.loads(response) if isinstance(response, str) else response
                if upload_remote_moviment.get('status') == 201:
                    print('[Movimentação enviada]')
                    EmployeesHistoryDAO.uploadNuvem(row['employees_code_id'])

        time.sleep(config.getint('SETTINGS', 'upload'))

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main_loop()

