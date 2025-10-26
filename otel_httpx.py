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

otel_insecure_env_var = os.environ.get("OTEL_INSECURE")

otel_insecure = (
    otel_insecure_env_var is not None and otel_insecure_env_var.upper() == "TRUE"
)

otel_environment = OtelEnvironment(
    service_name=os.environ.get("OTEL_SERVICE_NAME", "unknown service"),
    service_version=os.environ.get("OTEL_SERVICE_VERSION", "1.0.0"),
    otlp_endpoint=os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
    ),
    deployment_environment=os.environ.get("OTEL_DEPLOYMENT_ENVIRONMENT", "dev"),
    insecure=otel_insecure,
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

logger = logging.getLogger(__name__)


def main():
    """Main function that performs an HTTP GET request to httpbin.org/get,
    tracks the downloaded bytes as a metric, and returns the JSON response."""
    with tracer.start_as_current_span("main"):
        logger.debug("Starting download")

        try:
            res = httpx.get("https://httpbin.org/get", timeout=5)
            res.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise

        content_bytes = len(res.content)
        bytes_downloaded.add(content_bytes)
        print(f"Downloaded {content_bytes} bytes")

        logger.debug("Finished download")

        return res.json()


if __name__ == "__main__":
    print(main())
