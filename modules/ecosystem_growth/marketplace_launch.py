class MarketplaceLaunch:
    def launch(self, marketplace):
        for service in marketplace.services:
            marketplace.services[service]['status'] = 'LIVE'
        return marketplace.services

