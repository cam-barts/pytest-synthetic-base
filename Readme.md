# Synthetic-In-A-Box

This is a base image to build onto when creating new synthetic monitoring using pytest and selenium. 


## Usage

Let's say you have a test that you'd like to run every 5 minutes. 


```python
# test_google.py
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_google(driver: webdriver.Chrome):
    # Can I reach google?
    driver.get("https://www.google.com/")
    driver.find_element_by_name("q").click()
    driver.find_element_by_name("q").clear()
    driver.find_element_by_name("q").send_keys("do a barrel roll")
    driver.find_element_by_name("q").send_keys(Keys.ENTER)
    driver.find_element_by_name("q").send_keys(Keys.ENTER)
    search_value = driver.find_element_by_name("q").get_attribute("value")
    assert search_value == "do a barrel roll"
```

You'd first create a script and a crontab.

```bash synthetic.sh
#!/bin/bash

# Ping healthchecks.io for start, exit status, and message
curl --retry 3 https://hc-ping.com/1234-abcd/start
m=$(for i in $(seq 1 3); do [ $i -gt 1 ] && sleep 10; /usr/local/bin/pytest /app -vv && s=0 && break || s=$?; done; (exit $s))
curl -fsS -m 10 --retry 5 --data-raw "$m" https://hc-ping.com/1234-abcd/$?
```

```crontab crontab
*/5 * * * * BASH_ENV=/etc/profile /bin/bash /app/synthetic.sh

```

Then create a new docker image

```Dockerfile
FROM synthetic-base-image

RUN apt-get install -y cron

COPY crontab /app/crontab
COPY synthetic.sh /app/synthetic.sh

RUN chmod 700 /app/synthetic.sh
RUN chmod 644 /app/crontab
RUN crontab /app/crontab

CMD ["/bin/sh", "-c", "printenv > /etc/profile && cron -f"]
```

Spin that docker container and it will start running your synthetic monitor. 