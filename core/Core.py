from datetime import datetime


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
