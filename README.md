# eve2test
Script to convert eve.json into test.yaml file. This currently implements the functionality of creating the "checks" block in `test.yaml` from a given `eve.json`. You can add other configuration in the file thus created.

## Usage
```
└─ $ ▶ ./bin/eve2test -h
usage: eve2test [-h] [--eventtype-only] <path-to-eve> <output-path>

Convert eve.json to test.yaml

positional arguments:
  <path-to-eve>     Path to eve.json
  <output-path>     Path to the folder where generated test.yaml should be put

optional arguments:
  -h, --help        show this help message and exit
  --eventtype-only  Create filter blocks based on alert types only
```

## Sample output file

On running the following command

```
└─ $ ▶ ./bin/eve2test eve.json ./test.yaml
```

A file `test.yaml` is create with the content as follows.

```
# *** Add configuration here ***

checks:
  - filter:
      count: 1
      match:
        event_type: alert
        src_ip: 192.168.2.7
        src_port: 1041
        dest_ip: 208.75.250.50
        dest_port: 80
        proto: TCP
        tx_id: 0
        alert:
          action: allowed
          gid: 1
          signature_id: 2001340
          rev: 9
          signature: "ET MALWARE LocalNRD Spyware Checkin (Original Sig Fails to Fire)"
          category: A Network Trojan was detected
          severity: 1
        app_proto: http
  - filter:
      count: 1
      match:
        event_type: alert
        src_ip: 192.168.2.7
        src_port: 1041
        dest_ip: 208.75.250.50
        dest_port: 80
        proto: TCP
        app_proto: http
        tx_id: 0
        alert:
          action: allowed
          gid: 1
          signature_id: 2001341
          rev: 9
          signature: "ET MALWARE LocalNRD Spyware Checkin (OISF changed to content fails also)"
          category: A Network Trojan was detected
          severity: 1

```

You can also opt to create filters based on event types only. That will generate a rather compact test.yaml as follows.

On running
```
└─ $ ▶ ./bin/eve2test eve.json ./test.yaml --eventtype-only
```

the content of `test.yaml` looks like
```
# *** Add configuration here ***

checks:
  - filter:
      count: 4
      match:
        event_type: alert
  - filter:
      count: 1
      match:
        event_type: http
```
