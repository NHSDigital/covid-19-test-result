provider "apigee" {
  org          = var.apigee_organization
  access_token = var.apigee_token
}

terraform {
  backend "azurerm" {}

  required_providers {
    apigee = "~> 0.0"
    archive = "~> 1.3"
  }
}


module "covid-19-test-result" {
  source                   = "github.com/NHSDigital/api-platform-service-module"
  name                     = "covid-19-test-result"
  path                     = "covid-19-test-result"
  apigee_environment       = var.apigee_environment
  proxy_type               = (var.force_sandbox || length(regexall("sandbox", var.apigee_environment)) > 0) ? "sandbox" : "live"
  namespace                = var.namespace
  make_api_product         = !(length(regexall("sandbox", var.apigee_environment)) > 0)
  api_product_display_name = length(var.namespace) > 0 ? "covid-19-test-result${var.namespace}" : "COVID-19 Test Result API"
  api_product_description  = "This API will return a list of antibody and antigen (PCR and LFT) COVID-19 test results for a given citizen based on NHS number and optionally verified by additional demographic data."
}
