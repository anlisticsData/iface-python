import time
import threading
import requests
import core.RemoteConnect as rpc
from core.Company import Company
from configparser import ConfigParser


def face_download_worker():
    print('Hello world')
    config_path = "config.ini"
    config = ConfigParser()
    config.read(config_path)

    while True:
        try:
            print("processando..|")
            f = rpc.RemoteConnect()
            user = f.authenticate()
            print(user)
            print(user['data'])

            cc = Company(config.get('CUSTOMER', 'code'), 1, '001', 0)
            print(f.request_face_download(cc, '101'))

        except Exception as e:
            print(f"Erro durante execução: {e}")

        time.sleep(float(config.get('SETTINGS','download')))


if __name__ == '__main__':
    thread = threading.Thread(target=face_download_worker)
    thread.daemon = True  # Encerra a thread se o programa principal for finalizado
    thread.start()

    # Loop principal pode fazer outras coisas ou apenas manter o programa vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando aplicação...")
