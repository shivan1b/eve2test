# eve2test
Script to convert eve.json into test.yaml file.

## Usage
```
└─ $ ▶ ./bin/eve2test data/f_event_type_eve.json ./test.yaml
```

## Sample Output
Content of `test.yaml`

```
checks:
  - filter:
      count: 1
      match:
        event_type: alert
  - filter:
      count: 2
      match:
        event_type: drop
Success
```
