import random
import string


from connect.eaas.core.decorators import event
from connect.eaas.core.extension import EventsApplicationBase
from connect.eaas.core.responses import BackgroundResponse


class E2EEventsApplication(EventsApplicationBase):

    @event('installation_status_change', statuses=['installed', 'uninstalled'])
    def on_installation_status_change(self, request):
        account = f'{request["owner"]["name"]} ({request["owner"]["id"]})'
        if request['status'] == 'installed':
            self.logger.info(
                f'This extension has been installed by {account}: '
                f'id={request["id"]}, environment={request["environment"]["id"]}',
            )
        else:
            self.logger.info(
                f'This extension has removed by {account}: '
                f'id={request["id"]}, environment={request["environment"]["id"]}',
            )

    @event('asset_purchase_request_processing', statuses=['pending'])
    def autoapprove_purchase_request(self, request):
        param_a = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        param_b = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        self.logger.info(f'Update parameters: {param_a=}, {param_b=}')
        installation_owner = self.installation['owner']['id']
        if installation_owner.startswith('PA-'):
            self.logger.info(f'Skip event for distributor accounts: {installation_owner}')
            return BackgroundResponse.skip()
        self.installation_client.requests[request['id']].update(
            {
                'asset': {
                    'params': [
                        {
                            'id': 'param_a',
                            'value': param_a,
                        },
                        {
                            'id': 'param_b',
                            'value': param_b,
                        },
                    ],
                },
            },
        )

        product_id = request['asset']['product']['id']
        self.logger.info(f'Search approval template for product {product_id}')
        template = self.installation_client.products[product_id].templates.filter(
            scope='asset',
            type='fulfillment',
        ).first()

        self.logger.info(f'Approve purchase request with template {template["id"]}')
        self.installation_client.requests[request['id']]('approve').post(
            {'template_id': template['id']},
        )

        self.logger.info(f'Purchase request {request["id"]} has been approved')
        return BackgroundResponse.done()
