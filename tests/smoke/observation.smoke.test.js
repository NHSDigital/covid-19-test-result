const bent = require('bent');
const getJSON = bent('json')
const getStream = bent('https://e6ju084de8.execute-api.eu-west-2.amazonaws.com');

test('observations endpoint should return HTTP 200 with correct data', async () => {
  let stream = await getStream('/mryszard/observations?patient=0000000001')
  const obj = await stream.json();
  expect(stream.statusCode).toBe(200);
  expect(obj.total).toBe(19);
  expect(obj.entry.length).toBe(19);
  expect(obj.entry[0].resourceType).toBe("Observation");
  expect(obj.entry[0].subject.reference).toBe("Patient/firstName1-lastName1");
  expect(obj.entry[0].identifier[0].value).toBe("ZZZ00000001");
  expect(obj.entry[0].device.identifier.value).toBe("LFT");

});
