const bent = require('bent');
const getStream = bent('https://e6ju084de8.execute-api.eu-west-2.amazonaws.com');

test('ping endpoint should return HTTP 200', async () => {
  let stream = await getStream('/mryszard/_ping')
  expect(stream.statusCode).toBe(200);
});
