## Deployment instructions

Here's how you can deploy the app on an AWS EC2 instance (Ubuntu 24.04)

Install required packages

```sh
$ sudo apt update && sudo apt install python3.12-venv python3-pip apache2
```

Create a directory for the project and set up permissions.

```sh
$ sudo mkdir /srv/calorieapp
$ sudo chown ubuntu:ubuntu /srv/calorieapp/
```

Install Python virtual environment and requirements

```sh
$ cd /srv/calorieapp/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Add Gunicorn user and set up permissions

```sh
$ sudo adduser --system --no-create-home --group gunicorn
$ sudo chown -R gunicorn:gunicorn /srv/calorieapp/
```

Install background service

```sh
$ sudo cp config/calorieapp.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable calorieapp
$ sudo service calorieapp start
$ sudo service calorieapp status
```

Install Apache configuration

```sh
$ sudo cp config/calorieapp_apache.conf /etc/apache2/sites-available/
$ sudo a2enmod proxy proxy_http
$ sudo a2ensite calorieapp_apache.conf
$ sudo service apache2 reload
```

Install Let's Encrypt SSL certificate

```sh
$ sudo snap install --classic certbot
$ sudo ln -s /snap/bin/certbot /usr/bin/certbot
$ sudo certbot --apache
```

Set up cron job for automatic SSL certificate renewal

```sh
$ sudo crontab -e
```

Add this to crontab:

```
0 4 * * 1 /usr/bin/certbot --renew && /usr/sbin/service apache2 reload
```

Crate swapfile (bonus)

```sh
$ sudo fallocate -l 1G /swapfile
$ sudo chmod 0600 /swapfile
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
```

Add swapfile to `/etc/fstab` to persist over boot

```sh
$ echo "/swapfile   none   swap   sw   0 0" > /etc/fstab
```
