# botnet-enumeration-network
Simple POC Botnet done by Group 1

## Botnet C2 Functionalities
* Job Balancing
* Testing Connectivity with all known Agents
* Sending Instructions
* Receiving Output of Instructions (tagging must be done to identify the 'session' or specific instruction sent, the computer it came from)
* Gathering a location heatmap of all the agents and target (https://ipinfo.io/<ip>)

## Botnet Agent Functionalities
* Testing Connectivity to Internet
* Callback to server (used only on infection, and during network change)
* In-built network discovery function
* In-built portscanning function for discovered networks (scan an IP for given port range)
  * Dropper (downloads file from C2)
  * Execution of files
  * Persistency
  * Self-Removal

## Botnet C2 Web-GUI Components
* Login
* Dashboard
  * List of known compromised machines
  * Send Instruction
    * Select target agent(s)
    * Select from preconfigured list of commands (scan <>, download <>, run <>, ...)
    * Wait and receive output (if necessary)
* Generate report (.txt) for discovered hosts and respective ports
* Save and view past reports
* Build a network tree that showcases compromised machines

## Usage
```console
$ to be completed
```
