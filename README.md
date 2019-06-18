# eve2test
Script to convert eve.json into test.yaml file. This currently implements the functionality of creating the "checks" block in `test.yaml` from a given `eve.json`. You can add other configuration in the file thus created.

## Usage
```
└─ $ ▶ ./bin/eve2test -h
usage: eve2test [-h] [--eventtype-only] [--allow-events [ALLOW_EVENTS]]
                <path-to-eve> <output-path>

Convert eve.json to test.yaml

positional arguments:
  <path-to-eve>         Path to eve.json
  <output-path>         Path to the folder where generated test.yaml should be
                        put

optional arguments:
  -h, --help            show this help message and exit
  --eventtype-only      Create filter blocks based on count of event types only
  --allow-events [ALLOW_EVENTS]
                        Create filter blocks for the specified events
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

You can also opt to create filters based on count of event types only. That will generate a rather compact test.yaml as follows. Please note that this creates filters only for the number of different event types.

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

Another option for filter is to allow checks for certain event types only.
On running
```
└─ $ ▶ ./bin/eve2test eve.json ./test.yaml --allow-events alert,tls
```

the content of `test.yaml` looks like
```
checks:
- filter:
    count: 1
    match:
      dest_ip: 192.168.56.101
      dest_port: 443
      event_type: tls
      pcap_cnt: 47
      proto: TCP
      src_ip: 192.168.56.1
      src_port: 49368
      tls:
        fingerprint: 3a:0b:3b:23:15:2c:44:5c:27:ac:6a:0c:41:d6:fa:74:af:b4:09:5b
        issuerdn: C=FR, ST=IDF, L=Paris, O=Stamus, CN=SELKS
        ja3: {}
        ja3s: {}
        notafter: '2025-02-09T18:07:27'
        notbefore: '2015-02-12T18:07:27'
        serial: 00:97:E6:47:09:8E:EA:C9:B4
        subject: C=FR, ST=IDF, L=Paris, O=Stamus, CN=SELKS
        version: TLS 1.2
- filter:
    count: 1
    match:
      alert:
        action: allowed
        category: ''
        gid: 1
        rev: 1
        severity: 3
        signature: Stamus TLS
        signature_id: 1
      app_proto: tls
      dest_ip: 192.168.56.1
      dest_port: 49368
      event_type: alert
      flow:
        bytes_toclient: 1821
        bytes_toserver: 644
        pkts_toclient: 4
        pkts_toserver: 5
        start: 2015-03-06T19:12:25.787108+0000
      pcap_cnt: 49
      proto: TCP
      src_ip: 192.168.56.101
      src_port: 443
      tls:
        fingerprint: 3a:0b:3b:23:15:2c:44:5c:27:ac:6a:0c:41:d6:fa:74:af:b4:09:5b
        issuerdn: C=FR, ST=IDF, L=Paris, O=Stamus, CN=SELKS
        ja3: {}
        ja3s: {}
        notafter: '2025-02-09T18:07:27'
        notbefore: '2015-02-12T18:07:27'
        serial: 00:97:E6:47:09:8E:EA:C9:B4
        subject: C=FR, ST=IDF, L=Paris, O=Stamus, CN=SELKS
        version: TLS 1.2
      tx_id: 0
- filter:
    count: 1
    match:
      dest_ip: 192.168.56.101
      dest_port: 443
      event_type: tls
      pcap_cnt: 99
      proto: TCP
      src_ip: 192.168.56.1
      src_port: 49369
      tls:
        ja3: {}
        ja3s: {}
        session_resumed: true
        version: TLS 1.2
```
