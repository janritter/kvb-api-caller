from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
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

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
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
