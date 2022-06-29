from datetime import datetime


class Log:
    """A log class that the server uses to save reponses"""
    def log_response(self, type, error, username):
        """Logs the response of a client request to a txt file"""
        date_time = datetime.utcnow().isoformat()
        format = (f'{date_time} (ISO 8601):{username}:{type}:{error}')
        with open('log.txt', 'a') as f:
            f.write(format + '\n')
