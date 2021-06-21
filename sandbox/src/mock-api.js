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
  res.set('Content-Type', 'application/json');
  res.send({'response':'This is the _ping API'});
});

app.get("/_status", (req, res) => {
  res.sendStatus(200);
});

app.get("/FHIR/R4/Observation", (req, res) => {
  const nhsNumberPattern = "^https:\/\/fhir[.]nhs[.]uk\/Id\/nhs-number[|]{1}[0-9]{10}$";
  let nhsNumber = new RegExp(nhsNumberPattern);

  if (!req.query["patient.identifier"] | !nhsNumber.test(req.query["patient.identifier"])) {
    res.sendStatus(400);
    return;
  } else {
    res.set('Content-Type', 'application/json');
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
              reference: `Patient/${req.query["patient.identifier"].split("|")[1]}`,
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/nhs-number",
                  value: req.query["patient.identifier"].split("|")[1],
                },
              ],
            },
            code: {
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
              identifier: {
                system: "https://fhir.nhs.uk/Id/Covid19-TestKit",
                value: "rtPCR"
              },
              display: "rtPCR"
            }
            // performer: {
            //   //ToDo: New field in the doc (New ticket is needed) (check if ticket is created with Richard) (different epic)
            // },
            // extension: {
            //   //ToDo: New field in the doc (New ticket is needed)
            // },
          },
          search: {
            mode: "match",
          },
        },
        {
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
              reference: "Patient/3fa85f64-5717-4562-b3fc-2c963f66afa6",
              type: "Patient",
              identifier: [
                {
                  system: "https://fhir.nhs.uk/Id/nhs-number",
                  value: req.query["patient.identifier"].split("|")[1],
                },
              ],
            },
            code: {
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
              identifier: {
                system: "https://fhir.nhs.uk/Id/Covid19-TestKit",
                value: "LFT"
              },
              display: "LFT"
            }
            // performer: {
            //   //ToDo: as above
            // },
            // extension: {
            //   //ToDo: as above
            // },
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
