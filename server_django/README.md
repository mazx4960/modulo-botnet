# Botnet CnC (Django)

The default username is admin.
The default password is password

## Functionalities
* Job Balancing
* Testing Connectivity with all known Agents
* Sending Instructions
* Receiving Output of Instructions (tagging must be done to identify the 'session' or specific instruction sent, the computer it came from)
* Gathering a location heatmap of all the agents and target (https://ipinfo.io/)

## To do
- [ ] ??

## Usage
```console
$ pip install -r requirements.txt
$ python manage.py runserver
```

To specify the port and the interface to listen on,
```console
$ python manage.py runserver 0:8000  # port 8000 on the external interface
```