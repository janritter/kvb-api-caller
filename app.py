from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import requests


trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "kvb-api-caller"})
    )
)

span_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(span_exporter)
)

RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("kvb-api-request") as span:
    try:
        r = requests.get("http://localhost:8080/v1/departures/stations/bensberg")
        print(r.json())
    except Exception as e:
        span.record_exception(e)
        span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
        print(e)
