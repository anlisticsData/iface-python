import configparser
import json
import time
import threading
import traceback
from datetime import datetime
import requests
from configparser import ConfigParser

import core.Core
from core.dao.EventsDAO import EventsDAO
from core.dao.SettingsDAO import SettingsDAO
from core.usecases.DeviceDeleteEmployeesUseCase import DeviceDeleteEmployeesUseCase
from core.usecases.DeviceLogsUseCase import DeviceLogsUseCase
from core.usecases.DeviceUploadLogsUseCase import DeviceUploadLogsUseCase
from core.usecases.DeviceUploadUseCase import DeviceUploadUseCase
from core.usecases.InsertUploadUseCase import InsertUploadUseCase
from core.usecases.NewEmployyesUseCase import NewEmployyesUseCase
from core.constantes import __STATE_INSERT, __STATE_UPDATE, __IS_DEVICE_PROCESSING__
from core.usecases.UpdateUseCase import UpdateUseCase


def setting_aplication_init():
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
        pass

def load_config(path="config.ini"):
    config = ConfigParser()
    config.read(path)
    return config



def insert_upload():
   while True:
       try:
           print("01-Buscando Registros")
           useCase = InsertUploadUseCase()
           useCase.execute()
           print("01-Finalizando Registros\n\n")
       except Exception as e:
           core.Core.register_event("insert_upload", traceback.format_exc())

       time.sleep(10)



def update_upload():
   while True:
       try:
           print("02-Buscando Registros p.ara Atualizar")
           useCase = UpdateUseCase()
           useCase.execute()
           print("02-Finalizando Registros Atualizar\n\n")
       except:
           core.Core.register_event("update_upload", traceback.format_exc())

       time.sleep(25)





def update_uploa_device():
    while True:
        try:
            print("03-Processando Device  Upload *****************************************************************")
            useCase = DeviceUploadUseCase()
            useCase.execute()
            print("03-Finalizando Processando Device  Upload ***************************************************************** r\n\n")
        except:
            core.Core.register_event("update_uploa_device", traceback.format_exc())

        time.sleep(12)



def los_device():
    while True:
        try:
            print("04-Processando Logs  Device")

            useCase = DeviceLogsUseCase()
            useCase.execute()
            print("04-Finalizando Processando Logs  Device\n\n")
        except:
            core.Core.register_event("los_device", traceback.format_exc())

        time.sleep(60)





def upload_logs_device():
    while True:
        try:
            print("05-Processando Enviando Logs  Device")
            useCase = DeviceUploadLogsUseCase()
            useCase.execute()
            print("05-Finalizando Enviando Logs  Device\n\n")
        except:
            core.Core.register_event("upload_logs_device", traceback.format_exc())

        time.sleep(12)







def delete_empleyee_device():
    while True:
        try:
            print("06-Processando Device  Excluir")
            useCase = DeviceDeleteEmployeesUseCase()
            useCase.execute()
            print("06-Finalizando  Device  Excluir\n\n")
        except:
            core.Core.register_event("delete_empleyee_device", traceback.format_exc())

        time.sleep(25)




if __name__ == '__main__':
    print("Iniciando aplicação...")
    setting_aplication_init()
    thread_insert = threading.Thread(target=insert_upload, daemon=True)
    thread_insert.start()

    thread_update = threading.Thread(target=update_upload, daemon=True)
    thread_update.start()

    thread_update_devive = threading.Thread(target=update_uploa_device, daemon=True)
    thread_update_devive.start()

    thread_update_devive_logs = threading.Thread(target=los_device, daemon=True)
    thread_update_devive_logs.start()

    thread_update_devive_logs_upload = threading.Thread(target=upload_logs_device, daemon=True)
    thread_update_devive_logs_upload.start()

    thread_update_devive_logs_delete = threading.Thread(target=delete_empleyee_device, daemon=True)
    thread_update_devive_logs_delete.start()


    # Mantém o processo principal vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Aplicação finalizada pelo usuário.")








