from datetime import date

def parse(s: str, today: date | None = None) -> date:
    '''
    Given a natural language date (string), the function returns a datetime.date object representing the date that the input string refers to. 
    
    The today parameter is used as a reference point for relative date expressions (like "next Tuesday" or "in 3 days"). If today is not provided, it should default to the current date.

    Example
    ----------

    >>> parse('yesterday', today=date(2025,1,2))
    date(2025,1,1)

    >>> parse('two days from tomorrow', today = date(2025,1,1))
    date(2025,1,4)
    '''
    ...