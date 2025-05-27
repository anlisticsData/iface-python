import json
from typing import List, Optional


class EmployeeUpdate:
    def __init__(
        self,
        unique: str,
        Operacao: str,
        CodigoFuncionario: str,
        DataBloqueioLiberacao: str,
        CodigoBloqueio: str,
        CodigoObra: str,
        hash_64_dig_1: Optional[str] = None,
        hash_64_dig_2: Optional[str] = None,
        NumeroCracha: Optional[str] = None,
        NomeCompleto: Optional[str] = None,
        id: Optional[int] = None,
        Foto: Optional[str] = None,

    ):
        self.id = id
        self.unique = unique
        self.Operacao = Operacao
        self.CodigoFuncionario = CodigoFuncionario
        self.DataBloqueioLiberacao = DataBloqueioLiberacao
        self.hash_64_dig_1 = hash_64_dig_1
        self.hash_64_dig_2 = hash_64_dig_2
        self.NumeroCracha = NumeroCracha
        self.CodigoBloqueio = CodigoBloqueio
        self.CodigoObra = CodigoObra
        self.NomeCompleto = NomeCompleto
        self.Foto = Foto

    @staticmethod
    def from_dict(data: dict) -> 'EmployeeUpdate':
        return EmployeeUpdate(
            id=data.get('id'),
            unique=data.get('unique', ''),
            Operacao=data.get('Operacao', ''),
            CodigoFuncionario=data.get('CodigoFuncionario', ''),
            DataBloqueioLiberacao=data.get('DataBloqueioLiberacao', ''),
            hash_64_dig_1=data.get('hash_64_dig_1'),
            hash_64_dig_2=data.get('hash_64_dig_2'),
            NumeroCracha=data.get('NumeroCracha'),
            CodigoBloqueio=data.get('CodigoBloqueio', ''),
            CodigoObra=data.get('CodigoObra', ''),
            NomeCompleto=data.get('NomeCompleto'),
            Foto=data.get('Foto'),
        )

    def to_dict(self) -> dict:
        return self.__dict__


class EmployeeUpdateAPIResponse:
    def __init__(self, status: int, error: bool, api: str, data: List[EmployeeUpdate], bundle: List[dict]):
        self.status = status
        self.error = error
        self.api = api
        self.data = data
        self.bundle = bundle

    @staticmethod
    def from_json(json_str: str) -> 'EmployeeUpdateAPIResponse':
        parsed = json.loads(json_str) if isinstance(json_str, str) else json_str
        data_list = [EmployeeUpdate.from_dict(item) for item in parsed.get('data', [])]
        return EmployeeUpdateAPIResponse(
            status=parsed.get('status', 0),
            error=parsed.get('error', False),
            api=parsed.get('api', ''),
            data=data_list,
            bundle=parsed.get('bundle', [])
        )
