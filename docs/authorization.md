# Authorization

```python
from simple_drive import Auth
```

## Use a Service Account

With a Service Account file:

```python
auth = Auth.from_service_account_file(file='service_account.json')
```

With a Service Account info as dict:

```
auth = Auth.from_service_account_info(info)
```

## Use a Client Secrets

```python
auth = Auth.local_web_server(client_secrets_file='client_secrets.json')
```
