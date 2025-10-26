# py-otel-samples

This repository contains sample applications demonstrating the use of OpenTelemetry (OTEL) in Python for observability, including tracing, metrics, and logging. The samples showcase integration with HTTP clients like `httpx` to provide end-to-end visibility into your applications.

## Features

- **Tracing**: Automatic tracing of HTTP requests and responses using OpenTelemetry.
- **Metrics**: Collection of custom metrics, such as bytes downloaded from HTTP responses.
- **Logging**: Structured logging with OTLP export for centralized log management.
- **OTLP Export**: Support for exporting telemetry data to OTLP-compatible backends (e.g., Jaeger, Zipkin, Prometheus).
- **Easy Configuration**: Environment-based configuration for service settings, OTLP endpoints, and security options.
- **Instrumentation**: Pre-instrumented HTTP client for seamless observability.

## Prerequisites

- Python 3.13 or higher
- An OTLP-compatible observability backend (e.g., Jaeger, OpenTelemetry Collector) for collecting telemetry data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/farooq-teqniqly/py-otel-samples.git
   cd py-otel-samples
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Configure the following environment variables to customize OpenTelemetry behavior:

- `OTEL_SERVICE_NAME`: The name of your service (default: "unknown service").
- `OTEL_SERVICE_VERSION`: The version of your service (default: "1.0.0").
- `OTEL_EXPORTER_OTLP_ENDPOINT`: The OTLP endpoint URL (default: "http://localhost:4317").
- `OTEL_DEPLOYMENT_ENVIRONMENT`: The deployment environment (e.g., "dev", "staging", "prod") (default: "dev").
- `OTEL_INSECURE`: Set to "TRUE" for insecure OTLP connections (default: false, uses TLS).

You can set these in a `.env` file at the root of the project. The samples automatically load from `.env`.

## Usage

### Setting up a Local OTLP Backend (Optional)

For local development, you can quickly start the .NET Aspire standalone dashboard as an OTLP-compatible backend:

```bash
docker run -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard-standalone mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

This runs the dashboard UI on `http://localhost:18888` and accepts OTLP telemetry on `http://localhost:4317`.

### Running the HTTPX Sample

The `otel_httpx.py` script demonstrates making an HTTP request to `https://httpbin.org/get` with full telemetry instrumentation, including tracing, metrics, and logging.

1. Ensure your OTLP backend is running (e.g., start an OpenTelemetry Collector or Jaeger instance).

2. Run the sample:

   ```bash
   python otel_httpx.py
   ```

   This will:
   - Make a GET request to `https://httpbin.org/get`.
   - Create traces for the request/response.
   - Record metrics for bytes downloaded.
   - Log debug and error messages.
   - Export all telemetry data to the configured OTLP endpoint.

3. View the output in your observability backend.

### Customizing and Extending

- **Tracing**: Use `tracer.start_as_current_span()` to wrap your code blocks for custom tracing.
- **Metrics**: Create counters, gauges, or histograms using the `meter` object.
- **Logging**: Use standard Python logging; the configured handler will export logs via OTLP.
- **Instrumentation**: The `otel_setup.py` module provides reusable functions for setting up telemetry in your own applications.

## Project Structure

- `otel_httpx.py`: Sample application using `httpx` with OpenTelemetry instrumentation.
- `otel_setup.py`: Reusable module for configuring OpenTelemetry tracing, metrics, and logging.
- `requirements.txt`: Python dependencies.
- `README.md`: This documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements, bug fixes, or new samples.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
