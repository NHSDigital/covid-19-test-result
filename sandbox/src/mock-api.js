"use strict";

const express = require("express");

// Constants
const PORT = 8080;
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
  if (!req.query.patient) {
    res.sendStatus(400);
  }

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
          "https://test-results-api.nhs.uk/R4/Observation/eb89a392-5b20-11eb-ae93-0242ac130002",
        resource: {
          resourceType: "Observation",
          id: "eb89a392-5b20-11eb-ae93-0242ac130002",
          identifier: [
            {
              system: "urn:oid:",
              value: "eb89a392-5b20-11eb-ae93-0242ac130002",
            },
          ],
          status: "final",
          subject: {
            reference: "Patient/123456",
            identifier: [
              {
                system: "https://fhir.nhs.uk/Id/nhs-number",
                value: req.query.patient,
              },
            ],
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
        },
        search: {
          mode: "match",
        },
      },
      {
        fullUrl:
          "https://test-results-api.nhs.uk/R4/Observation/05ac9ea0-5b21-11eb-ae93-0242ac130002",
        resource: {
          resourceType: "Observation",
          id: "05ac9ea0-5b21-11eb-ae93-0242ac130002",
          identifier: [
            {
              system: "urn:oid:",
              value: "05ac9ea0-5b21-11eb-ae93-0242ac130002",
            },
          ],
          status: "final",
          subject: {
            reference: "Patient/123456",
            identifier: [
              {
                system: "https://fhir.nhs.uk/Id/nhs-number",
                value: "123456",
              },
            ],
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
        },
        search: {
          mode: "match",
        },
      },
    ],
  };

  res.send(responseBody);
});
