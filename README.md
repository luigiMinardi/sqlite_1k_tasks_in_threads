# How to run it 

## Easy way

```bash
./run.sh
```
*If for some reason you don't have permission to run the script you probably need to `chmod +x` it yourself.*

## Manually run

### Create Virtual Environment

```bash
python -m venv .venv && source .venv/bin/activate
```
*if on windows, replace `.venv/bin/activate` with `.venv\Scripts\activate.bat`*

### Install dependecies

```bash
pip install --upgrade pip && pip install -r requirements.txt --ignore-installed
```

### Run the script

```bash
./main.py
```
*If for some reason you don't have permission to run the script you probably need to `chmod +x` it yourself.*


# CLI Help

```bash
─────────────────────── Help ───────────────────────
-h or --help - Print this help
-w or --workers - [TYPE] integer - [DEFAULT] 10 - Define the ammount of workers (how many threads will be assigned).
-t or --tasks - [TYPE] integer - [DEFAULT] 1000 - Define the ammount of tasks that will run (how many users will be added to the db).
```
*The CLI args need to be exactly like on the help, you can't `-wt` or `-workers` for example, and you need to pass the integer when using `w` or `t` for it to work.*


