# KVB API caller

This is a small application calling the [KVB API](https://github.com/janritter/kvb-api) to demonstrate distributed tracing with OpenTelemetry and Jaeger

## Setup

### Create venv

```bash
python3 -m venv env
```

### Activate venv

```bash
source ./env/bin/activate
```

### Install requirements

```bash
pip3 install -r requirements.txt
```

## Usage

1. Start the [KVB API](https://github.com/janritter/kvb-api) on localhost:8080
2. Start a locally running Jaeger or adapt Jager configuration in `app.py`
3. Start the kvb-api-caller via `python3 app.py`
