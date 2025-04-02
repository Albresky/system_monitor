Server resources monitor for *Debian GNU/Linux* with email notifications. *Python3* environment is required.


**Usage：**

*Before applying this tool, make sure you have been granted with the root privilege.*

**1. Install the required packages**

```bash
pip install -r requirements.txt
```

**2. Config sender email and users' email addresses**

Create a file named `email.conf` under the same directory as the script with the following content

```conf
EMAIL_SENDER = "admin@example.cn"
EMAIL_PASSWORD = 'TOKEN_OR_PASSWD_OF_THE_SENDER_EMAIL'
SMTP_SERVER = "SENDER_EMAIL_SERVER"
SMTP_PORT = 465 # SENDER_EMAIL_PORT
```

Document the email addresses of the users to be monitored in the `/usr/tools/contacts.conf` file, with one email address per line. For example:

```conf
admin:admin@example.cn
staffJack:jack@example.cn
```

**3. Register as a systemd service**

First, change the `<DIR_TO_CUR_PRJ>` in the `system-monitor.service` file to the *absolute path* of the current project directory.

Then, copy the service file to the systemd directory and enable it:

```bash
sudo cp service/system-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable system-monitor
sudo systemctl start system-monitor
```

**4. Check the status of the service**

```bash
tail -f /var/log/system-monitor.log
```