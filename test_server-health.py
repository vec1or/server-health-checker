from server_health import evaluate_health, check_http, save_report, collect_metrics, parse_arguments
import requests
import json

def test_parse_arguments_defaults(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["server_health.py"]
    )

    args = parse_arguments()

    assert args.url == "http://127.0.0.1"
    assert args.cpu_threshold == 80
    assert args.memory_threshold == 80
    assert args.disk_threshold == 90
    assert args.timeout == 5
    assert args.output == "server_health.json"
    
def test_collect_metrics():
    result = collect_metrics()

    assert "cpu_percent" in result
    assert "memory_percent" in result
    assert "disk_percent" in result
    
def test_healthy_server():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 30,
        "disk_percent": 40
    }

    http_status = {
        "status": "UP"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == []


def test_high_cpu():
    metrics = {
        "cpu_percent": 95,
        "memory_percent": 30,
        "disk_percent": 40
    }

    http_status = {
        "status": "UP"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == ["High CPU usage"]
    
def test_http_down():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 30,
        "disk_percent": 40
    }

    http_status = {
        "status": "DOWN"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == ["HTTP is down"]
    
def test_high_memory():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 95,
        "disk_percent": 40
    }

    http_status = {
        "status": "UP"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == ["High memory usage"]


def test_high_disk():
    metrics = {
        "cpu_percent": 20,
        "memory_percent": 30,
        "disk_percent": 95
    }

    http_status = {
        "status": "UP"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == ["High disk usage"]
    
def test_check_http_success(monkeypatch):
    class FakeResponse:
        status_code = 200

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr("server_health.requests.get", fake_get)

    result = check_http("http://127.0.0.1", 5)

    assert result == {
        "status_code": 200,
        "status": "UP"
    }
    
def test_check_http_failure_status(monkeypatch):
    class FakeResponse:
        status_code = 500

    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr("server_health.requests.get", fake_get)

    result = check_http("http://127.0.0.1", 5)

    assert result == {
        "status_code": 500,
        "status": "DOWN"
    }
    
def test_check_http_connection_error(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError("Connection failed")

    monkeypatch.setattr("server_health.requests.get", fake_get)

    result = check_http("http://127.0.0.1", 5)

    assert result["status_code"] is None
    assert result["status"] == "DOWN"
    assert "Connection failed" in result["error"]
    
def test_save_report(tmp_path):
    report = {
        "status": "HEALTHY",
        "problems": []
    }

    output_file = tmp_path / "report.json"

    save_report(report, output_file)

    with open(output_file, "r", encoding="utf-8") as file:
        saved = json.load(file)

    assert saved == report
    
def test_multiple_problems():
    metrics = {
        "cpu_percent": 95,
        "memory_percent": 90,
        "disk_percent": 95
    }

    http_status = {
        "status": "DOWN"
    }

    problems = evaluate_health(
        metrics,
        http_status,
        80,
        80,
        90
    )

    assert problems == [
        "High CPU usage",
        "High memory usage",
        "High disk usage",
        "HTTP is down"
    ]
    
def test_check_http_timeout(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr("server_health.requests.get", fake_get)

    result = check_http("http://127.0.0.1", 5)

    assert result["status"] == "DOWN"
    assert "Request timed out" in result["error"]