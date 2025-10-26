import os
import logging
import httpx
from otel_setup import (
    configure_tracing,
    configure_metrics,
    configure_logging,
    OtelEnvironment,
)
from dotenv import load_dotenv

load_dotenv()

otel_environment = OtelEnvironment(
    service_name=os.environ.get("OTEL_SERVICE_NAME"),
    service_version=os.environ.get("OTEL_SERVICE_VERSION"),
    otlp_endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"),
    deployment_environment=os.environ.get("OTEL_DEPLOYMENT_ENVIRONMENT"),
    insecure=True,
)

configure_logging(
    otel_environment=otel_environment,
    level="DEBUG",
)

tracer = configure_tracing(otel_environment=otel_environment)

meter_provider = configure_metrics(
    otel_environment=otel_environment, export_interval_ms=5000
)

meter = meter_provider.get_meter("business")

bytes_downloaded = meter.create_counter(
    "bytes_downloaded", unit="bytes", description="Total bytes downloaded"
)


def main():
    """Main function that performs an HTTP GET request to httpbin.org/get,
    tracks the downloaded bytes as a metric, and returns the JSON response."""
    with tracer.start_as_current_span("main"):
        logging.debug("Starting download")
        res = httpx.get("https://httpbin.org/get")
        content_bytes = len(res.content)
        bytes_downloaded.add(content_bytes)
        print(f"Downloaded {content_bytes} bytes")
        logging.debug("Finished download")
        return res.json()


if __name__ == "__main__":
    print(main())
