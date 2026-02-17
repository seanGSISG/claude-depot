# Settings, Administration, and Management Commands

> Sources: functions/global_settings.md, functions/settings_override.md, functions/permissions.md, functions/django_admin.md, functions/url_actions.md, functions/user_ui.md, functions/software.md, functions/web_terminal.md, management_cmds.md, advanced_commands.md

## Table of Contents

- [Global Settings](#global-settings)
- [Overriding and Customizing Default Settings](#overriding-and-customizing-default-settings)
- [User Roles and Permissions](#user-roles-and-permissions)
- [Django Admin](#django-admin)
- [URL Actions](#url-actions)
- [User Interface Preferences](#user-interface-preferences)
- [Software Management](#software-management)
- [Web Terminal](#web-terminal)
- [Management Commands](#management-commands)
- [Advanced Commands](#advanced-commands)

---

## Global Settings

### General

- Enable agent automatic self update (Recommended setting: Enabled)
- Enable server side scripts
- Enable web terminal
- Default Agent timezone
- Default Date Format
- Default Server Policy
- Default Workstation Policy
- Default Alert Template
- Receive notifications on
- Agent Debug Level
- Clear faults on agents that haven't checked in after (days)
- Reset Patch Policy on Agents

### Email Alerts

See the Email Setup section in references/alerting-and-notifications.md

### SMS Alerts

See the SMS Alerts section in references/alerting-and-notifications.md

### Meshcentral

See the MeshCentral Integration section in references/architecture.md

### Custom Fields

See the Custom Fields section in references/scripting-and-variables.md

### Global Key Store

See the Key Store section in references/scripting-and-variables.md

### URL Actions

See the [URL Actions](#url-actions) section below.

### Web Hooks

See the Webhooks section in references/alerting-and-notifications.md

### Retention (TRMM Database)

These are the settings related to your Tools > Server Maintenance > Prune DB Tables.

Tactical RMM ships with data retention defaults that will work fine for most environments. There are situations, depending on the number of agents and checks configured, that these defaults need to be tweaked to improve performance.

#### Adjusting Data Retention

The options are:

- **Check History** - Will delete check history older than the days specified (default is 30 days).
- **Resolved Alerts** - Will delete alerts that have been resolved older than the days specified (default is disabled).
- **Agent History** - Will delete agent command/script history older than the days specified (default is 60 days).
- **Debug Logs** - Will delete agent debug logs older than the days specified (default is 30 days).
- **Audit Logs** - Will delete Tactical RMM audit logs older than the days specified (default is disabled).

To disable database pruning on a table, set the days to 0.

### API Keys

See references/api.md

---

## Overriding and Customizing Default Settings

### Admin User Browser Token Expiration and Idle Timeout Settings

The browser token expiration for admin users determines how long a session remains active before requiring re-authentication. By default, the token expires after 5 hours of inactivity. You can customize this idle timeout to automatically log out admin users after a shorter or longer period, depending on your security policy.

To change it, add the following code block to the end of `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
from datetime import timedelta

REST_KNOX = {
    "TOKEN_TTL": timedelta(days=30),
    "AUTO_REFRESH": True,
    "MIN_REFRESH_INTERVAL": 600,
}
```

Change `(days=30)` to whatever you prefer. Then run `sudo systemctl restart rmm.service` for changes to take effect.

### Using Your Own Wildcard SSL Cert

#### Before Install

Follow the instructions in the install guide for the `--use-own-cert` install flag. See the install server section in references/architecture.md for details.

#### Existing Install

1. Append the following two variables to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`, replacing the paths with the actual locations of your certificate and private key. The certificate must include the full chain:

```python
CERT_FILE = "/path/to/your/fullchain.pem"
KEY_FILE = "/path/to/your/privkey.pem"
```

2. Ensure that both files are readable by the `tactical` Linux user:

```bash
sudo chown tactical:tactical /path/to/your/fullchain.pem /path/to/your/privkey.pem
sudo chmod 440 /path/to/your/fullchain.pem /path/to/your/privkey.pem
```

3. Update all instances of `ssl_certificate` and `ssl_certificate_key` in the three Nginx configuration files located in `/etc/nginx/sites-enabled` to point to your certificate and private key paths.

4. Restart the services: `sudo systemctl restart nginx meshcentral rmm daphne`

### Use NATS Standard Instead of NATS Websocket

Prior to TRMM v0.14.0 (released 7/7/2022), agents NATS traffic connected to the TRMM server on public port 4222. If you have upgraded to v0.14.0 and have agents that won't work with websockets for some reason (too old TLS etc) then you can do the following to use NATS standard TCP on port 4222, just like how it was before v0.14.0:

For Windows agents:

Add the following registry string value (REG_SZ):

`HKEY_LOCAL_MACHINE\SOFTWARE\TacticalRMM\NatsStandardPort` with value `4222`

Then restart the `tacticalrmm` Windows service.

For Linux agents:

Add the following key/value pair to `/etc/tacticalagent`:

```json
{"natsstandardport": "4222"}
```

Then `sudo systemctl restart tacticalagent.service`

Just make sure port 4222 TCP is still open in your firewall and you're done.

### Configuring Custom Temp Dirs on Windows Agents

*Version added: Tactical RMM v0.15.10*

*Requires Agent v2.4.7*

By default, the Windows agent utilizes the `C:\ProgramData\TacticalRMM` directory for executing scripts and managing agent updates. However, it is possible to override this default directory by setting two optional registry string values (`REG_SZ`), specifying full paths to the desired directories:

`HKEY_LOCAL_MACHINE\SOFTWARE\TacticalRMM\WinTmpDir`: This registry value is used for running scripts and handling agent updates. Provide the full path to the custom directory.

`HKEY_LOCAL_MACHINE\SOFTWARE\TacticalRMM\WinRunAsUserTmpDir`: This registry value is specifically for executing Run As User scripts. Provide the full path to the custom directory.

Please note that these custom directories must already exist on the system, as the agent will not attempt to create them. Ensure that the desired directories are created and that the appropriate permissions are set before adding the registry values.

*Directory path cannot contain spaces, this is a known issue and will be fixed in a future release.*

To apply the changes, restart the `tacticalrmm` Windows service. The custom temporary directories will then be used for the respective tasks.

### Monitor NATS via its HTTP API

*Version added: Tactical RMM v0.15.1*

To enable NATS monitoring, add the following to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py` (replace with whatever port you want):

```python
NATS_HTTP_PORT = 8222
```

Then from the TRMM Web UI, do **Tools > Server Maintenance > Reload Nats Configuration**.

And then from your TRMM server CLI restart both the `rmm.service` and `nats.service` services.

### Modify the Placeholder Text for the Send Command Functionality

*Version added: Tactical RMM v0.15.12*

Users now have the flexibility to customize the placeholder text that is displayed in the 'Send Command' dialog. This customization can be achieved by defining any or all of the following three optional variables in `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
CMD_PLACEHOLDER_TEXT = "<Your customized command prompt text>"
POWERSHELL_PLACEHOLDER_TEXT = "<Your customized PowerShell prompt text>"
SHELL_PLACEHOLDER_TEXT = "<Your customized shell prompt text>"
```

To activate, restart the API with `sudo systemctl restart rmm` and then refresh the web interface.

### Define a Root User to Prevent Changes from Web UI

To define a "root" user who cannot be modified via the web UI, add the following line to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
ROOT_USER = "username"
```

Replace "username" with the actual username. After making this change, run `sudo systemctl restart rmm.service` to apply the changes.

### Adjusting Agent Check-In Intervals

The agent periodically communicates with the RMM server, sending various data about its status and environment at random intervals. These randomized intervals are designed to prevent the "thundering herd" problem, where too many agents would check in simultaneously, potentially overloading the server.

You can modify these intervals by adding one or more of the following variables to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`. Each variable is a Python tuple containing two values: the minimum and maximum interval times, specified in seconds. The agent will select a random interval within this range for each check-in.

The default check-in intervals are as follows:

```python
CHECKIN_HELLO = (30, 60)  # Agent heartbeat ("I'm alive")
CHECKIN_AGENTINFO = (200, 400)  # System info (logged-in user, boot time, RAM, etc.)
CHECKIN_WINSVC = (2400, 3000)  # Windows services and their status
CHECKIN_PUBIP = (300, 500)  # Agent's public IP address
CHECKIN_DISKS = (1000, 2000)  # Disk information and usage
CHECKIN_SW = (2800, 3500)  # Installed Windows software list
CHECKIN_WMI = (3000, 4000)  # Asset details (as seen in the "Assets" tab)
CHECKIN_SYNCMESH = (800, 1200)  # Agent's Mesh node ID
```

By adjusting these intervals, you can control how frequently the agent checks in with the RMM server for different types of data. This flexibility allows for balancing between server load and the frequency of updates.

After adding any of these settings, you must restart both the RMM service (`sudo systemctl restart rmm`) and the agent service. An easy way to restart the agent service is by using the "Tools > Recover All Agents" function in the TRMM web UI.

### Configuring Agent Check Jitter

*Version added: v1.0.0*

To prevent the thundering herd problem, where multiple agents send their check results simultaneously and overwhelm the server, a random jitter has been introduced. By default, this jitter is a random delay between 1 and 60 seconds.

To customize this behavior, add the following variable to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py` and adjust the values as needed, then restart the RMM service (`sudo systemctl restart rmm`):

```python
CHECK_INTERVAL_JITTER = (1, 60)
```

---

## User Roles and Permissions

### Permission Manager

Make sure you've setup at least 1 valid (Super User aka Administrator) role under _Settings > Permission Manager_.

1. Login as usual Tactical user
2. Go to Settings - Permissions Manager
3. Click New Role
4. You can call the role anything, e.g. "Admins"
5. Tick the Super User Box or relevant permissions required
6. Click Save then exit Permissions Manager
7. Go to Settings - Users
8. Open current logged in user or any other user and assign role (created above in step 6) in the Role drop down box
9. Click Save

Once you've set up a Super User role and assigned your primary user, you can create other Roles with more limited access.

**Tip:** If you are only trying to give permissions to one or more sites within a client, but not all of the sites, then leave the "Allowed Clients" field blank and only add sites to "Allowed Sites". If a client is set in "Allowed Clients" that will override any site perms and give access to all sites within that client, regardless of what sites are set.

### Permissions with Extra Security Implications

**Warning:** DO NOT use the Web Terminal for running the Tactical update script as it will stop the service running the web terminal and break your update.

- Use TRMM Server Web Terminal
- Run Scripts on TRMM Server

Both of these functions are running under the Linux user that you installed TRMM with (usually `tactical` if you followed the docs).

These have full access to your TRMM server's filesystem and as a result have the ability to become root if you have passwordless sudo enabled.

These can be very dangerous features if not handled with care so think carefully before you enable/use them.

These features can be disabled from the web UI in Global Settings.

They can also be disabled at the filesystem level (which overrides the setting in Global Settings) by adding any of these variables to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
TRMM_DISABLE_WEB_TERMINAL = True
TRMM_DISABLE_SERVER_SCRIPTS = True
```

After adding these make sure they take effect by running `sudo systemctl restart rmm daphne celery celerybeat`

**Note for Docker Installs:** Only update the `.env` file and issue command `docker compose down && docker compose up -d` for the variables to take effect.

---

## Django Admin

**Warning:** Do not use the Django admin unless you really know what you're doing. You should never need to access it unless you are familiar with Django or are instructed to do something here by one of the developers.

The Django admin is basically a web interface for the postgres database.

As of Tactical RMM v0.4.19, the Django admin is disabled by default.

To enable it, edit `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py` and change `ADMIN_ENABLED` from `False` to `True` then run these 2 commands:

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py collectstatic --no-input

sudo systemctl restart rmm.service
```

Login to the Django admin using the same admin credential that was created during the `install.sh` script (ie the web UI login).

If you did not save the Django admin URL (which was printed out at the end of the install script), check the `local_settings.py` file referenced above for the `ADMIN_URL` variable. Then simply append the value of this variable to your API domain (`https://api.EXAMPLE.COM/`) to get the full URL.

Example of a full Django admin URL:

```
https://api.example.com/JwboKNYb3v6K93Fvtcz0G3vUM17LMTSZggOUAxa97jQfAh0P5xosEk7u2PPkjEfdOtucUp/
```

---

## URL Actions

URL Actions will run against an agent and open a configured URL in a new browser tab or window. This allows for integrations with various remote viewing software.

### Adding URL Actions

In the dashboard, browse to **Settings > Global Settings > URL Actions**. The available options are:

- **Name** - This identifies the URL Action in other parts of the dashboard
- **Description** - Optional description for the URL Action
- **Pattern** - This is the actual URL pattern that will open in the new browser tab/window. This field supports variables from the Global Keystore and Script Variables. See references/scripting-and-variables.md for details on available variables.

#### URL Pattern Example

**Note:** Variable names are *case sensitive*!

```
https://remote.example.com/connect?API_KEY={{global.API_KEY}}&agent_id={{agent.Remote ID}}
```

The above example uses a value defined in the **global keystore** named *API_KEY* and an **Agent custom field** called *remote id*. The URLs are properly encoded to work with any special characters or spaces returned in the values.

### Running URL Actions

In the agent table, right-click on the Agent and select **Run URL Action** and select the action to run.

You can also create a shortcut for this by setting the default double-click action to open a URL action:

Click on your username in the top right of the web UI > **Preferences**, then select **Run URL Action** and then select the URL action. The URL action will now run when you double click on a row in the Agent table in the dashboard.

---

## User Interface Preferences

Click on your username at the top right of the dashboard > Preferences to access user interface customization options.

---

## Software Management

### Software Tab

The Software tab displays installed software on a selected agent.

### Install Software Button

This will give you a list of software installable from the Official Chocolatey Community repository (https://community.chocolatey.org/packages).

### Uninstall Button

This button will pull the software's uninstall string as set by the software developer.

You should be aware that:

- You can use the Agents history tab for log data
- If you don't select `Run as user` all commands are sent via the TRMM agent native security context: `SYSTEM`. See the RunAsUser functionality section in references/architecture.md for details. If the developer hasn't designed it to work from there you might get a stuck uninstaller with permission problems, or prompting with questions that can't be answered.
- msiexec doesn't log by default. If it's not uninstalling properly, you'll need to append `/l*v c:\path\to\somelog.txt` to the uninstall string and then check that log file and troubleshoot accordingly. Microsoft docs has other MSI command line options.

---

## Web Terminal

The Web Terminal provides web-based terminal access for remote command execution on agents.

**Warning:** DO NOT use the Web Terminal for running the Tactical update script as it will stop the service running the web terminal and break your update.

The Web Terminal can be enabled or disabled in Global Settings. It can also be disabled at the filesystem level by setting `TRMM_DISABLE_WEB_TERMINAL = True` in `local_settings.py`. See the [Permissions with Extra Security Implications](#permissions-with-extra-security-implications) section above for full details.

---

## Management Commands

To run any of the management commands first login to your server as the user used to install TRMM (eg `su - tactical`) and activate the python virtual env:

**Standard install:**

```bash
cd /rmm/api/tacticalrmm
source ../env/bin/activate
```

**Docker install:**

```bash
docker exec -it trmm-backend /bin/bash
/opt/venv/bin/python /opt/tactical/api/manage.py shell
```

**Dev Docker:**

```bash
docker exec -it trmm-api-dev env/bin/python manage.py shell
```

### Bulk Delete Agents (Last Check-In, Agent Version, Site, or Client)

If you want to remove old agents based on time, age, or location or for client offboarding - it's a best practice to first test the removal.

```bash
python manage.py bulk_delete_agents --days 60
python manage.py bulk_delete_agents --agentver 1.5.0
python manage.py bulk_delete_agents --site examplesite
python manage.py bulk_delete_agents --client exampleclient
python manage.py bulk_delete_agents --hostname examplehostname
```

Then run the deletion:

```bash
python manage.py bulk_delete_agents --days 60 --delete
python manage.py bulk_delete_agents --agentver 1.5.0 --delete
python manage.py bulk_delete_agents --site examplesite --delete
python manage.py bulk_delete_agents --client exampleclient --delete
python manage.py bulk_delete_agents --hostname examplehostname --delete
```

**Notes:**

- You must specify at least one of `--days`, `--agentver`, `--site`, `--client`, or `--hostname`.
- You can combine multiple parameters (e.g., `--site examplesite --days 90`) to narrow down agents further.
- Without the `--delete` flag, the command will only list agents that match.
- With the `--delete` flag, the agents will be uninstalled and deleted.

Example Bash one-liner to delete multiple agents at once by hostname (`hosts.txt` file should contain one hostname per line):

```bash
for i in $(cat hosts.txt); do python manage.py bulk_delete_agents --hostname $i --delete; done
```

### Reset a User's Password

```bash
python manage.py reset_password <username>
```

### Reset a User's 2FA Token

```bash
python manage.py reset_2fa <username>
```

### Delete a User

```python
python manage.py shell
from accounts.models import User
User.objects.get(username="changeme").delete()
```

### Find All Agents That Have X Software Installed

```bash
python manage.py find_software "adobe"
```

### Find All Agents That Have X Windows Service and Show the Service Status

```bash
python manage.py find_services "quickbooks"
```

### Set a Specific Windows Update to Not Install

```python
python manage.py shell
from winupdate.models import WinUpdate
WinUpdate.objects.filter(kb="KB5007186").update(action="ignore", date_installed=None)
```

### Show Outdated Online Agents

```bash
python manage.py show_outdated_agents
```

### Log Out All Active Web Sessions

```bash
python manage.py delete_tokens
```

### Reset All Auth Tokens for Install Agents and Web Sessions

```python
python manage.py shell
from knox.models import AuthToken
AuthToken.objects.all().delete()
```

### Check for Orphaned Tasks on All Agents and Remove Them

```bash
python manage.py remove_orphaned_tasks
```

### Get a URL to Login to Mesh as the Mesh Superuser

```bash
python manage.py get_mesh_login_url
```

### Create a MeshCentral Agent Invite Link

```bash
python manage.py get_mesh_exe_url
```

### Bulk Update Agent Offline / Overdue Time

Change offline time on all agents to 5 minutes:

```bash
python manage.py bulk_change_checkin --offline --all 5
```

Change offline time on all agents in site named *Example Site* to 2 minutes:

```bash
python manage.py bulk_change_checkin --offline --site "Example Site" 2
```

Change offline time on all agents in client named *Example Client* to 12 minutes:

```bash
python manage.py bulk_change_checkin --offline --client "Example Client" 12
```

Change overdue time on all agents to 10 minutes:

```bash
python manage.py bulk_change_checkin --overdue --all 10
```

Change overdue time on all agents in site named *Example Site* to 4 minutes:

```bash
python manage.py bulk_change_checkin --overdue --site "Example Site" 4
```

Change overdue time on all agents in client named *Example Client* to 14 minutes:

```bash
python manage.py bulk_change_checkin --overdue --client "Example Client" 14
```

**Tip:** You can cron it on the server to run every 30 minutes with something like:

```bash
*/30 * * * * /rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py bulk_change_checkin --overdue --all 10 > /dev/null 2>&1
```

### Script-Based Functions

Delete agents by client and site name by API - see the community scripts repository for a PowerShell-based mass delete script.

---

## Advanced Commands

**DANGER:** Use all commands here with caution, there is no undo. Have backups. You have been warned.

### Server Commands

#### Remove Agent History for One Agent

Permanently deletes all history records for a specific agent. This is useful for cleaning up agents with corrupted history or reducing database size for agents.

**Keywords:** agent history, delete history, cleanup, database maintenance, audit trail, task history, agent cleanup

**Parameters:**
- Replace `CHANGEME` with the exact hostname of the target agent
- Ensure the agent hostname exists before running the command

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py shell -c 'from agents.models import Agent,AgentHistory;agent = Agent.objects.get(hostname="CHANGEME");to_delete = AgentHistory.objects.filter(agent=agent).values_list("id", flat=True);AgentHistory.objects.filter(id__in=to_delete).delete()'
```

#### Get Mapping of Agent ID to Mesh ID

TRMM Agent unique ID and MeshCentral nodeID:

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py shell -c 'from agents.models import Agent; [print((i.agent_id, f"node//{i.hex_mesh_node_id}")) for i in Agent.objects.only("mesh_node_id") if i.mesh_node_id and i.hex_mesh_node_id != "error"]'
```

#### Maintenance Mode Toggle for All Agents

Set all agents in Maintenance Mode:

```bash
echo "from agents.models import Agent; Agent.objects.update(maintenance_mode=True)" | /rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py shell
```

Undo all agents from Maintenance Mode:

```bash
echo "from agents.models import Agent; Agent.objects.update(maintenance_mode=False)" | /rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py shell
```
