using 'main.bicep'

param tags = { 'azd-env-name': environmentName, CostControl: 'Ignore', SecurityControl: 'Ignore' }

param environmentName = 'dev-v2'
param location = 'eastus2'
param aiHubName = 'hub-${environmentName}'
param aiProjectName = 'project-${environmentName}'
param skipVnet = true

param principalId = '168a046a-c7e5-43fa-9c57-e26f27377ca5'
