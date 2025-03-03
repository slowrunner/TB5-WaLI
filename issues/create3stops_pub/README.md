# Republisher Stops Publishing


## Requested mod:
- /etc/systemd/logind.conf
  - uncomment ```#RemoveIPC=yes```
  - change to ```RemoveIPC=no```
- reboot


### Get Create3 Log:

```
 curl -o 2025-03-03_create3.log 10.0.0.178:8080/logs-raw
```

### Get RPi Log Since Boot

journalctl -b > 2025-03-03_RPi.log
