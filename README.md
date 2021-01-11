# Wol Control

This is a web based power controller for computer on a local network. It uses the Wake On Lan (WOL) standard to turn on devices remotely, and bash scripts to turn them off. It'd only work with devices that support WOL and the execution of commands over SSH (typically UNIX based systems). 

Wol Control makes heavy use of [WOL](https://github.com/timofurrer/WOL/), a C program written by [timofurrer](https://github.com/timofurrer), to send wol magic over the network.

## DISCLAIMER
**DO NOT use this on a production enviroment or anywhere security is a big concern. I wrote this application with the sole porpuse of running it on an isolated network with some media servers on it. This software comes with no warranty, so use it at your own discretion.**

# Setup

Although it is possible to install Wol Control on non Linux systems, it's recommened you install it on one, specially on one that supports systemd. And while its not necessary, I'd personally recommend you set it up on a single board computer such as a raspberry pi, just so it could always stay on, and not consume too much power.

***Also, I recommend you create a separate user for Wol Control and clone this repository in its home directory, as it makes this process a bit easier/faster.***

Before setting up Wol Control you'll need the following dependencies to use it:
* python3
* pip (python3)
* [WOL](https://github.com/timofurrer/WOL/)
* git
* nginx

## Clonning the repository

First, you'd need to clone this repository on the server where you'd like to install it. You can do so by using the following command:

```
git clone https://github.com/TheLastBilly/ydlg
```

### Using the setup.sh script 

If you'd like to skip out the rest of the setup process, you can use the **setup.sh** script to install Wol Control on you current machine. Since it's pretty much a quick hack I made so I wouldn't have to type many commands everytime I wanted to test it on a new system, keep in mind it might not work properly.

## Setting up a python virtual enviroment

Now that the repository is cloned, the next thing you'd like to do is to install `virtualenv` using `pip`. We're using a virtual enviroment for Wol Control to avoid conflicts with currently installed modules on your machine. You can skip this part if you want, but I don't recommend it.

```
python3 -m pip install --user virtualenv
```
**This will install `virtualenv` for your current user (no need for sudo).**

Next you'll have to create a python virtual enviroment and install all the necessary python dependencies on it. In order to do so, use the following commands:

***Make sure to move to the repository's directory first.***

```
python3 -m virtualenv ~/.ydlg_env
```
**This command will create a virtual enviroment on your home directory (`~/`) named `ydlg_env`. The `.` is used to make this a hidden folder so you wouldn't normaly see it unless you actively look for it. Regardless, you can name it however you want.**

```
source ~/.ydlg_env/bin/activate
python3 -m pip install -r requirements.txt
```
**The first command will active your virtual enviroment and the second one will install all of the dependencies listed on the requirements.txt file.**

## Wol Control setup

Now that all the necessary depencencies have been installed, you can now setup Wol Control's database, create new users and add devices.

First things first, intialize a new database using the **init_db.py** script:
```
python3 init_db.py
```

Create a new user and add some devices using the **manage_users.py** and **manage_devices.py** scripts respectively:
```
python3 manage_users.py
python3 manage_devices.py
```
And finally, go to the **ydlg/main.py** file and set the `remote_user` variable to the username that you'll use to shutdown remote computers with over SSH (more on that later).

## Nginx setup

Wol Control uses `nginx` to handle remote resquests from its clients. Assuming you already setup `nginx`, you'll then have to create a settings file so Wol Control can be accessed by it.

There's a file inluded in this repository, **ydlg.nginx**, which you can use as a template for that:

```
server {
	listen localhost:9090;
	location / {
		proxy_set_header   Host $host:9090;
                proxy_set_header   X-Real-IP $remote_addr;
                proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Host $server_name;
		proxy_pass http://unix:/home/sammy/ydlg/ydlg.sock:/;
	}
}
```

Just replace the path in between `proxy_pass http://unix:` and `/ydlg.sock:/` with the local path of this repository in your computer. Also, make sure to change the address that `nginx` will be listening to in the `listen` line at the beggining of the file from `localhost` to your machine's hostname/ip.

Now you can copy the **ydlg.nginx** file into your nginx `/etc/nginx/sites-available/` folder and enable it.

```
sudo cp ./ydlg.nginx /etc/nginx/sites-available/ydlg.nginx
sudo ln -s /etc/nginx/sites-available/ydlg.nginx /etc/nginx/sites-enabled/ydlg.nginx
```

Finally, we can check our `nginx` configuration file with the following command:

```
sudo nginx -t
```

And if everything is alright, restart `nginx`:
```
sudo systemctl restart nginx
```

## Systemd setup

You'll have to setup a service file for Wol Control. There's already one provided with this repository **ydlg.service**, so you can use it as a template.

```
[Unit]
Description=Gunicorn service of ydlg
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/ydlg
Environment="PATH=/home/sammy/.ydlg_env/bin:/usr/bin"
ExecStart=/home/sammy/.ydlg_env/bin/gunicorn --workers 3 --access-logfile ydlg.log --bind unix:ydlg.sock -m 007 wsgi

[Install]
WantedBy=multi-user.target
```

This file assumes that you installed a virtual enviroment on `~/.ydlg_env`, so make sure you change that path with whatever directory you used on that step, or remove the use of a virtual enviroment  from the file altogether. If you do remove any mentions of a virtual enviroment, your service file should end up looking like this:

```
[Unit]
Description=Gunicorn service of ydlg
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/ydlg
Environment="/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 -m gunicorn --workers 3 --access-logfile ydlg.log --bind unix:ydlg.sock -m 007 wsgi

[Install]
WantedBy=multi-user.target
```

Just like with the `nginx` setup step, replace the path specified after the `WorkingDirectory` variable with the path where you clonned this repository into. Also make sure to replace the `sammy` user in the `User` variable with username of the user that has access to this repository.

Then, copy the **ydlg.service** file to the `/etc/systemd/system` folder and reload the `systemd` daemon.

```
sudo cp ./ydlg.service /etc/systemd/system/ydlg.service
sudo systemctl daemon-reload
```

And finally, start the `ydlg` service and enable.

```
sudo systemctl start ydlg
sudo systemctl enable ydlg
```

## And that's it!

You should now be able to access Wol Control from your local network. 

You can do so by accessing the following address from your browser:
```
http://[Your Server's Address]:9090
```

***`[Your Server's Address]` is the address that you used in the `nginx`'s `listen` line.***

# Usage

***If you used a virtual enviroment to install Wol Control, you'll probably need to activate it before using any of the included python scripts in this repository.***

## Managing users

You can create and delte users by using the **manage_users.py** script:

```
python3 manage_users.py
```

## Managing devices

You can create and delte users by using the **manage_devices.py** script:

```
python3 manage_devices.py
```

## Seting up devices

In orther to properly setup a device, you'll need to enable `Wake On Lan` on it first. This may vary from device to device, but for most computers in can be enabled from a menu option on their BIOS menu.

### Setting up remote shut down 

***This is only supported on Unix based systems***

Assuming the machine where Wol Control is running is Machine A and the one that you'd like to shut down remotely is Machine B, follow these steps:

First, create an user on Machine B with the same username that you used on the `remote_user` variable from the **ydlg/main.py** file back at the **Wol Control setup** step.

Then, add the SSH key from the user running Wol Control on Machine A into the newly created user on Machine B:

***If you don't have a SSH key setup on Machine A, you can do so by using the `ssh-keygen` command on it.***

**On Machine A (Wol Control User)**
```
ssh-copy-id [Machine B's user]@[Machine B's IP]
```
**Make sure to log into Machine B from Machine A at least once, otherwise the `Turn Off` feature might not work. You can do that by using the following command: ```ssh [Machine B's user]@[Machine B's IP]``` on Machine A.**

Lastly, create a folder named `.ydlg/` on Machine B's user's home directory and then create a file named **~/.ydlg/remote_shutdown.sh**. Here you'll add the command that will shutdown Machine B whenever you click the `Turn Off` button on Wol Control's interface. I personally just use `poweroff` but this may not work depending on your system:

**On Machine B**
```
mkdir ~/.ydlg
echo "poweroff" > ~/.ydlg/remote_shutdown.sh
```