import json
import time
import threading
import traceback
from datetime import datetime

import requests
import core.RemoteConnect as rpc
from core import Core
from core.Company import Company
from configparser import ConfigParser

from core.UserDao import UserDao
from core.dao.EmployeeUpdate import EmployeeUpdateAPIResponse
from core.usecases.ByEmployeeActiveUseCase import ByEmployeeActiveUseCase
from core.usecases.ByEmployeeDesactiveUseCase import ByEmployeeDesactiveUseCase
from core.usecases.ByEmployyesUseCase import ByEmployyesUseCase
from core.usecases.NewEmployyesUseCase import NewEmployyesUseCase




__STATE_INSERT='I'
__STATE_DELETED='E'
__STATE_UPDATE='A'

__CONSTANT_OPERATION__="Operacao"













user_logged=None
company=None


def face_download_worker():
    print('Hello world')
    config_path = "config.ini"
    config = ConfigParser()
    config.read(config_path)
    ByUseUseCase =ByEmployyesUseCase()






    while True:
        try:
            print("processando.. inicio|")
            server = rpc.RemoteConnect()
            response = server.authenticate()
            uniques = []
            if response['status'] == 200:
                user_logged = UserDao.from_json(response['data'])
                company = Company(config.get('CUSTOMER', 'code'),
                                  config.get('CUSTOMER', 'company'),
                                  config.get('CUSTOMER', 'branch'), 0)

                users =server.request_face_download(company, config.get('CONSTRUCTION', 'code'))
                response_users = json.loads(users) if isinstance(users, str) else users
                if response_users['data'] is not None:

                    response = EmployeeUpdateAPIResponse.from_json(users)
                    for update in response.data:
                        row=update.to_dict()
                        unique=row['unique']
                        dir_codes=unique.split('-')
                        operation = row[__CONSTANT_OPERATION__]
                        employee_data =ByUseUseCase.execute(row)
                        is_registers = True if employee_data is not None else False
                        is_block=Core.is_expired(row['DataBloqueioLiberacao'])
                        if operation is not None and (operation == __STATE_INSERT or operation == __STATE_DELETED):
                            if is_registers is not True:
                                if NewEmployyesUseCase().execute(row) is not None:
                                    print('Salvo', row)




                        if operation is not None and operation==__STATE_DELETED:
                            ByEmployeeDesactiveUseCase().execute(employee_data['id'])


                        if operation is not None and operation==__STATE_UPDATE:
                            ByEmployeeActiveUseCase().execute(employee_data['id'],row)






                        if is_block and isinstance(employee_data, dict) and 'id' in employee_data:
                            ByEmployeeDesactiveUseCase().execute(employee_data['id'])




                        uniques.append(unique)

                    response_update_employees=server.update_employee(uniques)
                    if response_update_employees is not None:
                        if response_update_employees['status'] == 200:
                            print('Salvo', response_update_employees)
                            uniques.clear()








        # print(server.request_face_download(company, config.get('CONSTRUCTION', 'code')))

        except Exception as e:
            print(f"Erro durante execução: {e}")
            print("Erro durante execução  PILHA:")
            traceback.print_exc()

        print("processando.. Fim\n|")
        time.sleep(float(config.get('SETTINGS','download')))


if __name__ == '__main__':
    print("Hello world")
    face_download_worker()

    json_dict = {
        'name': 'Controladora 1',
        'email': 'controladora1@app.com',
        'jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'user': '6',
        'access': '3',
        'state': '3'
    }

    # Parse a partir de dicionário
    controller = UserDao.from_json(json_dict)
    print(controller)

    # Convertendo de volta para JSON
    json_str = controller.to_json()
    print(json_str)



















    '''
    if row['Foto'] is not None:
        file_path=config.get('API', 'file')

        file_url="{}{}/{}/{}/{}".format(config.get('API', 'file'),
                                     dir_codes[0],dir_codes[1],dir_codes[2], row['Foto'])


        try:
            url = "{}/api/user/face".format(config.get('API', 'iface'))
            # Dados do formulário (campos de texto)
            data = {
                   'id': row['CodigoFuncionario'],
                   'name': row['NomeCompleto'],
                   'enabled': 'true',  # ou 'false',
                   'photo_url': file_url,
            }

            response = requests.post(url, data=data)

            print(response.text)

        except:
            pass



    '''




    '''
    
  
    thread = threading.Thread(target=face_download_worker)
    thread.daemon = True  # Encerra a thread se o programa principal for finalizado
    thread.start()

    # Loop principal pode fazer outras coisas ou apenas manter o programa vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando aplicação...")


'''