
/*
Copyright (c) 2022, CloudBlue LLC
All rights reserved.
*/
// API calls to the backend
export const getSettings = (installationId) => {
  const url = installationId !== undefined ? `/api/admin/${installationId}/settings` : '/api/settings';

  return fetch(url).then((response) => response.json());
};

export const getChart = (type) => fetch(`/api/chart?type=${type}`).then((response) => response.json());

export const getMarketplaces = (installationId) => {
  const url = installationId !== undefined ? `/api/admin/${installationId}/marketplaces` : '/api/marketplaces';

  return fetch(url).then((response) => response.json());
};

export const updateSettings = (settings, installationId) => {
  const url = installationId !== undefined ? `/api/admin/${installationId}/settings` : '/api/settings';

  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  }).then((response) => response.json());
};

// data processing
export const processMarketplaces = (
  allMarketplaces,
  selectedMarketplaces,
) => allMarketplaces.map((marketplace) => {
  const checked = !!selectedMarketplaces.find(
    (selectedMarketplace) => selectedMarketplace.id === marketplace.id,
  );

  return { ...marketplace, checked };
});

export const processSelectedMarketplaces = (
  allMarketplaces,
  checkboxes,
) => checkboxes.map((checkbox) => allMarketplaces.find(
  (marketplace) => marketplace.id === checkbox.value,
));

export const processCheckboxes = (
  checkboxes,
) => Array.from(checkboxes).filter(checkbox => checkbox.checked);
