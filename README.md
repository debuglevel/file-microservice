# File Microservice

Simple service to store/download/delete files via POST/GET/DELETE.

## Example usage

```bash
$ curl -X POST 'http://localhost:8080/files/' -H "Content-type: whatever/ddsdsds" --data-binary @1.jpg

{"content_length":13195,"content_type":"whatever/ddsdsds","size":13195,"uuid":"d283ec9f-fce6-47b4-91d6-ecf718794b50"}
```

```bash
$ curl -X GET 'http://localhost:8080/files/d283ec9f-fce6-47b4-91d6-ecf718794b50' -o 1_.jpg
```

```bash
$ curl -X PUT 'http://localhost:8080/files/d283ec9f-fce6-47b4-91d6-ecf718794b50' -H "Content-type: whatever2/ddsdsds" --data-binary @2.jpg
```

```bash
$ curl -vvv -X DELETE 'http://localhost:8080/files/d283ec9f-fce6-47b4-91d6-ecf718794b50'
```
