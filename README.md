# eve2test
Script to convert eve.json into test.yaml file.

## Usage
```
└─ $ ▶ ./bin/eve2test data/f_event_type_eve.json .
```

## Sample Output
TODO: Redirect output to file. For now, the output on console would look like
the following.

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
