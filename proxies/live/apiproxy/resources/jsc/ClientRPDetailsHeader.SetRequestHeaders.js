var developerAppName = context.getVariable('developer.app.name');
var developerAppId = context.getVariable('developer.app.id');
var clientIP = context.getVariable('client.ip');
var proofingLevel = context.getVariable('custom.app.nhs-login-allowed-proofing-level');

var clientRpDetailsHeader = {
    "developer.app.name": developerAppName,
    "developer.app.id": developerAppId,
    "developer.app.nhs-login-minimum-proofing-level": proofingLevel,
    "client.ip": clientIP
};

context.targetRequest.headers['NHSD-Client-RP-Details'] = clientRpDetailsHeader;
