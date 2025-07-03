import os
import json
import time
import smtplib
from email.message import EmailMessage
from kafka import KafkaConsumer, errors
from dotenv import load_dotenv

load_dotenv()

# Lazy initalize  
consumer = None

def get_consumer():
    """
    Return a singleton KafkaConsumer, retrying up to 10 times if the broker isn't ready.
    Never exits the process—returns None if still not connected.
    """
    global consumer
    if consumer is not None:
        return consumer

    bootstrap = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
    topic     = os.getenv("KAFKA_TOPIC",     "weather-updates")

    for attempt in range(1, 11):
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                consumer_timeout_ms=1000,
            )
            print(f"[KAFKA] consumer connected on attempt {attempt}")
            break
        except errors.NoBrokersAvailable:
            print(f"[KAFKA] broker not available, retry {attempt}/10…")
            time.sleep(1)

    if consumer is None:
        print("[KAFKA] still not available, will retry on next loop")
    return consumer

# Get thresholds from .env 
PRECIP_PROB_THRESHOLD   = float(os.getenv("PRECIP_PROB_THRESHOLD",   50))
PRECIP_AMOUNT_THRESHOLD = float(os.getenv("PRECIP_AMOUNT_THRESHOLD", 0.0))

# Email setting from .env
SMTP_HOST     = os.getenv("SMTP_HOST",     "smtp.example.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT",     587))
SMTP_USER     = os.getenv("SMTP_USER",     "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ALERT_FROM    = os.getenv("ALERT_FROM",    SMTP_USER)
ALERT_TO      = os.getenv("ALERT_TO",      "")

def send_email_alert(location: str, conds: dict):
    subject = f"Rain Alert for {location.capitalize()}"
    body = (
        f"🚨 Rain expected in {location}!\n\n"
        f"  • Temp:        {conds.get('temp')}°\n"
        f"  • Precip Prob: {conds.get('precipprob')}%\n"
        f"  • Precip Amt:  {conds.get('precip')} in\n\n"
        "Stay dry! ☔\n"
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
    print(f"[STARTING] alerts consumer (prob≥{PRECIP_PROB_THRESHOLD}%, amt≥{PRECIP_AMOUNT_THRESHOLD})")
    while True:
        c = get_consumer()
        if not c:
            # Kafka still unavailable—wait then retry
            time.sleep(2)
            continue

        # Process all available messages
        for msg in c:
            value   = msg.value or {}
            loc     = value.get("location", "unknown")
            data    = value.get("data", {})
            current = data.get("currentConditions", {})

            prob   = current.get("precipprob", 0.0)
            amount = current.get("precip",      0.0)

            if prob >= PRECIP_PROB_THRESHOLD and amount >= PRECIP_AMOUNT_THRESHOLD:
                print(f"[TRIGGER] {loc}: prob={prob}, amount={amount}")
                send_email_alert(loc, current)
            else:
                print(f"[SKIP]    {loc}: prob={prob}, amount={amount}")

        # No more messages: pause, then loop back and re-attempt get_consumer()
        time.sleep(1)

if __name__ == "__main__":
    main()
