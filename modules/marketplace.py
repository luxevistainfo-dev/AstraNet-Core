class Marketplace:
    def __init__(self):
        self.services = {}

    def list_service(self, service_name, price):
        self.services[service_name] = {"price": price, "status": "LISTED"}
