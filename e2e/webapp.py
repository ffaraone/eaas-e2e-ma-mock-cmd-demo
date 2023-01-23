# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, CloudBlue LLC
# All rights reserved.
#
from typing import List

from connect.client import ConnectClient, R
from connect.eaas.core.decorators import (
    account_settings_page,
    admin_pages,
    module_pages,
    router,
    web_app,
)
from connect.eaas.core.extension import WebApplicationBase
from connect.eaas.core.inject.common import get_call_context
from connect.eaas.core.inject.models import Context
from connect.eaas.core.inject.synchronous import (
    get_installation,
    get_installation_admin_client,
    get_installation_client,
)
from fastapi import Depends

from e2e.schemas import Marketplace, Settings


@web_app(router)
@account_settings_page('Chart settings', '/static/settings.html')
@module_pages(
    'Bar chart',
    '/static/index.html',
    children=[
        {
            'label': 'Line chart',
            'url': '/static/line.html',
        },
    ],
)
@admin_pages(
    [
        {
            'label': 'Admin',
            'url': '/static/settings.html',
        },
    ],
)
class E2EWebApplication(WebApplicationBase):

    @router.get(
        '/settings',
        summary='Retrive charts settings',
        response_model=Settings,
    )
    def retrieve_settings(
        self,
        installation: dict = Depends(get_installation),
    ):
        return Settings(marketplaces=installation['settings'].get('marketplaces', []))

    @router.post(
        '/settings',
        summary='Save charts settings',
        response_model=Settings,
    )
    def save_settings(
        self,
        settings: Settings,
        context: Context = Depends(get_call_context),
        client: ConnectClient = Depends(get_installation_client),
    ):
        client('devops').installations[context.installation_id].update(
            payload={
                'settings': settings.dict(),
            },
        )
        return settings

    @router.get(
        '/admin/{installation_id}/settings',
        summary='Retrive charts settings for admin',
        response_model=Settings,
    )
    def retrieve_admin_settings(
        self,
        installation_id: str,
        client: ConnectClient = Depends(get_installation_admin_client),
    ):
        installation = client('devops').installations[installation_id].get()
        return Settings(marketplaces=installation['settings'].get('marketplaces', []))

    @router.post(
        '/admin/{installation_id}/settings',
        summary='Save charts settings for admin',
        response_model=Settings,
    )
    def save_admin_settings(
        self,
        installation_id: str,
        settings: Settings,
        client: ConnectClient = Depends(get_installation_admin_client),
    ):
        client('devops').installations[installation_id].update(
            payload={
                'settings': settings.dict(),
            },
        )
        return settings

    @router.get(
        '/admin/{installation_id}/marketplaces',
        summary='List all available marketplaces for admin',
        response_model=List[Marketplace],
    )
    def list_admin_marketplaces(
        self,
        installation_id: str,
        client: ConnectClient = Depends(get_installation_admin_client),
    ):
        return [
            Marketplace(**marketplace)
            for marketplace in client.marketplaces.all().values_list(
                'id', 'name', 'description', 'icon',
            )
        ]

    @router.get(
        '/marketplaces',
        summary='List all available marketplaces',
        response_model=List[Marketplace],
    )
    def list_marketplaces(
        self,
        client: ConnectClient = Depends(get_installation_client),
    ):
        return [
            Marketplace(**marketplace)
            for marketplace in client.marketplaces.all().values_list(
                'id', 'name', 'description', 'icon',
            )
        ]

    @router.get(
        '/chart',
        summary='Generate chart data',
    )
    def generate_chart_data(
        self,
        type: str,
        installation: dict = Depends(get_installation),
        client: ConnectClient = Depends(get_installation_client),
    ):
        data = {}
        for mp in installation['settings'].get('marketplaces', []):
            active_assets = client('subscriptions').assets.filter(
                R().marketplace.id.eq(mp['id']) & R().status.eq('active'),
            ).count()
            data[mp['id']] = active_assets

        return {
            'type': type,
            'data': {
                'labels': list(data.keys()),
                'datasets': [
                    {
                        'label': 'Subscriptions',
                        'data': list(data.values()),
                    },
                ],
            },
        }
