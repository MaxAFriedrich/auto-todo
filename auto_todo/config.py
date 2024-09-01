import yaml


class Config:
    def __init__(self):
        with open("config.yml", 'r') as file:
            self.config = yaml.safe_load(file)

    @property
    def server_port(self) -> int:
        return self.config.get('server', {}).get('port', 9999)

    @property
    def server_host(self) -> str:
        return self.config.get('server', {}).get('host', '0.0.0.0')

    @property
    def server_token(self) -> str:
        return self.config.get('server', {}).get('token', 'CHANGE_ME')

    @property
    def server_refresh(self) -> int:
        return self.config.get('server', {}).get('refresh', 30)

    @property
    def main_list(self) -> str:
        return self.config.get('main_list', 'todo.txt')
