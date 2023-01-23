/*
Copyright (c) 2022, CloudBlue LLC
All rights reserved.
*/
import {
  getChart,
  getMarketplaces,
  getSettings,
  processCheckboxes,
  processMarketplaces,
  processSelectedMarketplaces,
  updateSettings,
} from './utils';

import {
  addEventListener,
  disableButton,
  enableButton,
  hideComponent,
  prepareChart,
  prepareMarketplaces,
  prepareMarketplacesWithSwitch,
  renderChart,
  renderMarketplaces,
  showComponent,
} from './components';


export const saveSettingsData = async (app, installationId) => {
  if (!app) return;
  disableButton('save', 'Saving...');
  try {
    const allMarketplaces = await getMarketplaces(installationId);
    const checkboxes = processCheckboxes(document.getElementsByTagName('input'));
    const marketplaces = processSelectedMarketplaces(allMarketplaces, checkboxes);
    await updateSettings({ marketplaces }, installationId);
    app.emit('snackbar:message', 'Settings saved');
  } catch (error) {
    app.emit('snackbar:error', error);
  }
  enableButton('save', 'Save');
};

export const chartPage = async (type) => {
  hideComponent('app');
  showComponent('loader');
  const settings = await getSettings();
  const chartData = await getChart(type);
  const chart = prepareChart(chartData);
  const marketplaces = prepareMarketplaces(settings.marketplaces);
  hideComponent('loader');
  showComponent('app');
  renderChart(chart);
  renderMarketplaces(marketplaces);
};

export const settings = async (app) => {
  if (!app) return;
  try {
    await app.watch(
      '*',
      async (ctx) => {
        hideComponent('app');
        hideComponent('error');
        showComponent('loader');
        const allMarketplaces = await getMarketplaces(ctx.objectId);
        const { marketplaces: selectedMarketpaces } = await getSettings(ctx.objectId);
        const preparedMarketplaces = processMarketplaces(allMarketplaces, selectedMarketpaces);
        const marketplaces = prepareMarketplacesWithSwitch(preparedMarketplaces);
        renderMarketplaces(marketplaces);
        enableButton('save', 'Save');
        addEventListener('save', 'click', saveSettingsData.bind(null, app, ctx.objectId));
        showComponent('app');
      },
      { immediate: true },
    );
  } catch (error) {
    app.emit('snackbar:error', error);
    showComponent('error');
  }
  hideComponent('loader');
};
