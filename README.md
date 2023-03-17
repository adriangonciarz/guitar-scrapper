### Usage
To run scrap on page, provide parameter `--website` with value from: 
- blocket, 
- olx, 
- mercatino, 
- kleinanziegen, 
- markplaats`,
- zikinf,
- guitarristas

```shell 
python3 main.py --website blocket
```
or `--a` for all websites
```shell
python3 main.py --all
```
Create a database
```shell
python3 main.py --create-database
```
mode is used only for a purpose of db schema creation


Logging levels:
- debug
- info
- error
```shell
python3 --log-level error
```