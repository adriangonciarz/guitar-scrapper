### Usage
To run scrap on page, provide parameter `--w` with value from: `blocket, olx, mercatino, kleinanziegen, markplaats` 
```shell 
python3 main.py --w blocket
```
or `--a` for all websites
```shell
python3 main.py --a
```
Create a database
```shell
python3 main.py --create-database
```
Logging levels:
- debug
- info
- error
```shell
python3 --log-level error
```