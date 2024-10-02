# data_types.py

import datetime

def parse_data(value, data_type):
    if value is None or value == '':
        raise ValueError("Value cannot be empty.")
    try:
        if data_type == 'integer':
            return int(value)
        elif data_type == 'real':
            return float(value)
        elif data_type == 'char':
            if len(value) == 1:
                return value
            else:
                raise ValueError("Char must be a single character.")
        elif data_type == 'string':
            return str(value)
        elif data_type == 'date':
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        elif data_type == 'date_interval':
            dates = value.split(' to ')
            if len(dates) != 2:
                raise ValueError("Date interval must be in 'YYYY-MM-DD to YYYY-MM-DD' format.")
            start_date = datetime.datetime.strptime(dates[0], '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(dates[1], '%Y-%m-%d').date()
            return (start_date, end_date)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    except Exception as e:
        raise ValueError(f"Error parsing value '{value}' as {data_type}: {e}")

def validate_data(value, data_type):
    try:
        parse_data(value, data_type)
        return True
    except ValueError:
        return False
