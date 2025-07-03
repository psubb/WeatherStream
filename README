# WeatherStream

**A real-time weather monitoring platform with intelligent precipitation alerts**

WeatherStream is a microservice-based weather monitoring system that fetches live weather data, implements intelligent caching strategies, and delivers automated email notifications for high precipitation probability events. Built with a decoupled architecture using Apache Kafka for event-driven communication between services.

## Key Features

- **Real-time Weather Data**: Integrates with Visual Crossing Weather API for current conditions and forecasts
- **Intelligent Caching**: Redis-powered caching system reduces API calls and improves response times
- **Event-Driven Architecture**: Kafka message broker enables loose coupling between services
- **Smart Precipitation Alerts**: Configurable thresholds for rain probability and amount detection
- **Fault-Tolerant Design**: Graceful handling of service unavailability with retry mechanisms
- **Containerized Deployment**: Complete Docker Compose setup for local development and testing

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Weather API   │    │     Apache      │    │  Alert Service  │
│   (Flask)       │───▶│     Kafka       │───▶│   (Consumer)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         ▼                                              ▼
┌─────────────────┐                            ┌─────────────────┐
│     Redis       │                            │  SMTP Email     │
│    (Cache)      │                            │   Delivery      │
└─────────────────┘                            └─────────────────┘
```

The system follows a microservice architecture with clear separation of concerns:

- **Weather API Service**: Flask-based REST API that fetches, caches, and publishes weather data
- **Alert Consumer Service**: Kafka consumer that processes weather updates and sends notifications
- **Message Broker**: Kafka handles asynchronous communication between services
- **Caching Layer**: Redis provides fast data retrieval and reduces external API calls

## Technology Stack

**Backend & Runtime**
- **Python 3.13** - Core programming language
- **Flask** - Lightweight web framework for API service
- **Apache Kafka** - Distributed event streaming platform
- **Redis** - In-memory data structure store for caching

**Key Libraries**
- **kafka-python** - Kafka client for Python
- **redis-py** - Redis client library
- **requests** - HTTP library for external API calls
- **python-dotenv** - Environment variable management

**Infrastructure**
- **Docker & Docker Compose** - Containerization and orchestration
- **Visual Crossing Weather API** - External weather data source
- **SMTP** - Email notification delivery

## Prerequisites

- Docker and Docker Compose installed
- Visual Crossing Weather API key ([Get one here](https://www.visualcrossing.com/weather-api))
- SMTP credentials for email notifications

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd weatherstream
   ```

2. **Configure environment variables**
   Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` with your actual values:
   ```env
   # Weather API Configuration
   API_KEY=your_visual_crossing_api_key
   
   # Redis & Kafka Settings
   REDIS_HOST=redis
   KAFKA_BOOTSTRAP=kafka:9092
   KAFKA_TOPIC=weather-updates
   
   # Alert Thresholds
   PRECIP_PROB_THRESHOLD=50
   PRECIP_AMOUNT_THRESHOLD=0.0
   
   # SMTP Email Configuration
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ALERT_FROM=your_email@gmail.com
   ALERT_TO=recipient@example.com
   ```

3. **Start the services**
   ```bash
   docker-compose up --build
   ```

4. **Test the API**
   ```bash
   curl http://localhost:8000/weather-api/san_francisco
   ```

## API Usage

### Get Weather Data
```bash
GET /weather-api/{location}
```

**Example Request:**
```bash
curl http://localhost:8000/weather-api/new_york
```

**Example Response:**
```json
{
  "resolvedAddress": "New York, NY, United States",
  "days": [
    {
      "datetime": "2025-07-02",
      "hours": [
        {
          "datetime": "00:00:00",
          "temp": 72.5,
          "precipprob": 15,
          "precip": 0.0,
          "pressure": 30.1,
          "visibility": 10.0
        }
      ]
    }
  ],
  "currentConditions": {
    "temp": 74.2,
    "precipprob": 20,
    "precip": 0.0,
    "pressure": 30.15,
    "visibility": 10.0
  }
}
```

## Configuration

### Alert Thresholds
Customize precipitation alert sensitivity in your `.env` file:
- `PRECIP_PROB_THRESHOLD`: Minimum rain probability percentage (default: 50)
- `PRECIP_AMOUNT_THRESHOLD`: Minimum precipitation amount in inches (default: 0.0)

### Cache Settings
Weather data is cached in Redis for 24 hours (86400 seconds) to optimize API usage and response times.

## Development

### Running Tests
```bash
# Test the weather API endpoint
python tests/test_weather_api.py
```

### Local Development
For development without Docker:
```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis and Kafka locally, then run:
python app/weather_api.py
python alerts/alerts_consumer.py
```

## Technical Highlights

### Fault-Tolerant Kafka Integration
The system implements lazy-initialized Kafka producers and consumers with retry logic, allowing services to start gracefully even when Kafka is temporarily unavailable.

```python
def get_producer():
    global _producer
    if _producer is None:
        for attempt in range(10):
            try:
                _producer = KafkaProducer(
                    bootstrap_servers='kafka:9092',
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                break
            except errors.NoBrokersAvailable:
                time.sleep(1)
    return _producer
```

### Intelligent Data Filtering
Weather API responses are automatically filtered to include only relevant meteorological data, reducing bandwidth and improving cache efficiency.

### Event-Driven Architecture
The decoupled design allows for easy extension with additional services (analytics, dashboards, mobile notifications) without modifying existing components.

## Project Structure

```
weatherstream/
├── alerts/
│   ├── alerts_consumer.py     # Kafka consumer for alerts
│   └── Dockerfile.alerts      # Alert service container
├── app/
│   ├── weather_api.py         # Flask API service
│   └── weather_client.py      # Weather API client
├── tests/
│   └── test_weather_api.py    # API tests
├── .env                       # Environment configuration
├── .gitignore                 # Git ignore rules
├── docker-compose.yml         # Multi-service orchestration
├── Dockerfile.web             # Web service container
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## Deployment

The application is containerized and ready for deployment on any Docker-compatible platform. The `docker-compose.yml` file orchestrates all services including Kafka, Zookeeper, Redis, and the custom application services.

For production deployment, consider:
- Using managed Kafka and Redis services
- Implementing proper secrets management
- Adding health checks and monitoring
- Setting up CI/CD pipelines

## Contributing

This project demonstrates modern software engineering practices including microservice architecture, event-driven design, containerization, and comprehensive documentation. It showcases skills relevant to backend development, distributed systems, and DevOps practices.