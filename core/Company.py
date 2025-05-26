

class Company:
    def __init__(self, client_code=None, company_code=None, banch_code=None, company_access=None):
        self.clientCode = client_code
        self.companyCode = company_code
        self.banchCode = banch_code
        self.companyAccess = company_access

    def __repr__(self):
        return (f"Company(clientCode={self.clientCode!r}, "
                f"companyCode={self.companyCode!r}, "
                f"banchCode={self.banchCode!r}, "
                f"companyAccess={self.companyAccess!r})")