class DomainException(Exception):
    status_code = 400
    message = 'Domain error'
    log_level = 'warning'

    def to_dict(self):
        return {'error': self.message}
