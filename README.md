<h1 align="center">Modulo Botnet</h1>
<h6 align="center"><i>Simple POC Botnet done by Group 1</i></h6>

<p align="center">
 <img src="https://img.shields.io/badge/last%20updated-June%202020-3d62d1">
 <img src="https://img.shields.io/github/downloads/notclement/botnet-enumeration-network/total">
 <img src="https://github.com/notclement/botnet-enumeration-network/workflows/Django%20CI/badge.svg">
</p>

## Table of contents

* [Usage](#usage)
* [Features](#features)
* [Supported Plugins](#supported-plugins)
* [Future expansions](#future-expansions)

## Usage
C2 Server
<i>The default username is admin. The default password is password</i>
```commandline
cd server_django
python manage.py migrate # to initialise and migrate database
python manage.py createsuperuser <username> # to create a new superuser (optional)
python manage.py runserver
```

Agent
```commandline
to be completed
```

## Features
<b>C2 Server (webui)</b>
- [ ] Login
- [ ] Dashboard
    - [ ] List of known compromised machines
    - [ ] Send Instruction
        - [ ] Select target agent(s)
        - [ ] Select from preconfigured list of commands (scan <>, download <>, run <>, ...)
        - [ ] Wait and receive output (if necessary)
- [ ] Generate report (.txt) for discovered hosts and respective ports
- [ ] Save and view past reports
- [ ] Build a network tree that showcases compromised machines

<b>C2 Server (api)</b>
- [x] Job Balancing
- [ ] Testing Connectivity with all known Agents
- [x] Sending Instructions
- [ ] Receiving Output of Instructions (tagging must be done to identify the 'session' or specific instruction sent, the computer it came from)
- [ ] Gathering a location heatmap of all the agents and target (https://ipinfo.io/<ip>)

<b>Agent</b>
- [ ] Testing Connectivity to Internet
- [ ] Callback to server (used only on infection, and during network change)
- [ ] In-built network discovery function
- [ ] In-built portscanning function for discovered networks (scan an IP for given port range)
    - [ ] Dropper (downloads file from C2)
    - [ ] Execution of files
    - [ ] Persistency
    - [ ] Self-Removal

## Supported Plugins
- [x] nmap
```commandline
load module nmap
nmap -sS 192.168.1.1 1-65535
```

## Future expansions
Work in progress
