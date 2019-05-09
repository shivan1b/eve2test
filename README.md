# eve2test
Script to convert eve.json into test.yaml file.

## Usage
```
└─ $ ▶ ./bin/eve2test data/f_event_type_params_eve.json ./test.yaml
```

## Sample Output
Content of `test.yaml`

```
checks:
  - filter:
      count: 5
      match:
        event_type: tls
  - filter:
      count: 4
      match:
        event_type: alert
  - filter:
      count: 7
      match:
        event_type: flow
  - filter:
      count: 1
      match:
        event_type: stats
```
