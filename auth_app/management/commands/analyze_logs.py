from django.core.management.base import BaseCommand
import re
from collections import Counter


class Command(BaseCommand):
    help = "Analyze logs for abnormal requests"

    def handle(self, *args, **kwargs):
        with open("user_requests.log", "r") as file:
            logs = file.readlines()

        ip_addresses = [
            re.search(r"\d+\.\d+\.\d+\.\d+", log).group(0)
            for log in logs
            if re.search(r"\d+\.\d+\.\d+\.\d+", log)
        ]
        ip_count = Counter(ip_addresses)

        for ip, count in ip_count.items():
            if count > 5:  # Example threshold
                self.stdout.write(
                    self.style.WARNING(
                        f"Suspicious activity from {ip}: {count} requests"
                    )
                )
