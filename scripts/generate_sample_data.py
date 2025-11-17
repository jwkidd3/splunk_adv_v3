#!/usr/bin/env python3
"""
Splunk Advanced Course - Sample Data Generator
Generates comprehensive sample data for all course labs
"""

import random
import json
from datetime import datetime, timedelta
import os
import sys

# Configuration
OUTPUT_DIR = "../data"
DAYS_OF_DATA = 30
EVENTS_PER_DAY = 10000

# Sample data pools
HOSTS = ["web-server-01", "web-server-02", "app-server-01", "app-server-02", "db-server-01"]
USERS = [f"user{i:04d}" for i in range(1, 501)]
FIRST_NAMES = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", "James", "Maria"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
DEPARTMENTS = ["Sales", "Engineering", "Marketing", "HR", "Finance", "Operations", "IT", "Support"]
EMAIL_DOMAINS = ["company.com", "example.com", "testcorp.com"]
PRODUCTS = ["ProductA", "ProductB", "ProductC", "ProductD", "ProductE"]
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
]
URL_PATHS = [
    "/api/users", "/api/products", "/api/orders", "/api/auth/login", "/api/auth/logout",
    "/api/search", "/api/dashboard", "/api/reports", "/api/analytics", "/api/settings",
    "/home", "/about", "/contact", "/products", "/checkout", "/cart", "/profile"
]
LOG_LEVELS = ["INFO", "WARN", "ERROR", "DEBUG", "TRACE"]
ERROR_MESSAGES = [
    "Connection timeout",
    "Database connection failed",
    "Invalid authentication credentials",
    "Resource not found",
    "Permission denied",
    "Service unavailable",
    "Internal server error",
    "Bad request format",
    "Rate limit exceeded",
    "Session expired"
]


def generate_ip():
    """Generate random IP address"""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"


def generate_timestamp(base_time):
    """Generate timestamp with some randomness"""
    offset = random.randint(0, 86400)  # Random seconds within a day
    return base_time + timedelta(seconds=offset)


def generate_web_logs(output_file, start_date, num_events):
    """Generate web server access logs"""
    print(f"Generating {num_events} web server log events...")

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            src_ip = generate_ip()
            user = random.choice(USERS) if random.random() > 0.3 else "-"
            method = random.choice(HTTP_METHODS)
            url = random.choice(URL_PATHS)

            # Status code distribution (mostly 200s, some errors)
            status_rand = random.random()
            if status_rand < 0.7:
                status = 200
            elif status_rand < 0.85:
                status = random.choice([301, 302, 304])
            elif status_rand < 0.95:
                status = random.choice([400, 401, 403, 404])
            else:
                status = random.choice([500, 502, 503, 504])

            # Response time (ms) - faster for successful requests
            if status < 400:
                response_time = random.randint(50, 500)
            else:
                response_time = random.randint(200, 2000)

            bytes_sent = random.randint(200, 50000)
            user_agent = random.choice(USER_AGENTS)

            # Apache Combined Log Format
            log_line = f'{src_ip} - {user} [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")}] ' \
                      f'"{method} {url} HTTP/1.1" {status} {bytes_sent} "-" "{user_agent}" {response_time}ms\n'

            f.write(log_line)


def generate_application_logs(output_file, start_date, num_events):
    """Generate application logs with various levels"""
    print(f"Generating {num_events} application log events...")

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            host = random.choice(HOSTS)
            level = random.choices(
                LOG_LEVELS,
                weights=[50, 20, 10, 15, 5],  # INFO most common
                k=1
            )[0]

            user_id = random.choice(USERS) if random.random() > 0.4 else None
            transaction_id = f"TXN-{random.randint(100000, 999999)}"

            # Generate message based on level
            if level == "ERROR":
                message = random.choice(ERROR_MESSAGES)
            elif level == "WARN":
                message = f"High response time detected: {random.randint(1000, 5000)}ms"
            else:
                message = f"Processing request for {random.choice(URL_PATHS)}"

            log_line = f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")} host={host} level={level} ' \
                      f'transaction_id={transaction_id} '

            if user_id:
                log_line += f'user_id={user_id} '

            log_line += f'message="{message}"\n'

            f.write(log_line)


def generate_authentication_logs(output_file, start_date, num_events):
    """Generate authentication/security logs"""
    print(f"Generating {num_events} authentication log events...")

    actions = ["login", "logout", "login_failed", "password_change", "session_timeout"]

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            user = random.choice(USERS)
            src_ip = generate_ip()
            action = random.choices(
                actions,
                weights=[40, 30, 15, 10, 5],
                k=1
            )[0]

            # Success rate based on action
            if action == "login_failed":
                status = "failure"
                reason = random.choice(["Invalid password", "Account locked", "User not found"])
            else:
                status = "success"
                reason = "-"

            session_id = f"sess_{random.randint(1000000, 9999999)}"

            log_line = f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")} ' \
                      f'action={action} user={user} src_ip={src_ip} ' \
                      f'status={status} session_id={session_id} reason="{reason}"\n'

            f.write(log_line)


def generate_sales_data(output_file, start_date, num_events):
    """Generate sales transaction data"""
    print(f"Generating {num_events} sales transaction events...")

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            customer_id = random.choice(USERS)
            product = random.choice(PRODUCTS)
            quantity = random.randint(1, 10)
            unit_price = random.uniform(10.0, 500.0)
            amount = quantity * unit_price

            # Tiered discount based on amount
            if amount > 10000:
                discount = 0.15
            elif amount > 5000:
                discount = 0.10
            elif amount > 1000:
                discount = 0.05
            else:
                discount = 0.0

            final_amount = amount * (1 - discount)

            log_line = f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")} ' \
                      f'customer_id={customer_id} product={product} ' \
                      f'quantity={quantity} unit_price={unit_price:.2f} ' \
                      f'amount={amount:.2f} discount={discount:.2f} ' \
                      f'final_amount={final_amount:.2f}\n'

            f.write(log_line)


def generate_user_data(output_file):
    """Generate user profile data (CSV lookup file)"""
    print("Generating user profile data...")

    with open(output_file, 'w') as f:
        # CSV header
        f.write("user_id,email,first_name,last_name,department,premium,created_date\n")

        for user in USERS:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(EMAIL_DOMAINS)}"
            department = random.choice(DEPARTMENTS)
            premium = "true" if random.random() > 0.7 else "false"
            created_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")

            f.write(f'{user},{email},{first_name},{last_name},{department},{premium},{created_date}\n')


def generate_performance_metrics(output_file, start_date, num_events):
    """Generate system performance metrics"""
    print(f"Generating {num_events} performance metric events...")

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            host = random.choice(HOSTS)

            cpu_usage = random.uniform(10.0, 95.0)
            memory_usage = random.uniform(20.0, 90.0)
            disk_usage = random.uniform(30.0, 85.0)
            network_in = random.uniform(0.1, 100.0)  # Mbps
            network_out = random.uniform(0.1, 100.0)

            log_line = f'{timestamp.strftime("%Y-%m-%d %H:%M:%S")} ' \
                      f'host={host} metric_type=system_performance ' \
                      f'cpu_usage={cpu_usage:.2f} memory_usage={memory_usage:.2f} ' \
                      f'disk_usage={disk_usage:.2f} network_in={network_in:.2f} ' \
                      f'network_out={network_out:.2f}\n'

            f.write(log_line)


def generate_api_logs(output_file, start_date, num_events):
    """Generate API access logs with JSON format"""
    print(f"Generating {num_events} API log events...")

    endpoints = [
        {"path": "/api/v1/users", "methods": ["GET", "POST"]},
        {"path": "/api/v1/products", "methods": ["GET", "POST", "PUT", "DELETE"]},
        {"path": "/api/v1/orders", "methods": ["GET", "POST"]},
        {"path": "/api/v1/analytics", "methods": ["GET"]},
        {"path": "/api/v1/reports", "methods": ["GET", "POST"]}
    ]

    with open(output_file, 'w') as f:
        for _ in range(num_events):
            timestamp = generate_timestamp(start_date)
            endpoint = random.choice(endpoints)
            method = random.choice(endpoint["methods"])

            status_rand = random.random()
            if status_rand < 0.8:
                status = 200
            elif status_rand < 0.9:
                status = random.choice([400, 401, 403, 404])
            else:
                status = random.choice([500, 502, 503])

            response_time = random.randint(10, 2000)
            user_id = random.choice(USERS) if random.random() > 0.2 else None

            log_entry = {
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "method": method,
                "endpoint": endpoint["path"],
                "status": status,
                "response_time_ms": response_time,
                "user_id": user_id,
                "ip_address": generate_ip(),
                "request_id": f"req_{random.randint(1000000, 9999999)}"
            }

            f.write(json.dumps(log_entry) + '\n')


def main():
    """Main data generation function"""
    print("=" * 60)
    print("Splunk Advanced Course - Sample Data Generator")
    print("=" * 60)

    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"\nCreated output directory: {OUTPUT_DIR}")

    # Generate data for the past 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_OF_DATA)

    print(f"\nGenerating data from {start_date.date()} to {end_date.date()}")
    print(f"Approximately {EVENTS_PER_DAY * DAYS_OF_DATA:,} events total\n")

    # Generate various log types
    generate_web_logs(
        os.path.join(OUTPUT_DIR, "web_access.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 3
    )

    generate_application_logs(
        os.path.join(OUTPUT_DIR, "application.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 4
    )

    generate_authentication_logs(
        os.path.join(OUTPUT_DIR, "auth.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 8
    )

    generate_sales_data(
        os.path.join(OUTPUT_DIR, "sales.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 6
    )

    generate_performance_metrics(
        os.path.join(OUTPUT_DIR, "performance.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 10
    )

    generate_api_logs(
        os.path.join(OUTPUT_DIR, "api.log"),
        start_date,
        EVENTS_PER_DAY * DAYS_OF_DATA // 5
    )

    # Generate lookup files
    generate_user_data(os.path.join(OUTPUT_DIR, "users.csv"))

    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)
    print(f"\nGenerated files in: {OUTPUT_DIR}/")
    print("\nFiles created:")
    for filename in os.listdir(OUTPUT_DIR):
        filepath = os.path.join(OUTPUT_DIR, filename)
        size = os.path.getsize(filepath)
        size_mb = size / (1024 * 1024)
        print(f"  - {filename:30s} ({size_mb:.2f} MB)")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    print("1. Upload files to Splunk:")
    print("   - Go to Settings > Add Data > Upload")
    print("   - Upload each log file")
    print("   - Set source type appropriately")
    print("\n2. Create indexes (if needed):")
    print("   - index=web (for web_access.log)")
    print("   - index=app (for application.log)")
    print("   - index=auth (for auth.log)")
    print("   - index=sales (for sales.log)")
    print("   - index=main (for other logs)")
    print("\n3. Upload lookup file:")
    print("   - Settings > Lookups > Lookup table files")
    print("   - Upload users.csv")
    print("\n4. Verify data ingestion:")
    print("   - Search: index=* | stats count by index")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nData generation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
