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





def settings():
    try:
        new_setting = {
                'type':__IS_DEVICE_PROCESSING__,
                'description': 'Controle do Procesamenta da thread e device',
                'paramets': '',
                'json': 0
            }

        setting=SettingsDAO.by_description(new_setting['type'])

        if setting is  None:
            SettingsDAO.create(new_setting)
        else:
            SettingsDAO.update(setting['id'], {'json': '0'})



    except:
        print(traceback.format_exc())







def load_config(path="config.ini"):
    config = ConfigParser()
    config.read(path)
    return config


def process_user(row, config, by_use_case):
    unique = row['unique']
    dir_codes = unique.split('-')
    operation = row.get(__CONSTANT_OPERATION__)
    employee_data = by_use_case.execute(row)
    is_register = employee_data is not None
    is_block = Core.is_expired(row['DataBloqueioLiberacao'])


    # Inserção
    if operation == __STATE_INSERT and not is_register:
        user_create =  NewEmployyesUseCase().execute(row)

        if user_create is not None:
            print('Salvo', row)

    # Atualização ou Ativação
    elif operation in [__STATE_UPDATE, __STATE_INSERT] and is_register and 'id' in employee_data:
        ByEmployeeActiveUseCase().execute(employee_data['id'], row)
        print('Atualizar', row)

    # Exclusão
    if operation == __STATE_DELETED and is_register and 'id' in employee_data:
        ByEmployeeDesactiveUseCase().execute(employee_data['id'])

    # Bloqueio
    manager = UserStatusManager(config.get('API', 'iface'))
    if is_block and is_register and 'id' in employee_data:
        if employee_data is not None:
            ByEmployeeDesactiveUseCase().execute(employee_data['id'])
            print(manager.disable_user(employee_data['id']))
    else:
        if employee_data is not None:
            ByEmployeeActiveUseCase().execute(employee_data['id'],employee_data)
            print(manager.enable_user(employee_data['id']))



    return unique





def face_download_worker():

    print('[Iniciando o worker]')
    config = load_config()
    by_use_case = ByEmployyesUseCase()

    while True:
        try:

            setting_device=SettingsDAO.by_description(__IS_DEVICE_PROCESSING__)
            delete_logs=config.get('SETTINGS', 'delete_logs')
            typesaccepted = config.get('SETTINGS', 'typesaccepted')


            if setting_device['json'] == __STATE_FACE_DEVICE__:
                thread_device = threading.Thread(target=faces_in_device(), daemon=True)
                thread_device.start()

            elif setting_device['json'] == __STATE_DELETE_LOG_DEVICE__:
                print("Log")
                log_fetcher = UserLogFetcher(config.get('API', 'iface'))
                log_sender_delete = DeletedLogSender(config.get('API', 'iface'))
                # Buscar todos os logs
                logs = log_fetcher.fetch_logs()
                for log in logs:
                    print(log)
                    accepted=typesaccepted.split("|")

                    if  log['action'] in accepted:
                        employees_iface_id =log['user_id']
                        employees_data=EmployeeDAO.read(employees_iface_id)
                        if employees_data is not None:
                            new_history = {
                                'employees_iface_id': employees_iface_id,
                                'employees_remote_code': employees_data['employees_code'],
                                'remote_event_code': employees_data['remote_uuid'],
                                'remote_uud': employees_data['remote_uuid'],
                                'fullname':employees_data['fullname'],
                                'company_join':config.get('CONSTRUCTION', 'code'),
                                'readding':None,
                                'recordType': None,
                                'process': Core.parse_http_date(log['time']),
                                'upload': 'N'
                            }
                            employee_data =  EmployeesHistoryDAO.has_time(new_history['employees_iface_id'], new_history['process'])
                            if employee_data is not  None and len(employee_data)==0:
                                EmployeesHistoryDAO.create(new_history)
                                print('save Employee data')
                                if len(logs) >= int(delete_logs):
                                    # Enviar um log deletado
                                    log_data = {
                                        'log_id': log['log_id'],
                                        'reason': '',
                                        'timestamp': '0000-00-00T00:00:00'
                                    }
                                    print(log_sender_delete.send_deleted_log(log_data))
                        SettingsDAO.update(setting_device['id'], {'json': '0'})

                    else:
                        print("nao processado"+log['action'])

            else:
                print("[Início do processamento]  ")
                server = rpc.RemoteConnect()
                response = server.authenticate()
                if response.get('status') == 200:
                    user_logged = UserDao.from_json(response['data'])
                    company = Company(config.get('CUSTOMER', 'code'),
                                      config.get('CUSTOMER', 'company'),
                                      config.get('CUSTOMER', 'branch'), 0)

                    users = server.request_face_download(company, config.get('CONSTRUCTION', 'code'))
                    response_users = json.loads(users) if isinstance(users, str) else users

                    if response_users.get('data') is not None:
                        response_obj = EmployeeUpdateAPIResponse.from_json(users)
                        uniques = [process_user(row.to_dict(), config, by_use_case) for row in response_obj.data]

                        response_update = server.update_employee(uniques)
                        if response_update and response_update.get('status') == 200:
                            print('Atualização concluída:', response_update)
                            SettingsDAO.update(setting_device['id'], {'json': '1'})










        except Exception as e:
            print(f"[Erro] {e}")
            traceback.print_exc()

        print("[Fim do processamento]\n")
        time.sleep(float(config.get('SETTINGS', 'download')))






def faces_in_device():
    try:

        config = configparser.ConfigParser()
        config.read('config.ini')
        setting_device = SettingsDAO.by_description(__IS_DEVICE_PROCESSING__)
        print('[Iniciando o worker send Faces]')
        faces_not_device = EmployeeDAO.device_not_faces()
        for row in faces_not_device:
            try:

                if row['photo'] is not None:
                    dirs = row['remote_uuid'].split('-')
                    dir_codes = [dirs[0], dirs[1], dirs[2]]
                    row = {
                        'id': row['id'],
                        'name':row['fullname'],
                        'enabled': True,
                        'photo': row['photo'],

                    }
                    uploader = UserPhotoUploader(config)
                    response=json.loads(uploader.upload_photo(row, dir_codes))
                    if response.get('create-user-face'):
                        EmployeeDAO.enabled(row['id'])





            except Exception as e:
                print(f"[Erro] {e}")

        print('[Finalizando o worker send Faces]')
        SettingsDAO.update(setting_device['id'], {'json': '0'})

    except Exception:
        traceback.print_exc()




def get_device_logs():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        while True:
            print('[Iniciando o worker busca de Logs]')
            setting_device = SettingsDAO.by_description(__IS_DEVICE_PROCESSING__)
            if setting_device['json'] !=2:
                SettingsDAO.update(setting_device['id'], {'json': '2'})
                print('[Agendando Busca e Dormindo   o worker busca de Logs]')



            print('[Finalizando e Dormindo   o worker busca de Logs]')
            time.sleep(config.getint('SETTINGS', 'logs_search'))





    except Exception:
        traceback.print_exc()








def  upload_movements():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        remote = RemoteConnect()  # deve ser criado fora do loop
        while True:
            print('[Iniciando o worker busca de Movements]')
            try:
                moviments=EmployeesHistoryDAO.get_pending_movements()
                for row in moviments:
                    if row['remote_uuid'] is not None:
                        dirs = row['remote_uuid'].split('-')
                        company_join =  "{}|{}|{}|{}".format(dirs[0], dirs[1], dirs[2], dirs[4])

                        mv ={
                            "branchCompanyCustomerConstruct":company_join,
                            "employeeCode": row['employees_code'] ,
                            "readding":row['process'],
                            "recordType":1,
                            "nsr":  row['employees_code_id']
                        }

                        response=remote.register_return(mv)
                        upload_remote_moviment =json.loads(response) if isinstance(response, str) else response
                        if upload_remote_moviment.get('status') == 201:
                            print('[Salvo Remoto Movements]')
                            EmployeesHistoryDAO.uploadNuvem(row['employees_code_id'])










            except Exception as e:
                print(traceback.print_exc())
                print(f"[Erro] {e}")



            print('[Iniciando o worker busca de Movements   o worker busca de Logs]')
            time.sleep(config.getint('SETTINGS', 'upload'))






    except Exception:
        traceback.print_exc()



if __name__ == '__main__':
    print("Iniciando aplicação...")
    settings()
    thread = threading.Thread(target=face_download_worker, daemon=True)
    thread.start()

    thread_logs = threading.Thread(target=get_device_logs, daemon=True)
    thread_logs.start()

    thread_upload_logs = threading.Thread(target=upload_movements, daemon=True)
    thread_upload_logs.start()







    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando aplicação...")
