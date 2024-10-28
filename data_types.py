# data_types.py
import datetime

SUPPORTED_DATA_TYPES = {'int','str','integer', 'real', 'char', 'string', 'date', 'date_interval'}

# data_types.py


def parse_data(value, data_type):
    if value is None or value == '':
        raise ValueError(f"Value cannot be empty. Expected {data_type}.")
    try:
        if data_type == 'integer' or data_type == 'int':
            return int(value)
        elif data_type == 'real':
            return float(value)
        elif data_type == 'char':
            if len(value) == 1:
                return value
            else:
                raise ValueError("Char must be a single character.")
        elif data_type == 'string' or data_type == 'str':
            return str(value)
        elif data_type == 'date':
            if isinstance(value, datetime.date):
                return value
            elif isinstance(value, str):
                try:
                    return datetime.datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError as e:
                    raise ValueError(f"Invalid date format: {value}. Expected 'YYYY-MM-DD'.") from e
            else:
                raise TypeError(f"Expected str or datetime.date for data_type 'date', got {type(value).__name__}")
        elif data_type == 'date_interval':
            if isinstance(value, tuple):
                if len(value) != 2:
                    raise ValueError("Date interval tuple must have exactly two elements.")
                start_date, end_date = value
                if not isinstance(start_date, datetime.date) or not isinstance(end_date, datetime.date):
                    raise TypeError("Both elements of the tuple must be datetime.date objects.")
                return f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

            elif isinstance(value, str):
                dates = value.split(' to ')
                if len(dates) != 2:
                    raise ValueError("Date interval must be in 'YYYY-MM-DD to YYYY-MM-DD' format.")
                try:
                    start_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d').date()
                    end_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d').date()
                except ValueError as e:
                    raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.") from e
                return f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            else:
                raise TypeError("Value must be either a tuple of two dates or a string in 'YYYY-MM-DD to YYYY-MM-DD' format.")
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    except ValueError as e:
        raise ValueError(f"Error parsing value '{value}' as {data_type}: {e}")
    finally:
        pass


def validate_data(value, data_type):
    try:
        parse_data(value, data_type)
        return True
    except ValueError:
        return False