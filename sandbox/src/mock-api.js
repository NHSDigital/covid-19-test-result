"use strict";

const express = require("express");

// Constants
const PORT = 9000;
const HOST = "0.0.0.0";

// App
const app = express();

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

app.get("/_ping", (req, res) => {
  res.send({});
});

app.get("/_status", (req, res) => {
  res.sendStatus(200);
});

app.get("/observation", (req, res) => {
  const nhsNumberPattern = "^https:\/\/fhir[.]nhs[.]uk\/Id\/nhs-number[|]{1}[0-9]{10}$";
  let nhsNumber = new RegExp(nhsNumberPattern);

  if (!req.query["patient.identifier"] | !nhsNumber.test(req.query["patient.identifier"])) {
    res.sendStatus(400);
  }

  const nhsNumberNotFoundPattern = "^https:\/\/fhir.nhs.uk\/Id\/nhs-number[|]1000000000$";
  let nhsNumberNotFound = new RegExp(nhsNumberNotFoundPattern);

  if (req.query["patient.identifier"] & nhsNumberNotFound.test(req.query["patient.identifier"])) {
    let responseBody = {
      resourceType: "Bundle",
      id: "1a420b58-5b91-4706-9a7c-90028ca79ff3",
      type: "searchset",
      total: 0,
      entry: [],
    };
  
    res.send(responseBody);
  } else {
    let responseBody = {
      resourceType: "Bundle",
      id: "1a420b58-5b91-4706-9a7c-90028ca79ff3",
      meta: {
        lastUpdated: "2021-01-20T12:46:07.830+00:00",
      },
      type: "searchset",
      total: 2,
      entry: [
        {
          fullUrl:
            "https://test-results-api.nhs.uk/R4/Observation/eb89a392-5b20-11eb-ae93-0242ac130002", //ToDo: Check if it was removed from the real API
          resource: {
            resourceType: "Observation",
            id: "ASD32145123",
            identifier: [
              {
                system: "https://fhir.nhs.uk/Id/SpecimenId",
                value: "ASD32145123",
              },
            ],
            status: "final",
            subject: {
              reference: "Patient/3fa85f64-5717-4562-b3fc-2c963f66afa6", //ToDo: Change value to Patient/DPSsubjectId
              type: "Patient", //ToDo: Missing in the real API
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/nhs-number",
                  value: req.query.patient,
                },
              ],
            },
            code: { //ToDo: Missing field. Must be added to the real API (New ticket is needed) (code=871552002 (antibody test) or code=871562009 (antigen test))
              coding: [{
                system: "http://snomed.info/sct",
                code: "871562009",
                display: "Detection of Severe acute respiratory syndrome coronavirus 2 (observable entity)"
              }]  
            },
            effectiveDateTime: "2020-09-23T13:00:08.476+00:00",
            valueCodeableConcept: {
              coding: [
                {
                  system: "http://snomed.info/sct",
                  code: "1240581000000104",
                  display:
                    "SARS-CoV-2 (severe acute respiratory syndrome coronavirus 2) detection result positive",
                },
              ],
              text: "SARS-CoV-2-ORGY",
            },
            method: {
              coding: [
                {
                  system: "http://snomed.info/sct",
                  code: "1240471000000102",
                  display:
                    "Measurement of Severe acute respiratory syndrome coronavirus 2 antigen (observable entity)",
                },
              ],
            },
            device: {
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/Covid19-TestKit",
                  value: "LFT",
                  display: "Lateral Flow Test",
                },
              ],
            },
            performer: {
              //ToDo: New field in the doc (New ticket is needed) (check if ticket is created with Richard) (different epic)
            },
            extension: {
              //ToDo: New field in the doc (New ticket is needed)
            },
          },
          search: {
            mode: "match",
          },
        },
        {
          fullUrl:
            "https://test-results-api.nhs.uk/R4/Observation/05ac9ea0-5b21-11eb-ae93-0242ac130002", //ToDo: Check if it was removed from the real API
          resource: {
            resourceType: "Observation",
            id: "05ac9ea0-5b21-11eb-ae93-0242ac130002",
            identifier: [
              {
                system: "https://fhir.nhs.uk/Id/SpecimenId",
                value: "ASD32145127",
              },
            ],
            status: "final",
            subject: {
              reference: "Patient/3fa85f64-5717-4562-b3fc-2c963f66afa6", //ToDo: Change value to Patient/DPSsubjectId
              type: "Patient", //ToDo: Missing in the real API
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/nhs-number",
                  value: req.query.patient,
                },
              ],
            },
            code: { //ToDo: Missing field. Must be added to the real API (New ticket is needed)
              coding: [{
                system: "http://snomed.info/sct",
                code: "871562009",
                display: "Detection of Severe acute respiratory syndrome coronavirus 2 (observable entity)"
              }]  
            },
            effectiveDateTime: "2020-09-23T13:00:08.476+00:00",
            valueCodeableConcept: {
              coding: [
                {
                  system: "http://snomed.info/sct",
                  code: "1240581000000104",
                  display:
                    "SARS-CoV-2 (severe acute respiratory syndrome coronavirus 2) detection result positive",
                },
              ],
              text: "SARS-CoV-2-ORGY",
            },
            method: {
              coding: [
                {
                  system: "http://snomed.info/sct",
                  code: "1240471000000102",
                  display:
                    "Measurement of Severe acute respiratory syndrome coronavirus 2 antigen (observable entity)",
                },
              ],
            },
            device: {
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/Covid19-TestKit",
                  value: "LFT",
                  display: "Lateral Flow Test",
                },
              ],
            },
            performer: {
              //ToDo: New field in the doc (New ticket is needed)
            },
            extension: {
              //ToDo: New field in the doc (New ticket is needed)
            },
          },
          search: {
            mode: "match",
          },
        },
      ],
    };

    res.send(responseBody);
  }
});
