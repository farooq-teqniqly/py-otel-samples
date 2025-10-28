"""OpenTelemetry setup utilities for configuring tracing, metrics, and
logging."""

from opentelemetry.sdk.resources import Resource
from dataclasses import dataclass


class OtelEnvironmentError(Exception):
    """Exception raised for errors related to OpenTelemetry environment
    configuration."""

    def __init__(self, message="An OtelEnvironment instance is required"):
        super().__init__(message)


@dataclass(frozen=True)
class OtelEnvironment:
    """Dataclass to hold configuration settings for OpenTelemetry
    environment."""

    service_name: str = "unknown service"
    service_version: str = "1.0.0"
    otlp_endpoint: str = "http://localhost:4317"
    deployment_environment: str = "dev"
    insecure: bool = False


def __create_resource(otel_environment) -> Resource:
    resource = Resource.create(
        {
            "service.name": otel_environment.service_name,
            "service.version": otel_environment.service_version,
            "deployment.environment": otel_environment.deployment_environment,
        }
    )
    return resource


def configure_logging(
    otel_environment: OtelEnvironment,
    level: str | int = "INFO",
):
    """Configure OpenTelemetry logging with OTLP exporter.

    Args:
        otel_environment (OtelEnvironment): Configuration for OpenTelemetry environment.
        level (str | int): Logging level. Defaults to "INFO".
    """
    if otel_environment is None:
        raise OtelEnvironmentError()

    import logging
    from opentelemetry._logs import set_logger_provider
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

    numeric = getattr(logging, level, level)

    resource = __create_resource(otel_environment)

    provider = LoggerProvider(resource=resource)
    set_logger_provider(provider)

    exporter = OTLPLogExporter(
        endpoint=otel_environment.otlp_endpoint, insecure=otel_environment.insecure
    )
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

    handler = LoggingHandler(level=logging.NOTSET, logger_provider=provider)
    root = logging.getLogger()
    root.setLevel(numeric)
    root.addHandler(handler)


def configure_metrics(
    otel_environment: OtelEnvironment,
    export_interval_ms: int = 60000,
):
    """Configure OpenTelemetry metrics with periodic OTLP exporter.

    Args:
        otel_environment (OtelEnvironment): Configuration for OpenTelemetry environment.
        export_interval_ms (int): Interval in milliseconds for exporting metrics. Defaults to 60000.

    Returns:
        MeterProvider: The configured meter provider.
    """
    if otel_environment is None:
        raise OtelEnvironmentError()

    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.metrics import set_meter_provider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,
    )

    resource = __create_resource(otel_environment)

    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint=otel_environment.otlp_endpoint, insecure=otel_environment.insecure
        ),
        export_interval_millis=export_interval_ms,
    )

    mp = MeterProvider(resource=resource, metric_readers=[reader])
    set_meter_provider(mp)

    return mp


def configure_tracing(otel_environment: OtelEnvironment):
    """Configure OpenTelemetry tracing with OTLP exporter.

    Args:
        otel_environment (OtelEnvironment): Configuration for OpenTelemetry environment.

    Returns:
        Tracer: The tracer for the service.
    """
    if otel_environment is None:
        raise OtelEnvironmentError()

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    resource = __create_resource(otel_environment)

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(
        endpoint=otel_environment.otlp_endpoint, insecure=otel_environment.insecure
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    return trace.get_tracer(otel_environment.service_name)
