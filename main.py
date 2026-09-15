from zapv2 import ZAPv2
import os
import time
from datetime import datetime

TARGET = "https://example.com"
API_KEY = os.getenv("ZAP_API_KEY")
ZAP_HOST = os.getenv("ZAP_HOST")
zap_port = os.getenv("ZAP_PORT")

if API_KEY is None:
    print("API_KEY missing")
    exit()
elif ZAP_HOST is None:
    print("ZAP_HOST missing")
    exit()

if zap_port is None:
    print("ZAP_PORT missing; using 8080")
    zap_port = 8080

zap = ZAPv2(
    apikey=API_KEY,
    proxies={
        "http": f"http://{ZAP_HOST}:{zap_port}",
        "https": f"http://{ZAP_HOST}:{zap_port}",
    },
)


# Proxy a request to the target so that ZAP has something to deal with
print("Accessing target {}".format(TARGET))
zap.urlopen(TARGET)
# Give the sites tree a chance to get updated
time.sleep(2)

print("Spidering target {}".format(TARGET))
scanid = zap.spider.scan(TARGET)
# Give the Spider a chance to start
time.sleep(2)
while int(zap.spider.status(scanid)) < 100:
    # Loop until the spider has finished
    print(f"Spider progress: {zap.spider.status(scanid)}%")
    time.sleep(2)

print("Spider completed")

print(zap.spider.added_nodes(scanid))

while int(zap.pscan.records_to_scan) > 0:
    print("Records to passive scan : {}".format(zap.pscan.records_to_scan))
    time.sleep(2)

print("Passive Scan completed")

print("Active Scanning target {}".format(TARGET))
scanid = zap.ascan.scan(TARGET)
while int(zap.ascan.status(scanid)) < 100:
    # Loop until the scanner has finished
    print("Scan progress %: {}".format(zap.ascan.status(scanid)))
    time.sleep(5)

print("Active Scan completed")

# Report the results

print("Hosts: {}".format(", ".join(zap.core.hosts)))
print("Alerts: ")
print(zap.core.alerts())

timestamp = datetime.now().isoformat()

with open(f"/scanner_output/report.{timestamp}.json", "w") as file:
    file.write(zap.core.alerts())
