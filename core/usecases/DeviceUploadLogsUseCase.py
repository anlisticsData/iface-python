import configparser
import json
import traceback

import core
from core.Company import Company
from core.RemoteConnect import RemoteConnect
from core.dao.EmployeesHistoryDAO import EmployeesHistoryDAO


class DeviceUploadLogsUseCase(object):
    def __init__(self):
        self.cfg = core.Core.settings()
        self.server = RemoteConnect()
        self.authenticate = self.server.authenticate()

        if self.authenticate.get('status') == 200:
            self.company = Company(self.cfg.get('CUSTOMER', 'code'),
                                   self.cfg.get('CUSTOMER', 'company'),
                                   self.cfg.get('CUSTOMER', 'branch'), 0)



    def  execute(self):

        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            remote = RemoteConnect()  # deve ser criado fora do loop
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
                        print('[Salvo Remoto Movements]')
                        EmployeesHistoryDAO.uploadNuvem(row['employees_code_id'])
        except Exception as e:
            print(f"[Erro] {e}")

