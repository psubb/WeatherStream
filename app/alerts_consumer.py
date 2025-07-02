import os
import json
import time
import smtplib
from email.message import EmailMessage
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Load config from .env

# Setup Kafka
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "weather-updates")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    consumer_timeout_ms=1000 # exit if no messages for 1 second
)

# Rain alert thresholds
PRECIP_PROB_THRESHOLD = float(os.getenv("PRECIP_PROB_THRESHOLD", 50))
PRECIP_AMOUNT_THRESHOLD = float(os.getenv("PRECIP_AMOUNT_THRESHOLD", 50))

# Email Setup
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.example.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", 587))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ALERT_FROM    = os.getenv("ALERT_FROM",  SMTP_USER)
ALERT_TO      = os.getenv("ALERT_TO",    "")

def send_email_alert(location: str, conds: dict):
    """
    Compose and send a simple email alert
    """
    subject = f"Rain Alert for {location.capitalize()}"
    body = (
        f"Rain expected for {location}!\n\n"
        f"Current Conditions:\n"
        f"  • Temp: {conds.get('temp')}°\n"
        f"  • Precip Prob: {conds.get('precipprob')}%\n"
        f"  • Expected Precip: {conds.get('precip')} inches\n\n"
        "Stay dry!\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = ALERT_FROM
    msg["To"]      = ALERT_TO
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
        print(f"[ALERT SENT] {location} (@{conds.get('precipprob')}%)")

def main():
    print(f"[STARTING] alerts consumer, listening to '{TOPIC}' on {KAFKA_BOOTSTRAP}")
    try:
        while True:
            for msg in consumer:
                value = msg.value
                loc   = value.get("location")
                data  = value.get("data", {})
                current = data.get("currentConditions", {})

                prob   = current.get("precipprob", 0.0)
                amount = current.get("precip",    0.0)

                # Check thresholds
                if prob >= PRECIP_PROB_THRESHOLD and amount >= PRECIP_AMOUNT_THRESHOLD:
                    print(f"[TRIGGER] {loc}: prob={prob}, amount={amount}")
                    send_email_alert(loc, current)
                else:
                    print(f"[SKIP]    {loc}: prob={prob}, amount={amount}")

            # If we hit consumer_timeout, sleep a bit then re-poll
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] consumer interrupted, exiting.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
