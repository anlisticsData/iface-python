from configparser import ConfigParser
from datetime import datetime

from core.dao.EventsDAO import EventsDAO


def is_expired(date_str: str) -> bool:
    """
    Checks if the given date is expired compared to the current time.

    Parameters:
    - date_str (str): Date in the format "YYYY-MM-DD HH:MM:SS"

    Returns:
    - bool: True if expired, False otherwise
    """
    given_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    return given_date < now


def parse_http_date(date_str: str) -> str:
    """
    Converte uma string de data no formato HTTP para o formato 'YYYY-MM-DD HH:MM:SS'.

    Exemplo:
        'Thu, 29 May 2025 05:36:00 GMT' -> '2025-05-29 05:36:00'
    """
    try:
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Formato de data inválido: {date_str}") from e




def settings(path="config.ini"):
    config = ConfigParser()
    config.read(path)
    return config



def register_event(evento, log, quando=None):
    """
    Registra um novo evento no banco de dados.

    :param evento: Nome curto ou título do evento (string)
    :param log: Detalhes ou descrição do evento (string)
    :param quando: Data/hora do evento (datetime, opcional). Usa datetime.now() se não for informado.
    :return: ID do evento criado, ou False em caso de falha.
    """
    from datetime import datetime
    event_data = {
        "event": evento,
        "event_log": log,
        "created_at": quando or datetime.now()
    }
    return EventsDAO.create(event_data)

