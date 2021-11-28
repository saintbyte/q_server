# q_server


## Client
example:
```
python3 main.py --host=127.0.0.1 --request=CREATE --command=REVERSE --data=123456
```

```
python3 main.py --host=127.0.0.1 --request=STATUS --data=84d7f907-3eae-4893-942f-a4a3637ecea4
```

```
python3 main.py --host=127.0.0.1 --request=GET  --data=84d7f907-3eae-4893-942f-a4a3637ecea4
```

## server
```
python3 main.py
```
If needed set HOST and PORT env values
