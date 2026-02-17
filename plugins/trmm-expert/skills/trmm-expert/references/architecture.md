# Architecture and Installation

> Sources: howitallworks.md, install_considerations.md, install_agent.md, mesh_integration.md

## Table of Contents

- [How It All Works](#how-it-all-works)
  - [Understanding TRMM](#understanding-trmm)
  - [Server](#server)
    - [Outbound Firewall Rules](#outbound-firewall-rules)
    - [System Services](#system-services)
    - [Other Dependencies](#other-dependencies)
  - [Windows Agent](#windows-agent)
    - [RunAsUser Functionality](#runasuser-functionality)
    - [Agent Outbound Firewall Rules](#agent-outbound-firewall-rules)
    - [Agent Installation Process](#agent-installation-process)
    - [Agent Update Process](#agent-update-process)
    - [Tactical Agent Debugging](#tactical-agent-debugging)
    - [Windows Update Management](#windows-update-management)
    - [Log Files](#log-files)
    - [Failed / Successful Admin Logins](#failed--successful-admin-logins)
- [Installation Considerations](#installation-considerations)
  - [Debian vs Ubuntu](#debian-vs-ubuntu)
  - [Traditional Install](#traditional-install---officially-supported)
  - [Docker Install](#docker-install)
  - [Azure VMs](#azure-vms)
  - [Larger Installs](#larger-installs)
- [Agent Installation](#agent-installation)
  - [UI](#ui)
  - [Manual](#manual)
  - [Dynamically Generated Executable](#dynamically-generated-executable)
  - [PowerShell](#powershell)
  - [Using a Deployment Link](#using-a-deployment-link)
  - [Optional Installer Args](#optional-installer-args)
  - [Scripting Agent Installation](#scripting-agent-installation)
  - [Script for Full Agent Uninstall](#script-for-full-agent-uninstall)
  - [Reinstalling Mesh and Reconnecting to TRMM](#reinstalling-mesh-and-reconnecting-to-trmm)
  - [Install Linux Agent (beta)](#install-linux-agent-beta)
  - [Linux Deployment Link](#linux-deployment-link)
  - [Mac Agent Permissions](#mac-agent-permissions)
- [MeshCentral Integration](#meshcentral-integration)
  - [Overview](#overview)
  - [How Does It Work?](#how-does-it-work)
  - [Customize Take Control Username](#customize-take-control-username)
  - [Turn Off the Sync Feature](#turn-off-the-sync-feature)
  - [Toggle a Full Permissions Re-sync](#toggle-a-full-permissions-re-sync)
  - [Get a URL to Login to Mesh as the Mesh Superuser](#get-a-url-to-login-to-mesh-as-the-mesh-superuser)
  - [Modifying the Internal Mesh Port Configuration](#modifying-the-internal-mesh-port-configuration)
  - [Running Your Own Existing or Separate MeshCentral Server](#running-your-own-existing-or-separate-meshcentral-server)
  - [Take Control Connect vs RDP Connect](#take-control-connect-vs-rdp-connect)
  - [Remote Terminal How It Works](#remote-terminal-how-it-works)
  - [MeshCentral Options](#meshcentral-options)
  - [Using Tactical RMM Without MeshCentral](#using-tactical-rmm-without-meshcentral)
  - [Fixing Missing Agents in TRMM or Mesh](#fixing-missing-agents-in-trmm-or-mesh)
  - [MeshCentral Maintenance Status](#meshcentral-maintenance-status)

---

## How It All Works

### Understanding TRMM

Anything you configure: scripts, tasks, patching, etc is queued and scheduled on the server to do something.
Everything that is queued, happens immediately when agents are online.
The agent gets a NATS command, the server tells it to do xyz and it does it.

When agents are not connected to the server nothing happens. The Windows Task Scheduler says do x at some time, what it's asked to do is get x command from the server. If the server is offline, nothing happens.
If an agent comes online, every x interval (Windows Update, pending tasks etc) check and see if there is something for me to do that I missed while I was offline. When that time occurs (e.g. agent sees if it needs to update itself at 35 minutes past every hour) it'll get requested on the online agent.

That's the simplified general rule for everything TRMM.

Still need graphics for:

    1. Agent installer steps

    2. Agent checks / tasks and how they work on the workstation/interact with server

### Server

Has a Postgres database. See the Django Admin section in references/settings-and-admin.md for the web interface for the Postgres database.

All Tactical RMM dependencies are listed at https://github.com/amidaware/tacticalrmm/blob/develop/api/tacticalrmm/requirements.txt.

A complete list of all packages used by Tactical RMM are listed at https://github.com/amidaware/tacticalrmm-web/blob/develop/package-lock.json.

#### Outbound Firewall Rules

If you have strict outbound firewall rules these are the outbound rules needed for all functionality:

##### Regular Use

1. Access to Github for downloading and installing TRMM, and checking if new TRMM version is available to show in the admin web panel.
2. Access to nginx.org to install
3. Access to mongodb.org to install
4. Access to python.org to install
5. Access to postgresql.org to install
6. Whatever servers [Let's Encrypt](https://letsencrypt.org/docs/faq/#what-ip-addresses-does-let-s-encrypt-use-to-validate-my-web-server) uses for DNS-01 challenges
7. Cloudflare is for the licensing servers.

##### Server Without Code Signing Key

No additional rules needed.

##### Server With Code Signing Key

No additional rules needed.

#### System Services

This lists the system services used by the server.

Quick server health inspection

```bash
cd /rmm/api/tacticalrmm/
source ../env/bin/activate
for i in active reserved scheduled stats; do celery -A tacticalrmm inspect $i; done
```

##### Nginx Web Server

Nginx is the web server for the `rmm`, `api`, and `mesh` domains. All sites redirect port 80 (HTTP) to port 443 (HTTPS).

**nginx configuration (a.k.a. sites available)**

- nginx configuration docs: https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/

**`rmm.example.com`** - This serves the frontend website that you interact with.

- Config: `/etc/nginx/sites-enabled/frontend.conf`
- root: `/var/www/rmm/dist`
- Access log: `/var/log/nginx/frontend-access.log`
- Error log: `/var/log/nginx/frontend-error.log`
- TLS certificate: `/etc/letsencrypt/live/example.com/fullchain.pem`

**`api.example.com`** - This serves the TRMM API for the frontend and agents.

- Config: `/etc/nginx/sites-enabled/rmm.conf`
- roots:
    - `/rmm/api/tacticalrmm/static/`
    - `/rmm/api/tacticalrmm/tacticalrmm/private/`
- Upstreams:
    - `unix://rmm/api/tacticalrmm/tacticalrmm.sock`
    - `unix://rmm/daphne.sock`
- Access log: `/rmm/api/tacticalrmm/tacticalrmm/private/log/access.log`
- Error log: `/rmm/api/tacticalrmm/tacticalrmm/private/log/error.log`
- TLS certificate: `/etc/letsencrypt/live/example.com/fullchain.pem`

**`mesh.example.com`** - This serves MeshCentral for remote access.

- Config: `/etc/nginx/sites-enabled/meshcentral.conf`
- Upstream: `http://127.0.0.1:4430/`
- Access log: `/var/log/nginx/access.log` (uses default)
- Error log: `/var/log/nginx/error.log` (uses default)
- TLS certificate: `/etc/letsencrypt/live/example.com/fullchain.pem`

**default** - This is the default site installed with nginx. This listens on port 80 only.

- Config: `/etc/nginx/sites-enabled/default`
- root: `/var/www/rmm/dist`
- Access log: `/var/log/nginx/access.log` (uses default)
- Error log: `/var/log/nginx/error.log` (uses default)

**systemd config**

Status commands:

- Status: `systemctl status --full nginx.service`
- Stop: `systemctl stop nginx.service`
- Start: `systemctl start nginx.service`
- Restart: `systemctl restart nginx.service`
- Restart: `systemctl reload nginx.service` reloads the config without restarting
- Test config: `nginx -t`
- Listening process: `ss -tulnp | grep nginx`

Standard:

- Service: `nginx.service`
- Address: `0.0.0.0`
- Port: 443
- Exec: `/usr/sbin/nginx -g 'daemon on; master_process on;'`
- Version: 1.18.0

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-nginx"`
- View logs: `docker compose logs tactical-nginx`
- "tail" logs: `docker compose logs tactical-nginx | tail`
- Shell access: `docker exec -it trmm-nginx /bin/bash`


##### Tactical RMM (Django uWSGI) Service

Built on the Django framework, the Tactical RMM service is the heart of the system by serving the API for the frontend and agents.

**uWSGI config**

- uWSGI docs: https://uwsgi-docs.readthedocs.io/en/latest/index.html

Status commands:

- Status: `systemctl status --full rmm.service`
- Stop: `systemctl stop rmm.service`
- Start: `systemctl start rmm.service`
- Restart: `systemctl restart rmm.service`
- journalctl:
    - "tail" the logs: `journalctl --identifier uwsgi --follow`
    - View the logs: `journalctl --identifier uwsgi --since "30 minutes ago" | less`
    - Debug logs for 5xx errors will be located in `/rmm/api/tacticalrmm/tacticalrmm/private/log`

Standard:

- Service: `rmm.service`
- Socket: `/rmm/api/tacticalrmm/tacticalrmm.sock`
- uWSGI config: `/rmm/api/tacticalrmm/app.ini`
- Log: None
- Journal identifier: `uwsgi`
- Version: 2.0.18

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-backend"`
- View logs: `docker compose logs tactical-backend`
- "tail" logs: `docker compose logs tactical-backend | tail`
- Shell access: `docker exec -it trmm-backend /bin/bash`

##### Daphne: Django Channels Daemon

[Daphne](https://github.com/django/daphne) is the official ASGI HTTP / WebSocket server maintained by the [Channels project](https://channels.readthedocs.io/en/stable/index.html).

**Daphne config**

- Django Channels configuration docs: https://channels.readthedocs.io/en/stable/topics/channel_layers.html

Status commands:

- Status: `systemctl status --full daphne.service`
- Stop: `systemctl stop daphne.service`
- Start: `systemctl start daphne.service`
- Restart: `systemctl restart daphne.service`
- journalctl (this provides only system start/stop logs, not the actual logs):
    - "tail" the logs: `journalctl --identifier daphne --follow`
    - View the logs: `journalctl --identifier daphne --since "30 minutes ago" | less`

Standard:

- Service: `daphne.service`
- Socket: `/rmm/daphne.sock`
- Exec: `/rmm/api/env/bin/daphne -u /rmm/daphne.sock tacticalrmm.asgi:application`
- Config: `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`
- Log: `/rmm/api/tacticalrmm/tacticalrmm/private/log/trmm_debug.log`

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-websockets"`
- View logs: `docker compose logs tactical-websockets`
- "tail" logs: `docker compose logs tactical-websockets | tail`
- Shell access: `docker exec -it trmm-websockets /bin/bash`

##### NATS Server Service

[NATS](https://nats.io/) is a messaging bus for "live" communication between the agent and server. NATS provides the framework for the server to push commands to the agent and receive information back.

**NATS config**

- NATS server configuration docs: https://docs.nats.io/running-a-nats-service/configuration

Status commands:

- Status: `systemctl status --full nats.service`
- Stop: `systemctl stop nats.service`
- Start: `systemctl start nats.service`
- Restart: `systemctl restart nats.service`
- Reload: `systemctl reload nats.service` reloads the config without restarting
- journalctl:
    - "tail" the logs: `journalctl --identifier nats-server --follow`
    - View the logs: `journalctl --identifier nats-server --since "30 minutes ago" | less`
- Listening process: `ss -tulnp | grep nats-server`
- Checking for NATS or websocket problems `sudo journalctl --no-pager -u nats` and `sudo journalctl --no-pager -u nats-api`

Standard:

- Service: `nats.service`
- Address: `0.0.0.0`
- Port: `4222 (standard), 9235 (websocket)`
- Exec: `/usr/local/bin/nats-server --config /rmm/api/tacticalrmm/nats-rmm.conf`
- Config: `/rmm/api/tacticalrmm/nats-rmm.conf`
    - TLS: `/etc/letsencrypt/live/example.com/fullchain.pem`
- Log: None
- Version: v2.3.3

Docker:

- Get into bash in your docker with: `docker exec -it trmm-nats /bin/bash`
- Log: `nats-api -log debug`
- Shell access: `docker exec -it trmm-nats /bin/bash`

##### NATS API Service

**NATS API config**

Status commands:

- Status: `systemctl status --full nats-api.service`
- Stop: `systemctl stop nats-api.service`
- Start: `systemctl start nats-api.service`
- Restart: `systemctl restart nats-api.service`
- journalctl: This application does not appear to log anything.

Standard:

- Service: `nats-api.service`
- Exec: `/usr/local/bin/nats-api --config /rmm/api/tacticalrmm/nats-api.conf`
- Config: `/rmm/api/tacticalrmm/nats-api.conf`
    - TLS: `/etc/letsencrypt/live/example.com/fullchain.pem`
- Log: None

Docker:

- Get into bash in your docker with: `docker exec -it trmm-nats /bin/bash`
- Log: `nats-api -log debug`

##### Celery Service

[Celery](https://github.com/celery/celery) is a task queue focused on real-time processing and is responsible for scheduling tasks to be sent to agents.

Log located at `/var/log/celery`

**Celery config**

- Celery docs: https://docs.celeryproject.org/en/stable/index.html
- Celery configuration docs: https://docs.celeryproject.org/en/stable/userguide/configuration.html

Status commands:

- Status: `systemctl status --full celery.service`
- Stop: `systemctl stop celery.service`
- Start: `systemctl start celery.service`
- Restart: `systemctl restart celery.service`
- journalctl: Celery executes `sh` causing the systemd identifier to be `sh`, thus mixing the `celery` and `celerybeat` logs together.
    - "tail" the logs: `journalctl --identifier sh --follow`
    - View the logs: `journalctl --identifier sh --since "30 minutes ago" | less`
- Tail logs: `tail -F /var/log/celery/w*-*.log`

Standard:

- Service: `celery.service`
- Exec: `/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'`
- Config: `/etc/conf.d/celery.conf`
- Log: `/var/log/celery/w*-*.log`

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-celery"`
- View logs: `docker compose logs tactical-celery`
- "tail" logs: `docker compose logs tactical-celery | tail`
- Shell access: `docker exec -it trmm-celery /bin/bash`

##### Celery Beat Service

[Celery Beat](https://github.com/celery/django-celery-beat) is a scheduler. It kicks off tasks at regular intervals, that are then executed by available worker nodes in the cluster.

**Celery Beat config**

- Celery beat docs: https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html

Status commands:

- Status: `systemctl status --full celerybeat.service`
- Stop: `systemctl stop celerybeat.service`
- Start: `systemctl start celerybeat.service`
- Restart: `systemctl restart celerybeat.service`
- journalctl: Celery executes `sh` causing the systemd identifier to be `sh`, thus mixing the `celery` and `celerybeat` logs together.
    - "tail" the logs: `journalctl --identifier sh --follow`
    - View the logs: `journalctl --identifier sh --since "30 minutes ago" | less`
- Tail logs: `tail -F /var/log/celery/beat.log`

Standard:

- Service: `celerybeat.service`
- Exec: `/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat --pidfile=${CELERYBEAT_PID_FILE} --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'`
- Config: `/etc/redis/redis.conf`
- Log: `/var/log/celery/beat.log`

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-celerybeat"`
- View logs: `docker compose logs tactical-celerybeat`
- "tail" logs: `docker compose logs tactical-celerybeat | tail`
- Shell access: `docker exec -it trmm-celerybeat /bin/bash`

##### Redis Service

[Redis](https://github.com/redis/redis) is an in-memory data structure store used as a database, cache, and message broker for Django / Celery.

Log located at `/var/log/redis`

**Redis config**

- Redis docs: https://redis.io/

Status commands:

- Status: `systemctl status --full redis-server.service`
- Stop: `systemctl stop redis-server.service`
- Start: `systemctl start redis-server.service`
- Restart: `systemctl restart redis-server.service`
- Tail logs: `tail -F /var/log/redis/redis-server.log`

Standard:

- Service: `redis-server.service`
- Log: `/var/log/redis/redis-server.log`

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-redis"`
- View logs: `docker compose logs tactical-redis`
- "tail" logs: `docker compose logs tactical-redis | tail`
- Shell access: `docker exec -it trmm-redis /bin/bash`

##### MeshCentral

[MeshCentral](https://github.com/Ylianst/MeshCentral) is used for "Take Control" (connecting to machine for remote access), and 2 screens of the "Remote Background" (Terminal, and File Browser).

Config file location:

```bash
/meshcentral/meshcentral-data/config.json
```

Customize (https://ylianst.github.io/MeshCentral/meshcentral/config/) with care.

> **Note:** Mesh usernames are **CaSe sEnSiTive**. Tactical will make sure it's all lower case to avoid sync problems.

**MeshCentral management**

- MeshCentral docs: https://ylianst.github.io/MeshCentral/

Status commands:

- Status: `systemctl status --full meshcentral`
- Stop: `systemctl stop meshcentral`
- Start: `systemctl start meshcentral`
- Restart: `systemctl restart meshcentral`

Docker:

- From the docker host view container status - `docker ps --filter "name=trmm-meshcentral"`
- View logs: `docker compose logs tactical-meshcentral`
- "tail" logs: `docker compose logs tactical-meshcentral | tail`
- Shell access: `docker exec -it trmm-meshcentral /bin/bash`

Debugging:

- Open either "Take Control" or "Remote Background" to get mesh login token.
- Open https://mesh.example.com to open native mesh admin interface.
- Left-side "My Server" > Choose "Console" > type `agentstats`
- To view detailed logging goto "Trace" > click Tracing button and choose categories.

If you run `sudo systemctl status --full --no-pager meshcentral` and you don't see `Active: active (running) since ...`

You can manually run meshcentral using this command to see the full output with errors.

```bash
sudo systemctl stop meshcentral
cd /meshcentral/
/usr/bin/node node_modules/meshcentral
```

##### MeshCentral Agent

Get Mesh Agent Version info with this command. Should match server version.

```cmd
"C:\Program Files\Mesh Agent\MeshAgent.exe" -info"
```
Compare the hash with the tags in the repo at https://github.com/Ylianst/MeshAgent/tags.

Checks / tasks / agent data uses regular http to Nginx.

Agent status uses NATS websockets.

#### Other Dependencies

[Django](https://www.djangoproject.com/) - Framework to enable the server to interact with browser.

<details>
  <summary>Django dependencies</summary>

```text
future==0.18.2
loguru==0.5.3
msgpack==1.0.2
packaging==20.9
psycopg2-binary==2.9.1
pycparser==2.20
pycryptodome==3.10.1
pyotp==2.6.0
pyparsing==2.4.7
pytz==2021.1
```
</details>

[qrcode](https://pypi.org/project/qrcode/) - Creating QR codes for 2FA.

<details>
  <summary>qrcode dependencies</summary>

```text
requests==2.25.1
six==1.16.0
sqlparse==0.4.1
```
</details>

[Twilio](https://www.twilio.com/) - Python SMS notification integration.

<details>
  <summary>twilio dependencies</summary>

```text
urllib3==1.26.5
uWSGI==2.0.19.1
validators==0.18.2
vine==5.0.0
websockets==9.1
zipp==3.4.1
```
</details>


### Windows Agent

Found in `%programfiles%\TacticalAgent`

The Tactical RMM agent runs under the `SYSTEM` security context.

When scripts / checks execute, they are:

1. Transferred from the server via NATS.
2. Saved to a randomly created file in `C:\ProgramData\TacticalRMM`.
3. Executed.
4. Return info is captured and returned to the server via NATS.
5. File in `C:\ProgramData\TacticalRMM` is removed automatically after execution / timeout.
6. Command Parameters for scripts stay in memory

Also "Send Command" stay in memory as well.

Having said that...Windows logs all things PowerShell: `Event Viewer` > `Microsoft` > `Windows` > `PowerShell` > `Operational` Log so be careful with fancy API calls and auth token using agents for execution.

> **Warning:** Auth tokens are Username/Password/2FA verification all rolled into a single chunk of text!

#### RunAsUser Functionality

Now that we know the agent runs under the `SYSTEM` security context and what that means, there is an option to "RunAsUser" (Windows only).

There are multiple things to understand and consider.

1. TRMMs native "RunAsUser" is only supported on workstations and non-RDP/terminal services servers.
2. The user has to be logged in, if the computer is still sitting at the Login screen there will be no active user to discover, and fail. If you're using fast user switching, it is the active user that will be discovered and used.

There are two ways to do RunAsUser with tactical in relation to scripting.

1. The Tactical RMM "RunAsUser" checkbox associated with the script, and all code will be run under the actively logged in user only with their security permissions. The user access token that will be used is the [limited user access token](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/how-it-works). You will not be able to do any admin level stuff because TRMM's RunAsUser doesn't have a UAC elevation capability to call and request a 2nd access token with admin privileges.
2. Using the PowerShell "RunAsUser" [3rd party module](https://github.com/amidaware/community-scripts/blob/da4d615a781d218ed3bec66d56a1530bc7513e16/scripts/Win_RunAsUser_Example.ps1)

#### Agent Outbound Firewall Rules

If you have strict firewall rules these are the only outbound rules from the agent needed for all functionality:

1. All agents have to be able to connect outbound to TRMM server on the 3 domain names on port 443.

2. The agent uses `https://icanhazip.tacticalrmm.io/` to get public IP info. If this site is down for whatever reason, the agent will fallback to `https://icanhazip.com` and then `https://ifconfig.co/ip`

##### Unsigned Agents

Unsigned agents require access to: `https://github.com/amidaware/rmmagent/releases/*` for downloading / updating agents.

##### Signed Agents

Signed agents require access to: `https://agents.tacticalrmm.com` for downloading / updating agents.

#### Agent Installation Process

* Copies temp files to `C:\ProgramData\TacticalRMM` folder.
* INNO setup installs app into `%ProgramFiles%\TacticalAgent\` folder.

---

#### Agent Update Process

Downloads latest `tacticalagent-vx.x.x.exe` to `%PROGRAMDATA\TacticalRMM%`.

Executes the file (INNO setup exe).

Log file `C:\ProgramData\TacticalRMM\tacticalagent_update_vX.X.X.txt` is created.

---

#### Tactical Agent Debugging

Choose your method:

**Windows Automatically**

If the Tactical agent is connecting to your server, you can use the Community scripts:

- `TacticalRMM - TRMM Agent enable Debug Mode`
- `TacticalRMM - TRMM Agent disable Debug Mode`
- and `TacticalRMM - Get Agent Logs`

**Windows Manually**

Open CMD as admin on the problem computer and stop the agent services:

```cmd
net stop tacticalrmm
```

Run the tacticalrmm service manually with debug logging:

```cmd
"C:\Program Files\TacticalAgent\tacticalrmm.exe" -m rpc -log debug -logto stdout
```

> **Note:** There's a Community script that will collect your agent log called `TacticalRMM - Get Agent Logs`.

**Linux**

As root user, edit:

```bash
vi /etc/systemd/system/tacticalagent.service
```

Change

```
ExecStart=/usr/local/bin/tacticalagent -m svc
```

to

```
ExecStart=/usr/local/bin/tacticalagent -m svc -log debug
```

then

```
systemctl daemon-reload
systemctl restart tacticalagent.service
```

**Mac**

In terminal window:

```bash
sudo launchtl list | grep -e mesh -e tacticalagent
```

##### Mesh Agent Recovery

Use Agents right click menu > `Agent recovery` > `Mesh Agent`

##### Tactical Agent Recovery

Use Agents right click menu > `Agent recovery` > `Tactical Agent`

**...OR**

**MeshCentral is online:**

Connect to `Terminal` (Admin Shell)

Run

```cmd
net stop tacticalrmm
net start tacticalrmm
```

Check if Tactical RMM agent is online.

**From Local Machine:**

Start / Restart Tactical RMM service from either `services.msc` or from Admin Command prompt:

```cmd
net stop tacticalrmm
net start tacticalrmm
```

Open `C:\Program Files\TacticalAgent\agent.log` to look for issues.

#### Windows Update Management

_The current Tactical RMM Windows Update process is relatively simple atm. As of right now, it is in the top 3 big items to be reworked._

##### TLDR: Tactical RMM Based Patching Recommendation

* Use the `Automation Policy` > `Patch Policy` to apply it to machines. The `Other` category is poorly named by Microsoft, those are the regular monthly updates and should be auto-approved.
* Be patient, and things will be patched (based on the policy).
* Trying to immediately approve patches to many machines **OR** block specific patches is a slow and manual process.

> **Note:** If you want more control of Windows patching right now, look into a script-based implementation of [PSWindowsUpdate](http://woshub.com/pswindowsupdate-module/).

**Be aware**: When you install the Tactical RMM Agent on a Windows computer it sets this:

```reg
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU
AUOptions (REG_DWORD):
1: Keep my computer up to date is disabled in Automatic Updates.
```

If you want to resume normal Windows patching and disable Tactical RMM updating functions, you should run the revert script at https://github.com/amidaware/community-scripts/blob/main/scripts/Win_Windows_Update_RevertToDefault.ps1.

**Where does it get updates from?** TRMM gets the list of Windows updates using this Microsoft API: https://docs.microsoft.com/en-us/windows/win32/api/_wua/

The Tactical RMM server updates an agent's patch list every 8 hours based on the patch policy to check for what to update, and what's installed.

> **Note:** Currently if the agent is not online at the time the patch policy is set to install, there is no "install as soon as it comes online".

> **Tip:** Trying to get reboots to happen at specific times after Windows update? Set your `Reboot After Installation` to: Never. Then create a task that reboots at your preferred date/time.

#### Log Files

You can find 3 sets of detailed logs at `/rmm/api/tacticalrmm/tacticalrmm/private/log`.

* `error.log` Nginx log for all errors on all TRMM URL's: rmm, api and mesh

```bash
tail -f /rmm/api/tacticalrmm/tacticalrmm/private/log/error.log
```

* `access.log` Nginx log for auditing access on all URL's: rmm, api and mesh (_this is a large file, and should be cleaned periodically_)

```bash
tail -f /rmm/api/tacticalrmm/tacticalrmm/private/log/access.log
```

* `django_debug.log` created by Django webapp

```bash
tail -f /rmm/api/tacticalrmm/tacticalrmm/private/log/django_debug.log
```

#### Failed / Successful Admin Logins

These are logged in `/rmm/api/tacticalrmm/tacticalrmm/private/log/access.log`

Successful Login

```log
10.0.0.18 - - [21/May/2025:00:01:43 -0400] "POST /v2/checkcreds/ HTTP/1.1" 200 13 "https://rmm.example.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
```

Failed Login

```log
10.0.8.62 - - [21/May/2025:00:01:13 -0400] "POST /v2/checkcreds/ HTTP/1.1" 400 17 "https://rmm.example.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
```

| Field                                      | Description                                                                 |
|-------------------------------------------|-----------------------------------------------------------------------------|
| `10.0.0.18`                               | Client IP address                                                           |
| `-`                                       | Unused (RFC 1413 identity)                                                  |
| `-`                                       | Unused (authenticated user ID)                                             |
| `[21/May/2025:00:01:43 -0400]`            | Timestamp (local time with timezone offset)                                |
| `"POST /v2/checkcreds/ HTTP/1.1"`         | HTTP request method, path, and version                                     |
| `200`                                     | HTTP status code (200 = OK/success) (400 = Failed)                          |
| `13`                                      | Response size in bytes (body only)                                         |
| `"https://rmm.example.com/"`         | Referer URL (origin of the request)                                        |
| `"Mozilla/5.0 (Windows NT 10.0;...)`      | User-Agent string (browser and OS info)                                    |

See the unsupported scripts section in references/integrations-and-tips.md for Fail2Ban configuration to limit password guessing.

---

## Installation Considerations

> **Note:** Paid Hosted TRMM is available! Open a ticket for pricing at https://support.amidaware.com.

There's pluses and minuses to each install type (Standard vs Docker *which is currently unsupported*). Be aware that:

- There is no migration script. Once you've installed with one type there is no "conversion". You'll be installing a new server and migrating agents manually if you decide to go another way.

> **Warning:** Tactical RMM does not support changing DNS names, so choose your names wisely. If you need to change your DNS name later a paid migration (https://support.amidaware.com) is possible.

### Debian vs Ubuntu

| Base RAM Usage | OS |
| --- | --- |
| 80MB | Clean install of Debian |
| 300MB | Clean install of Ubuntu |

Because of RAM usage alone, we recommend Debian 12.

### Traditional Install - **Officially supported**

- It's a VM/machine. One storage device to backup if you want to do VM based backups.
- You have a backup and restore script.
- Much easier to troubleshoot when things go wrong.
- Faster performance / easier to fine tune and customize to your needs.

### Docker Install
- Docker is more complicated in concept: has volumes and images.
- Backup/restore is via Docker methods only.
- Docker has container replication/mirroring options for redundancy/multiple servers.
- **NOT** officially supported and **NOT** recommended for production use at the moment unless you are very comfortable managing/troubleshooting docker.

### Azure VMs

Azure ranks their VM's in Series (https://azure.microsoft.com/en-us/pricing/details/virtual-machines/series/).

Tactical RMM will run poorly in CPU limited VMs. So **DO NOT** use Series A or Series B VMs. You will need at least a Series F or better. Also, make sure there is no IO throttling / IOPS limits for the VM.

The same applies for other big cloud providers that throttle low end VMs.

### Larger Installs

If you're having more than 200 agents, that's a larger install. You're probably also a business and making (and saving?) money with Tactical RMM.

You should be aware of server defaults like `Default script run time: 120 seconds`

Imagine you have 10 check, on 500 computers, running every 120 seconds.

For checks alone, that's 5000 writes every 120 seconds, or 3.6 million database entries created every 24hrs. Default retention on check history is 30 days, so your check history database is probably averaging 108,000,000 records before regular data purges. That's a lot of write-wear on your SSD-based storage layer.

Do you really need your Disk Space check running more than 1-2 times a day? Probably not.

Also consider staggering the times of all your checks, so that each check is naturally spreading the load on your server at more random intervals instead of focusing all checks at exactly the same time.

So in Summary:

- Adjust script default run intervals
- Don't have checks (and tasks) all run at the same time

If you have questions please open a ticket at https://support.amidaware.com to discuss looking at your server and configuration, load testing, and giving recommendations.

---

## Agent Installation

### UI

Click **Agents > Install Agent**.

You can also **right click on a site > Install Agent**. This will automatically fill in the client / site dropdown for you.

### Manual

The 'Manual' installation method requires you to first download the Inno Setup installer and call it using command line args.

This is useful for scripting the installation using Group Policy or some other batch deployment method.

This or the Powershell method are also the preferred method of installing to avoid unauthorized agents appearing in your Tactical RMM instance. See the FAQ section in references/integrations-and-tips.md for details.

### Dynamically Generated Executable

The dynamically generated exe is a standalone binary which is simply a wrapper around the Manual install method, using a single exe / command without the need to pass any command line flags to the installer.
All it does is download the Inno Setup installer and call it using predefined command line args that you choose from the web UI.
It "bakes" the command line args into the executable.
Please note that using this method can result in unauthorized agents appearing in your instance. See the FAQ section in references/integrations-and-tips.md for details.

### PowerShell

The PowerShell method is also a wrapper around the Manual install method and functionally identical to the dynamically generated EXE installer but in powershell format instead of EXE format.

> **Tip:** You can reuse the installer for any of the deployment methods, you don't need to constantly create a new installer for each new agent. The installer will be valid for however long you specify the token expiry time when generating an agent.

### Using a Deployment Link

The main benefit of this method is that the executable is generated only whenever the deployment download link is accessed, whereas with the other methods it's generated right away and the agent's version is hardcoded into the exe.
Using a deployment link will allow you to not worry about installing using an older version of an agent, which will fail to install if you have updated your RMM to a version that is not compatible with an older installer you might have lying around. The deployment link method uses the dynamic EXE method behind the scenes.

To create a deployment, from the web UI click **Agents > Manage Deployments**.

> **Tip:** Create a client / site named "Default" and create a deployment for it with a very long expiry to have a generic installer that can be deployed anytime at any client / site. You can then move the agent into the correct client / site from the web UI after it's been installed.

Copy / paste the download link from the deployment into your browser. It will take a few seconds to dynamically generate the executable and then your browser will automatically download the exe.

### Optional Installer Args

The following optional arguments can be passed to any of the installation method executables:

```text
--log debug
```

Will print very verbose logging during agent install. Useful for troubleshooting agent install.

```text
--silent
```

This will not popup any message boxes during install, including any error messages or the "Installation was successful" message box that pops up at the end of a successful install.

```text
--proxy "http://proxyserver:port"
```

Use a http proxy.

```text
--meshdir "C:\Program Files\Your Company Name\Mesh Agent"
```

Specify the full path to the directory containing `MeshAgent.exe` if using custom agent branding for your MeshCentral instance.

```text
--nomesh
```

Do not install MeshCentral agent during Tactical agent install. Note: Take Control, Remote Terminal and File Browser will not work.

You can get full command line options from (`--help`).

### Scripting Agent Installation

If you want to deploy the TRMM agent using AD, Intune, Mesh, TeamViewer, Group Policy GPO, etc, this is a sample CMD script for deploying Tactical.

**batch file**

> **Note:** You will need to replace `deployment url` with your custom deployment URL:

```bat
@echo off

REM Setup deployment URL
set "DeploymentURL=!!!REPLACEME!!!"

for /f "delims=" %%g in ('powershell -NoProfile -Command "(Get-Service -Name tacticalrmm -ErrorAction SilentlyContinue).Name"') do (
set "Name=%%g"
)

if not defined Name (
echo Tactical RMM not found, installing now.
if not exist "C:\ProgramData\TacticalRMM\temp" md "C:\ProgramData\TacticalRMM\temp"
powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force
powershell Add-MpPreference -ExclusionPath "C:\Program Files\TacticalAgent\*"
powershell Add-MpPreference -ExclusionPath "C:\Program Files\Mesh Agent\*"
powershell Add-MpPreference -ExclusionPath "C:\ProgramData\TacticalRMM\*"
powershell Add-MpPreference -ExclusionProcess "C:\Windows\Temp\is-*.tmp\tacticalagent*"
cd /d "C:\ProgramData\TacticalRMM\temp"
powershell Invoke-WebRequest "%DeploymentURL%" -Outfile tactical.exe
tactical.exe
) else (
echo Tactical RMM already installed Exiting
exit 0
)
```

**powershell**

```powershell
# Update variables
$deploymenturl = "<deployment URL>"
$agentstoinstall = 1 # Replace with the number of agents to install if greater than 20

# Do not modify below here
Add-MpPreference -ExclusionPath "C:\Program Files\Mesh Agent\*"
Add-MpPreference -ExclusionPath "C:\Program Files\TacticalAgent\*"
Add-MpPreference -ExclusionPath "C:\ProgramData\TacticalRMM\*"
Add-MpPreference -ExclusionProcess "C:\Windows\Temp\is-*.tmp\tacticalagent*"
$randomSleepTime = if ($agentstoinstall -gt 1) { Get-Random -Minimum 1 -Maximum (($agentstoinstall + 1) * 2) } else { 1 }
Start-Sleep -Seconds $randomSleepTime
Invoke-WebRequest $deploymenturl -OutFile (New-Item -Path "c:\ProgramData\TacticalRMM\temp\trmminstall.exe" -Force)
$proc = Start-Process "c:\ProgramData\TacticalRMM\temp\trmminstall.exe" -ArgumentList '-silent' -PassThru
Wait-Process -InputObject $proc
if ($proc.ExitCode -ne 0) {
    Write-Warning "$proc exited with status code $($proc.ExitCode)"
}
Remove-Item -Path "c:\ProgramData\TacticalRMM\temp\trmminstall.exe" -Force
```

**msi**

* Use `Agents` menu > `Manage Deployments`
* Generate a deployment link with an expiry date set to very far in the future, then access the link to download the executable.
* Create the msi (https://docs.microsoft.com/en-us/mem/configmgr/develop/apps/how-to-create-the-windows-installer-file-msi)
* Apply via GPO software deployment to the appropriate machines

**AD GPO**

For Active Directory Group Policy Deployment you can deploy via Batch File. It'll check to see if installed and only install when missing.

```bat
@echo off

REM Setup deployment URL
set "DeploymentURL=snip"

SC query "TacticalRMM" >nul 2>&1

IF %ERRORLEVEL% EQU 1060 (
    echo Tactical RMM not found, installing now.
    if not exist c:\ProgramData\TacticalRMM\temp md c:\ProgramData\TacticalRMM\temp
    powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted
    powershell Add-MpPreference -ExclusionPath "C:\Program Files\TacticalAgent\*"
    powershell Add-MpPreference -ExclusionPath "C:\Program Files\Mesh Agent\*"
    powershell Add-MpPreference -ExclusionPath C:\ProgramData\TacticalRMM\*
    powershell Add-MpPreference -ExclusionProcess "C:\Windows\Temp\is-*.tmp\tacticalagent*"
    cd c:\ProgramData\TacticalRMM\temp
    powershell Invoke-WebRequest "%DeploymentURL%" -Outfile tactical.exe
    tactical.exe
    exit /b 0
) ELSE (
    REM Service exists (it might be running or stopped, but it is installed)
    EXIT /B 0
)
```


### Script for Full Agent Uninstall

You can always use this to silently uninstall the agent on workstations:

**Windows Automatically**

```cmd
"C:\Program Files\TacticalAgent\unins000.exe" /VERYSILENT
```

**Mac**

Run the uninstall script at: https://github.com/amidaware/tacticalrmm/blob/develop/api/tacticalrmm/core/mac_uninstall.sh

**Linux**

Download: https://raw.githubusercontent.com/amidaware/tacticalrmm/develop/api/tacticalrmm/core/agent_linux.sh

Run: `chmod +x agent_linux.sh && ./agent_linux.sh uninstall`

### Reinstalling Mesh and Reconnecting to TRMM

Run this from **Send Command**:

```cmd
"C:\Program Files\Mesh Agent\meshagent.exe" -fullinstall
```

Then use **Agent Recovery > Mesh Agent**, and choose **Recover**.

### Stuck at "Downloading mesh agent..."?

Make sure TRMM can connect to Mesh. Run:

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py check_mesh
```

If there's an error, make sure you have MeshCentral setup correctly (see the MeshCentral section in this document).

### Install Linux Agent (beta)

To install:

1. Go to rmm.yourdomain.com and login.
2. Click on Agents > Install Agent.
3. Choose the Client, Site, Server or Workstation and Architecture (change expiry if required) as well as Linux.
4. Click Download.
5. If downloaded on the Linux machine you want to add as an agent (otherwise copy to machine using WinSCP or similar) open terminal.
6. cd to the folder you have downloaded the script to.
7. Run `chmod +x rmm-clientname-sitename-type.sh`
8. Run `sudo ./rmm-clientname-sitename-type.sh` and wait for script to complete.

If you changed the expiry time you could upload the script to any accessible server and deploy to multiple devices.

```text
-- debug
```

Will print very verbose logging during agent install. Useful for troubleshooting agent install.

### Linux Deployment Link

Currently there are no deploy links for Linux agents however you could use the following method if uploaded somewhere (website etc).

An example deployment script would be (note there's an install token in that script, so delete it when done if you're concerned):

```bash
wget scripturl
chmod +x rmm.sh
./rmm.sh
```

### Mac Agent Permissions

**macOS 15+ Sequoia**

Enable Screen Sharing under settings.

Top switch is the only item needed for TRMM access.

Do not enable anything else.

> **Warning:** Enabling `Anyone may request permission to control screen` and `VNC viewers may control screen with password` will enable Mac-proprietary VNC options that will make TRMM's VNC implementation fail.

> **Note:** This enabled the native VNC client on MacOS. If you don't limit in the `Allow access for` to `Only theses users` make certain you don't have other users or users without passwords.

**macOS 14 Sonoma and earlier**

Step 1: Open System Preferences
Click on the Apple logo in the top-left corner of your screen.
Select System Preferences from the dropdown menu.

Step 2: Navigate to Security & Privacy
In the System Preferences window, click on Security & Privacy.
At the top of the Security & Privacy window, click the Privacy tab.

Step 3: Grant Accessibility Permissions
In the list on the left, scroll down and select Accessibility.
If the padlock in the bottom-left corner is locked, click it and enter your password to make changes.
Click the plus (+) button under the list on the right side.
Navigate to and add tacticalagent from the /opt/tacticalagent/ folder and meshagent in the /opt/tacticalmesh/ folder.
Ensure both are checked in the list to grant them Accessibility Permissions.

Step 4: Grant Screen Recording Permissions
In the list on the left, find and select Screen Recording.
Unlock the padlock if necessary as described above.
Click the plus (+) button and add meshagent from the /opt/tacticalmesh/ folder, or check the boxes next to them if they're already listed.
A prompt may appear asking you to quit Meshcentral. Please do so to enable the permissions.

Step 5: Grant Full Disk Access
In the list on the left, scroll down and select Full Disk Access.
Unlock the padlock if necessary as described above.
Click the plus (+) button and add tacticalagent from the /opt/tacticalagent/ folder and meshagent from the /opt/tacticalmesh/ folder, or check the boxes next to them if they're already listed.

Finalizing the Setup
Restart Your Applications: Quit and restart Tactical RMM and Meshcentral for the changes to take effect.
Restart Your Mac: If the applications do not recognize the new permissions, a system restart may be necessary.

### Antivirus Exclusions

> **Warning:** You must add antivirus exclusions for the tactical agent. AV will usually flag the agent as a virus, since it technically is one due to the nature of this software. Adding the following exclusions will make sure everything works, including agent update:

```ps
#Windows Defender Exclusions for Tactical
Add-MpPreference -ExclusionPath "C:\Program Files\Mesh Agent\*"
Add-MpPreference -ExclusionPath "C:\Program Files\TacticalAgent\*"
Add-MpPreference -ExclusionPath "C:\ProgramData\TacticalRMM\*"
Add-MpPreference -ExclusionPath "C:\Windows\Temp\is-*.tmp\tacticalagent*"
Add-MpPreference -ExclusionProcess "C:\Program Files\TacticalAgent\tacticalrmm.exe"
Add-MpPreference -ExclusionProcess "C:\ProgramData\TacticalRMM\tacticalagent*"
Add-MpPreference -ExclusionProcess "C:\Windows\Temp\is-*.tmp\tacticalagent*"
```

See the FAQ section in references/integrations-and-tips.md for other AV screenshot examples.

---

## MeshCentral Integration

### Overview

Tactical RMM integrates with [MeshCentral](https://github.com/Ylianst/MeshCentral) for the following 3 functions:

- Take Control.
- Real time shell.
- Real time file browser.

> **Note:** MeshCentral has issues with Firefox, use a Chromium-based browser.

It should be noted that Tactical RMM and MeshCentral are 2 completely separate products and can run independently of each other.

They do not even have to run on the same box, however when you install Tactical RMM it simply installs MeshCentral for you with some pre-configured settings to allow integration.

It is highly recommended to use the MeshCentral instance that Tactical installs, since it allows the developers more control over it and to ensure things don't break.

### How Does It Work?

MeshCentral has an embedding feature that allows integration into existing products.

See *Section 14 - Embedding MeshCentral* in the [MeshCentral User Guide](https://ylianst.github.io/MeshCentral/meshcentral/#embedding-meshcentral) for a detailed explanation of how this works.

The Tactical RMM agent keeps track of your Mesh agents, and periodically interacts with them to synchronize the Mesh agent's unique ID with the Tactical RMM database.

When you do a take control / terminal / file browser on an agent using the Tactical UI, behind the scenes, Tactical generates a login token for MeshCentral's website and then "wraps" MeshCentral's UI in an iframe for that specific agent only, using it's unique ID to know what agent to render in the iframe.

### Customize Take Control Username

If you've enabled any of the remote control options such as "Notify user", "Prompt for consent" and "Show connection toolbar" and you'd like to change the name that users see, make sure the user has a First and/or Last name set in TRMM (Settings > User Administration). If you would also like your company name to show, you can set your company name in TRMM > Settings > Global Settings > MeshCentral. See the Tips and Tricks section in references/integrations-and-tips.md for details on enabling remote control options.

### Turn Off the Sync Feature

If you're having issues with the new MeshCentral sync feature added in TRMM v0.18.0 you can simply disable it to revert back to the previous behavior prior to this release, although you're probably just looking for way to get the old mesh interface back (see "Get a URL to Login to Mesh as the Mesh Superuser" below):

From TRMM's web interface go to Settings > Global Settings > MeshCentral

1. Un-check the "Sync Mesh Perms with TRMM" checkbox, and click Yes to the "are you sure" prompt.

2. Click "Save"

### Toggle a Full Permissions Re-sync

From TRMM's web interface go to Settings > Global Settings > MeshCentral

1. Un-check the "Sync Mesh Perms with TRMM" checkbox, and click Yes to the "are you sure" prompt.

2. Click "Save"

3. Re-open the same settings window and check the same checkbox, click yes to the prompt, and Save.

4. Wait a few minutes for the sync to fully complete in the background.

### Get a URL to Login to Mesh as the Mesh Superuser

This will generate a url that will log you into meshcentral as the superuser, the same way it used to be prior to TRMM Release 0.18.0

You should open this in a different browser than the one you're using for TRMM, or open in an incognito window.

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py get_mesh_login_url
```

### Modifying the Internal Mesh Port Configuration

By default, Tactical RMM configures the Mesh service to listen on the internal port 4430. Should there be a need to modify this default port within the Nginx or Mesh configuration, it is imperative to update Tactical RMM with the new port information. To accomplish this, the following entry must be added to the file `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
MESH_PORT = <new_port_number>
```

Replace `<new_port_number>` with the actual port number you have configured. For example, if the new port number is 1234, the entry should be as follows:

```python
MESH_PORT = 1234
```

Then, restart your entire server for changes to take effect.

### Running Your Own Existing or Separate MeshCentral Server

We do testing to make sure everything works with the version found at https://github.com/amidaware/tacticalrmm/blob/master/api/tacticalrmm/tacticalrmm/settings.py (look for MESH_VER).

Installation instructions for using your own MeshCentral server:

1. Run standard installation.
2. After installation is complete, disable meshcentral `sudo systemctl disable --now meshcentral`.
3. In TRMM Web UI go to Settings > Global Settings > MeshCentral and update values from your existing mesh (make sure to use a mesh superuser). Username MUST be all lowercase. For mesh token recovery see the troubleshooting documentation.
4. Add `USE_EXTERNAL_MESH = True` to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`
5. Restart TRMM server.

> **Note:** Mesh usernames are **CaSe sEnSiTive**

### Take Control Connect vs RDP Connect

When using `Take Control` from Tactical RMM you are using the Desktop function in MeshCentral

`Connect` button:

Right-click the button for options.

About the same a VNC, but it's not compatible with VNC. The original VNC protocol did not use JPEG, instead it uses RLE encoding or ZRLE. MeshCentral's remote desktop only uses JPEG (or WEBP in some cases) because browsers can decode JPEG easily.

The MeshAgent will split the desktop into 32x32 pixel tiles and see if any of the tiles have changed. If a group of tiles change since the last frame, a JPEG is sent to update the area.

`RDP Connect` button:

Is a browser based RDP client. It connects to the native RDP in versions of Windows that support inbound RDP connects. Pro, Workstation, Enterprise, Server, Terminal Server, RDS Server etc. You must enable RDP in Windows to be able to connect to it, it's not enabled by default (or enable when installing agent if supported).

> **Note:** It does not work for Windows Home because Home doesn't support incoming RDP connections.

### Remote Terminal How It Works

For the remote terminal, we launch a shell on the remote system and pipe VT100 terminal emulation to/from the browser. On the browser, we use XTermJS to view the terminal session.

### MeshCentral Options

There are many MeshCentral options that you can configure (see https://github.com/Ylianst/MeshCentral/blob/master/meshcentral-config-schema.json). Here are some you might want to investigate:

- `allowHighQualityDesktop`
- `desktopMultiplex`
- `userAllowedIP`
- `agentAllowedIP`
- `tlsOffload` (for proxy users)
- `maxInvalid2fa`

### Using Tactical RMM Without MeshCentral

Install Tactical RMM normally. Then, to disable the MeshCentral Server on the TRMM server run:

```bash
sudo systemctl disable --now meshcentral mongod
```

Then when installing an agent, make sure to pass the `-nomesh` flag to the installer (see the Optional Installer Args section above).

### Fixing Missing Agents in TRMM or Mesh

**Agent Missing in Mesh**

From the Script Library run: `TacticalRMM - Install Mesh Agent if it's not installed`

Then from trmm web ui right click agent > agent recovery > mesh agent

**Agent Missing in TRMM**

Use mesh to run the trmm agent installer with the `--nomesh` flag.

Then from trmm web ui right click agent > agent recovery > mesh agent

### MeshCentral Maintenance Status

MeshCentral is still actively being maintained (https://meshcentral2.blogspot.com/2023/10/meshcentral-windows-arm64-nodejs-v11.html), the lead devs had jobs in which they were paid by a corporation to develop MeshCentral, they now have got other jobs which means they are supporting and developing MeshCentral in their free time (like alot of other projects) this means development is slower but not that it isn't maintained anymore. If this changes or it becomes necessary to fix something that breaks or packages needing updated we are prepared to begin maintaining our own fork. The features of MeshCentral that TRMM uses are only the 3 items above and are extremely mature.
