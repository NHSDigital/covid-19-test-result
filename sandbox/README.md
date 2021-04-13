Commands run locally:

Build an image:
```
docker build -t {stage-name}/mock-api .
```

Run the image with publishing the 8080 port as 49160 out of docker container:
```
docker run -p {port}:8080 -d {stage-name}/mock-api
```

To list container:
```
docker ps
```

To see logs from container:
```
docker logs {containerId}
```

To test it:

```bash
curl -i localhost:{​​​​​​port}​​​​​​/_ping
curl -i localhost:{​​​​​​port}​​​​​​/_status
curl -i 'localhost:{​​​​​​port}​​​​​​/observartion?patient=123'
```
