// Creates an Azure AI resource with proxied endpoints for the Azure AI services provider

@description('Azure region of the deployment')
param location string

@description('Tags to add to the resources')
param tags object

@description('AI Foundry account name')
param aiFoundryName string

@description('AI Project name')
param aiProjectName string

@description('AI Project friendly name')
param aiProjectFriendlyName string

@description('AI Project description')
param aiProjectDescription string

//for constructing endpoint
// var subscriptionId = subscription().subscriptionId
// var resourceGroupName = resourceGroup().name

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: aiFoundryName
  scope: resourceGroup()
}

resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  name: aiProjectName
  parent: aiFoundry
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // organization
    displayName: aiProjectFriendlyName
    description: aiProjectDescription
  }
  tags: tags
}

var projectConnectionString = 'https://${aiFoundryName}.services.ai.azure.com/api/projects/${aiProjectName}'

output aiProjectName string = aiProject.name
output aiProjectResourceId string = aiProject.id
output aiProjectPrincipalId string = aiProject.identity.principalId
output aiProjectEndpoint string = 'https://${aiFoundryName}.services.ai.azure.com/'
output projectConnectionString string = projectConnectionString
