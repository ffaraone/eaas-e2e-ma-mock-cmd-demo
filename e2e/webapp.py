from connect.client import ConnectClient
from fastapi import Depends, Request


from connect.eaas.core.decorators import router, web_app
from connect.eaas.core.extension import WebAppExtension
from connect.eaas.core.inject.synchronous import get_installation, get_installation_client


@web_app(router)
class E2EWebAppExtension(WebAppExtension):
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
