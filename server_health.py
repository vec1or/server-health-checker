import psutil
import json
import requests
from datetime import datetime
import logging
import sys
import argparse

def setup_logging():
    logging.basicConfig(
        filename="server_health.log",
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    args = parse_arguments()

    setup_logging()

    logging.info("Health check started...")
    metrics = collect_metrics()

    logging.info(
        "Metrics collected: CPU=%s%% RAM=%s%% Disk=%s%%",
        metrics["cpu_percent"],
        metrics["memory_percent"],
        metrics["disk_percent"]
    )

    http_status = check_http(args.url, args.timeout)
    problems = evaluate_health(
        metrics,
        http_status,
        args.cpu_threshold,
        args.memory_threshold,
        args.disk_threshold
    )
    status = "UNHEALTHY" if problems else "HEALTHY"
    logging.info("Overall status: %s", status)

    if problems:
        logging.warning("Health check found problems: %s", problems)
    else:
        logging.info("System health is OK")

    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "http_request": http_status,
        "problems": problems,
        "status": status
    }

    save_report(report, args.output)

    logging.info("Health check finished with status: %s", status)
    print(report)

    if problems:
        sys.exit(1)
    else:
        sys.exit(0)
        
def save_report(report, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

def collect_metrics():
    cpu = psutil.cpu_percent(1)
    virtual_memory = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    return {
        "cpu_percent": cpu,
        "memory_percent": virtual_memory,
        "disk_percent": disk_usage
    }

def evaluate_health(
    metrics,
    http_status,
    cpu_threshold,
    memory_threshold,
    disk_threshold
):
    problems = []

    if metrics["cpu_percent"] > cpu_threshold:
        problems.append("High CPU usage")

    if metrics["memory_percent"] > memory_threshold:
        problems.append("High memory usage")

    if metrics["disk_percent"] > disk_threshold:
        problems.append("High disk usage")

    if http_status["status"] != "UP":
        problems.append("HTTP is down")

    return problems

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Check server health"
    )

    parser.add_argument(
        "--url",
        default="http://127.0.0.1",
        help="URL to check"
    )

    parser.add_argument(
        "--cpu-threshold",
        type=float,
        default=80,
        help="CPU usage threshold"
    )

    parser.add_argument(
        "--memory-threshold",
        type=float,
        default=80,
        help="Memory usage threshold"
    )

    parser.add_argument(
        "--disk-threshold",
        type=float,
        default=90,
        help="Disk usage threshold"
    )
    
    parser.add_argument(
        "--output",
        default="server_health.json",
        help="Path to output JSON report"
    )
    
    parser.add_argument(
        "--timeout",
        type=float,
        default=5,
        help="HTTP request timeout in seconds"
    )

    return parser.parse_args()

def check_http(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)

        if response.status_code == 200:
            logging.info("HTTP check is successful: %s", response.status_code)
            status = "UP"
        else:
            logging.warning("HTTP check ended with status code: %s", response.status_code)
            status = "DOWN"

        return {
            "status_code": response.status_code,
            "status": status
        }

    except requests.exceptions.RequestException as error:
        logging.error("HTTP check failed: %s", error)

        return {
            "status_code": None,
            "status": "DOWN",
            "error": str(error)
        }

if __name__ == "__main__":
    main()