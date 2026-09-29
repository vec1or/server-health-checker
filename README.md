# Server Health Checker

A Python CLI tool for monitoring basic Linux server health.

## Features

- CPU usage monitoring
- Memory usage monitoring
- Disk usage monitoring
- HTTP availability checks
- Configurable CPU, memory, and disk thresholds
- Configurable HTTP timeout
- JSON report generation
- Logging to a file
- Exit codes for automation
- Pytest test suite
- Test coverage with pytest-cov

## Project Structure

```text
server-health-checker/
├── server_health.py
├── test_server_health.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

The `.venv/` directory should not be committed to Git.

## Requirements

- Python 3.14+
- Linux
- pip
- Python virtual environment support

## Installation

Move into the project directory:

```bash
cd server-health-checker
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the health checker with the default settings:

```bash
python server_health.py
```

By default, the script checks:

- CPU usage
- Memory usage
- Disk usage
- HTTP availability of `http://127.0.0.1`

It generates:

- `server_health.json` — JSON health report
- `server_health.log` — log file

## Custom Options

You can customize the URL, thresholds, timeout, and output file:

```bash
python server_health.py \
  --url http://127.0.0.1 \
  --cpu-threshold 80 \
  --memory-threshold 80 \
  --disk-threshold 90 \
  --timeout 5 \
  --output server_health.json
```

Available options:

- `--url` — URL to check
- `--cpu-threshold` — maximum allowed CPU usage percentage
- `--memory-threshold` — maximum allowed memory usage percentage
- `--disk-threshold` — maximum allowed disk usage percentage
- `--timeout` — HTTP request timeout in seconds
- `--output` — path to the JSON report file

Display the built-in help:

```bash
python server_health.py --help
```

## Health Evaluation

The script reports the system as `UNHEALTHY` if any of the following conditions are met:

- CPU usage exceeds the configured CPU threshold
- Memory usage exceeds the configured memory threshold
- Disk usage exceeds the configured disk threshold
- The HTTP check does not return status code `200`
- The HTTP request fails

Otherwise, the overall status is reported as `HEALTHY`.

## Example JSON Output

```json
{
  "timestamp": "2026-09-29T16:30:10.123456",
  "metrics": {
    "cpu_percent": 3.2,
    "memory_percent": 28.4,
    "disk_percent": 17.1
  },
  "http_request": {
    "status_code": 200,
    "status": "UP"
  },
  "problems": [],
  "status": "HEALTHY"
}
```

## Logging

The script writes execution information to:

```text
server_health.log
```

Example log entries:

```text
2026-09-29 16:30:10,123 - INFO - Health check started...
2026-09-29 16:30:11,124 - INFO - Metrics collected: CPU=3.2% RAM=28.4% Disk=17.1%
2026-09-29 16:30:11,130 - INFO - HTTP check is successful: 200
2026-09-29 16:30:11,131 - INFO - Overall status: HEALTHY
2026-09-29 16:30:11,132 - INFO - System health is OK
2026-09-29 16:30:11,133 - INFO - Health check finished with status: HEALTHY
```

## Exit Codes

The script returns an exit code that can be used by automation tools such as cron, systemd, or CI/CD pipelines.

- `0` — server is healthy
- `1` — one or more health checks failed

Example:

```bash
python server_health.py
echo $?
```

## Testing

Run the complete test suite with:

```bash
pytest -v
```

The current test suite covers scenarios including:

- Healthy server state
- High CPU usage
- High memory usage
- High disk usage
- HTTP service failure
- Successful HTTP response
- HTTP error response
- Connection errors
- JSON report generation

## Test Coverage

Run tests with coverage reporting:

```bash
pytest --cov=server_health --cov-report=term-missing
```

The coverage report shows which lines of `server_health.py` were executed during the test suite and which lines are still not covered.

Current test status:

```text
9 passed
```

## Dependencies

The project uses:

- `psutil` — system CPU, memory, and disk metrics
- `requests` — HTTP availability checks
- `pytest` — automated testing
- `pytest-cov` — coverage reporting

Exact installed versions are stored in:

```text
requirements.txt
```

## .gitignore

Recommended entries:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.coverage
*.log
server_health.json
```

Runtime-generated files and the virtual environment should not be committed to Git.

## Future Improvements

Possible next steps:

- GitHub Actions CI
- Configurable log file path
- Structured JSON logging
- Additional service checks
- Alert integrations
- Scheduled execution with cron or systemd
- Packaging as an installable CLI tool
- Docker support

## Purpose

This project was created as a hands-on DevOps learning exercise focused on:

- Python automation
- Linux monitoring
- CLI development
- Logging
- JSON output
- Exit codes
- HTTP health checks
- Testing with pytest
- Preparing Python tools for CI/CD workflows
