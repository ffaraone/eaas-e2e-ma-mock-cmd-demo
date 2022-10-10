from connect.client import ConnectClient
from fastapi import Depends, Request


from connect.eaas.core.decorators import (
    account_settings_page,
    admin_pages,
    module_pages,
    router,
    web_app,
)
from connect.eaas.core.extension import WebApplicationBase
from connect.eaas.core.inject.synchronous import get_installation, get_installation_client


@web_app(router)
@account_settings_page('My Settings', '/static/settings.html')
@module_pages(
    'My Main Page',
    '/static/index.html',
    children=[
        {
            'label': 'Page 1',
            'url': '/static/page1.html'
        },
        {
            'label': 'Page 2',
            'url': '/static/page2.html'
        },
    ],
)
@admin_pages(
    [
        {
            'label': 'Admin Page',
            'url': '/static/admin.html'
        },
    ]
)
class E2EWebApplication(WebApplicationBase):
    @router.get('/settings')
    def retrieve_settings(
        self,
        installation: dict = Depends(get_installation),
    ):
        return installation

    @router.post('/settings')
    def update_settings(
        self,
        request: Request,
        installation: dict = Depends(get_installation),
        installation_client: ConnectClient = Depends(get_installation_client),
    ):
        settings = request.json()

        installation_client('devops').installations[installation['id']].update(
            {'settings': settings},
        )
        return installation_client('devops').installations[installation['id']].get()

    @router.get('/whoami')
    def whoami(self, installation_client: ConnectClient = Depends(get_installation_client)):
        return installation_client.auth.action('context').get()
