<h1 align="center">Modulo Botnet</h1>
<h6 align="center"><i>Simple POC Botnet done by Group 1</i></h6>

<p align="center">
 <img src="https://img.shields.io/badge/last%20updated-July%202020-3d62d1">
 <img src="https://img.shields.io/pypi/pyversions/Django">
 <img src="https://img.shields.io/github/downloads/notclement/botnet-enumeration-network/total">
 <img src="https://github.com/notclement/botnet-enumeration-network/workflows/Django%20CI/badge.svg">
</p>

## Table of contents

* [Important directories](#important-directories)
* [Usage](#usage)
* [Features](#features)
* [Supported Plugins](#supported-plugins)
* [Future expansions](#future-expansions)

## Important Directories
* apps => server_django/apps (api, authentication, webui)
* modules => server_django/apps/api/modules

## Usage
<b>C2 Server</b>
<br><i>The default username is admin. The default password is password</i>
```commandline
cd server_django
python manage.py migrate # to initialise and migrate database
python manage.py createsuperuser <username> # to create a new superuser (optional)
python manage.py runserver
```

<b>Agent</b>
```commandline
to be completed
```

## Features
<b>C2 Server (webui)</b>
- [x] Login
- [x] Dashboard
    - [x] List of known compromised machines
- [x] Sessions
    - [x] Select target agent(s)
    - [x] Send Instruction
    - [x] Wait and receive output (if necessary)
    - [ ] Viewing other sessions
- [ ] Executing commands on individual agents
- [x] Style sheets
- [ ] Generate report (.txt) for discovered hosts and respective ports
- [ ] Save and view past reports
- [ ] Build a network tree that showcases compromised machines

<b>C2 Server (api)</b>
- [x] Job Balancing
- [x] Testing Connectivity with all known Agents
- [x] Sending Instructions
- [x] Receiving Output of Instructions (tagging must be done to identify the 'session' or specific instruction sent, the computer it came from)
- [x] Modules hosting for agents
- [ ] Gathering a location heatmap of all the agents and target (https://ipinfo.io/<ip>)

<b>Agent</b>
- [ ] Testing Connectivity to Internet
- [x] Callback to server (every 5 seconds)
- [ ] In-built network discovery function
- [ ] In-built portscanning function for discovered networks (scan an IP for given port range)
- [x] Dropper (downloads file from C2)
- [x] Execution of files
- [x] Persistency
- [ ] Self-Removal

## Supported Plugins
- [x] nmap
```commandline
load module nmap
nmap -sS 192.168.1.1 1-65535
```
- [x] dns_tunnelling
```commandline
# on the agent side
sudo dns2tcpc -f dns2tcpc.conf <server_ip>

# on the server side
sudo dns2tcpd -f dns2tcpd.conf
```

## Future expansions
- [ ] Docker swarm for different protocols like http and dns tunneling
