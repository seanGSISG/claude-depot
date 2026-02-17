# Integrations, Tips, FAQ, and Guides

> Sources: faq.md, tipsntricks.md, 3rdparty_bitdefender_gravityzone.md, 3rdparty_zammad.md, guide_gettingstarted.md, functions/examples-serial-number.md, functions/BitLocker-Key.md, functions/snmp_checks.md, functions/remote_bg.md, roadmap.md

## Table of Contents

- [FAQ](#faq)
  - [Reporting](#how-do-i-get-reporting)
  - [Antivirus Sandbox Agents](#help-ive-been-hacked-and-there-are-weird-agents-appearing-in-my-tactical-rmm)
  - [Code Signing](#why-isnt-the-code-signing-free)
  - [Privacy and Compliance](#is-tactical-rmm-compliant-with-privacy-laws)
  - [Linux/macOS Agents](#linuxmacos-agents)
  - [User Management](#i-forgot-my-username-to-login-to-the-web-ui-how-can-i-find-it)
  - [Server Migration](#i-want-to-move-andor-migrate-my-server-how-do-i-do-it)
  - [Checks vs Tasks](#should-i-use-a-check-or-a-task)
  - [Terminology](#terminology)
- [Tips and Tricks](#tips-and-tricks)
  - [Monitoring Endpoint](#monitor-your-trmm-instance-via-the-built-in-monitoring-endpoint)
  - [Server Monitoring](#server-monitoring)
  - [Customize User Interface](#customize-user-interface)
  - [URL Search Filter](#url-search-filter)
  - [MeshCentral Tips](#meshcentral)
  - [Scripts Tips](#scripts)
  - [3rd Party Software Patching](#3rd-party-software-patching)
  - [Run Intervals for Checks](#run-intervals-for-checks)
  - [False SMS and Email Alerts](#getting-false-sms-and-email-alerts-from-scripts)
- [BitDefender GravityZone Deployment](#bitdefender-gravityzone-deployment)
  - [Deploying GravityZone](#how-to-deploy-bitdefender-gravityzone)
  - [Onboarding a New Company](#how-to-onboard-a-new-company)
  - [Alert Types](#alert-types)
  - [Troubleshooting](#troubleshooting-and-problem-resolution)
- [Zammad Integration](#zammad-integration)
- [Getting Started Guide](#getting-started-guide)
  - [Post Install Checklist](#post-install)
  - [Automation Policies Setup](#setup-automation-policies)
  - [Multiple Users](#multiple-users)
  - [Maintenance Schedule](#every-75-days)
  - [Dont Do These Things](#dont-do-these-things)
- [Examples: Serial Number URL Actions](#examples-serial-number-url-actions)
  - [URL Actions for Support Pages](#create-run-url-action-to-computer-support-page)
  - [LAPS Setup](#setup-laps---local-administrator-password-solution)
- [BitLocker Recovery Key](#bitlocker-recovery-key)
- [SNMP Checks](#snmp-checks)
- [Remote Background](#remote-background)
- [Roadmap](#roadmap)

---

## FAQ

### How do I get Reporting?

See the Reporting FAQ section in references/reporting.md

### Help! I've been hacked and there are weird agents appearing in my Tactical RMM!

No, you haven't.

1. You used the Dynamic EXE/Deployment EXE installation method (see the agent installation section in references/architecture.md), and the installer was scanned by an antivirus.

2. It didn't recognize the exe.

3. You have the option enabled to submit unknown applications for analysis.

4. They ran it against their virtualization testing cluster.

**To prevent this from happening**: either turn off file uploads in your AV settings, or use the Powershell or Manual install methods (see the agent installation section in references/architecture.md).

### Can I __________?

If you've been sent a link to this, we are not going to allow or support things like your request. The reason is because it would facilitate people avoiding to pay for/supporting Tactical RMM for these/similar premium paid features.

So the answer is No.

### I'd like to be able to __________?

If you've been sent a link to this, it's possible that we could support this but it would most likely be a paid premium feature. Please contact Commercial Support to discuss further.

### Why isn't the Code Signing free?

It is recommended because it helps the project mature, Tactical is source available and free. Community support is also free on top of this we have spent a lot of time developing the docs, please follow them!
With many source available (and similar) projects devs get bored of them because they don't make money out of it. So here is your reasons to pay for code signing and also why it was discussed and implemented.

1. Code signing costs a lot of money. OV code signing requires a legitimate legal business...Amidaware was setup for this purpose. Code signing + operating a business costs thousands of dollars a year.
2. It helps the project move forward and it can support devs spending time on it, they have lives, wives, jobs and kids which all demands attention.
3. It should stop bad actors using it maliciously.
4. It helps with AVs detecting it as anything malicious.

We had github sponsors up for many months before code signing. Very few people donated, some $5 and $10. maybe $40 a month. Once we announced code signing, sponsors came in like crazy, and many people upgraded their $5 to $55 so whilst everyone believes people would gladly donate, that's just not the case. We already tried.

### Is Tactical RMM Compliant with Privacy Laws?

Tactical, as a self-hosted solution, offers the potential for GDPR and HIPAA compliance as well as many other privacy laws, but its adherence largely depends on the hosting environment and how it's configured. Since you have full control over the hosting, you bear a significant responsibility for compliance. By default, the Tactical server collects essential information which is displayed in the dashboard on each agent. None of this data is transmitted outside of the Tactical server, enhancing data security. Encryption at rest is possible at the file system level, contingent on your hosting infrastructure. Additionally, all communications between the Tactical server and your clients are encrypted in transit, enhancing security. Furthermore, Tactical incorporates an audit log that records all actions, assisting in tracking and ensuring accountability. However, it's crucial to be cautious about collector scripts, as they could potentially alter data collection practices, potentially leading to non-compliance if not carefully managed and configured in accordance with GDPR and HIPAA regulations. Therefore, maintaining a vigilant approach to configuration and monitoring is essential when utilizing Tactical for compliance purposes.

### Linux/macOS Agents

**Why do I see?**

```
Missing code signing token
400: Bad Request
```

You must have a paid code signing certificate while Linux/macOS support is in the post-alpha/beta:

- Code signing makes these installs easy and is a benefit offered to code signing sponsors.
- DIYer can read thru the code and... DIY.

This is primarily for 2 reasons:

1. As this has been a sponsorship goal it seems only fair that those who contributed to make this a reality get early access to easy agent installs.
2. We're looking for good bug reports from active users to get these agent into production ready code.

### Who is Amidaware Inc?

The Legal entity behind Tactical RMM.

### How do I move an agent to another client/site?

Right click on the agent > Edit agent. Then select the new site from the dropdown.

### Is it possible to use XXX with Tactical RMM

While it _may be possible_ to use XXX, we have not configured it and therefore it is Unsupported. We cannot help you configure XXX as it pertains to **your environment**.

### Is it possible to use XXX proxy server with Tactical RMM

If you wish to stray from the easy install of a standard install in a VPS (see the installation section in references/architecture.md), you need to have the knowledge on how to troubleshoot your own custom environment.

The most common reasons you're running a proxy are:

1. Because you only have a single public IP and you already have something on Port 443. **Workaround**: Get another public IP from your ISP.
2. Because you want to monitor traffic for security reasons: You're a Networking Wizard.

There are some unsupported implementations that others have done, but be aware it is Unsupported and if you're requesting help in Discord please let us know in advance.

### I want to use a different port other than 443

I want to use a different port for Tactical RMM because my public IP on 443 is currently being used by something else. PAT (aka Port Address Translation)

That is not possible at this time (see GitHub issue #999).

Your options are:

- Run in a VPS
- Get another Public IP from your ISP
- Use another proxy server in an unsupported configuration
- Run TRMM in a SDWAN like Netmaker/Zerotier/Tailscale/Sunbird etc

### How do I do X feature in the web UI?

A lot of features in the web UI are hidden behind right-click menus. Almost everything has a right click menu so if you don't see something, try right clicking on it.

### Can I run Tactical RMM locally behind NAT without exposing my RMM server to the internet?

Yes, you will just need to setup local DNS for the 3 subdomains, either by editing host files on all your agents or through a local DNS server.

Similarly asked: Can I use onsite DNS servers (I don't want my server accessible from the internet).

Yes, you can use (only) internal DNS (if you want) for api, mesh and rmm domains. You don't have to put these records in your public DNS servers.

The Let's Encrypt DNS `TXT` wildcard cert request process **does not** require any inbound connection from the internet (port forwarding etc) to be enabled. This does not expose your RMM server to the internet in any way.

### I forgot my username to login to the web UI, how can I find it?

Do the following as the `tactical` user which will list all user accounts:

```bash
tactical@trmm:~$ /rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py shell
Python 3.11.3 (main, Apr  9 2023, 04:41:05) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from accounts.models import User
>>> User.objects.exclude(is_installer_user=True).filter(agent__isnull=True)
```

### How do I make another superuser for logging into rmm.

```sh
cd /rmm/api/tacticalrmm/
source ../env/bin/activate
python manage.py createsuperuser
```

### I am locked out of the web UI. How do I reset my password?

SSH into your server and run:

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py reset_password <username>
```

### How do I reset password or 2 factor token?

#### From TRMM Admin GUI

From the web UI, click **Settings > User Administration** and then right-click on a user.

#### From SSH

Login with SSH using your install ID (eg `tactical`)

and Reset Password (see the management commands section in references/settings-and-admin.md)

**OR**

Reset 2FA token for a TRMM user:

**Standard install:**

```bash
/rmm/api/env/bin/python /rmm/api/tacticalrmm/manage.py reset_2fa <username>
```

**Docker install:**

```bash
docker exec -it trmm-backend /bin/bash
```

Then simply log out of the web UI and next time the user logs in they will be redirected to the 2FA setup page which will present a barcode to be scanned with the Authenticator app.

### How do I recover my MeshCentral login credentials?

From Tactical's web UI: **Settings > Global Settings > MeshCentral**

Copy the username, then ssh into the server and run:

```bash
cd /meshcentral/
sudo systemctl stop meshcentral.service
node node_modules/meshcentral --resetaccount <username> --pass <newpassword>
sudo systemctl start meshcentral.service
```

to reset Mesh password for user.

> **Warning:** Resetting the default admin in mesh will break agent installs if you don't also update the mesh connection info in Settings > General > Meshcentral and make sure it's working (see troubleshooting section).

### DNS can't find record

Q. My DNS isn't working.

A. Make sure it's correctly formatted, as most DNS providers add in the domain automatically.

### License FAQ

If you're not certain if your business use case is allowed by the license please open a ticket at https://support.amidaware.com and let us know how you're planning on using it.

### Can I password protect the uninstalling of the TRMM agent?

From the client / agent side: Installing and uninstalling software is part of system administration. Administrators can install / uninstall. Users cannot. Configure your system appropriately.

From the TRMM Admin panel: Use `Permissions Manager` to restrict your techs permissions (see the permissions section in references/settings-and-admin.md).

To hide Tactical RMM from the Control Panel's Program and Features, use the following PowerShell command:

```powershell
Set-ItemProperty -Path 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{0D34D278-5FAF-4159-A4A0-4E2D2C08139D}_is1' -Name 'SystemComponent' -Value 1 -Type DWord
```

To undo the changes and make Tactical RMM visible again in the Control Panel, use the following PowerShell command:

```powershell
Remove-ItemProperty -Path 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{0D34D278-5FAF-4159-A4A0-4E2D2C08139D}_is1' -Name 'SystemComponent'
```

Alternative: Check out community scripts like `Win_TRMM_Agent_Locker.ps1` and `Win_TRMM_Agent_unLocker.ps1` in the amidaware/community-scripts repository.

### I want to move and/or migrate my server? How do I do it?

#### Changing a public IP or private LAN IP address?

TRMM doesn't care about that. TRMM uses DNS, and only the 3 configured DNS names used during install. Make them right, and you'll be fine (with a backup/restore script if necessary).

#### Are you keeping the same DNS names?

Use the backup and restore process.

> **Note:** It's best practice to make sure you're running the latest version before running the backup script, and make sure you have the latest backup script. It does change.

#### Are you wanting to change the DNS names on the server?

There is no supported way to do this because of the complexities involved. A paid migration service is offered - open a ticket at https://support.amidaware.com for pricing.

If you want to try it yourself, your best bet is to use another service outside of TRMM to uninstall and reinstall your agents to a new TRMM server. Then you'll need to migrate all your automation policies, alert policies, patch policies, custom scripts, reports, users, user permissions, user settings, custom fields, api keys, key store items, email configuration, sms configuration etc from your old TRMM server to the new one manually.

### If you received this link

You have asked for assistance in Discord or Github, and you have not provided enough information.

Please provide the following information:

```
Install type (Standard/Docker) and amount of RAM on server?
Did you deviate IN ANY WAY from these Standard server install instructions https://docs.tacticalrmm.com/install_server/ ?
Did you deviate IN ANY WAY from these Docker server install instructions https://docs.tacticalrmm.com/install_docker/ ?
Where is the server (VPS/onprem)?
New/old install? Rough age of TRMM server (days/weeks/months)?

Server Install Specific questions:
What OS/version is TRMM installed on.
Using a real domain?
Did letsencrypt finalize and work?
Have you looked at the troubleshooting steps to see if something there is appropriate to you situation? Test DNS from an agent etc. https://docs.tacticalrmm.com/troubleshooting/
Run the Server Troubleshooting Script and DM the person (from @Support) that is working with you https://docs.tacticalrmm.com/troubleshooting/#server-troubleshooting-script
What kind of ssl certs? Let's Encrypt, or purchased.
Check Expiry date of your certificates in the browser (at https://rmm.example.com/ )

Network Troubleshooting
Are you using a proxy?
Are you a wizard? See https://docs.tacticalrmm.com/unsupported_guidelines/
If so, what's in the network between agent and server?

Agent Troubleshooting
Is there ANY 3rd party Antivirus installed on the computer?
Is there any network based filtering/AV filtering?

Asking yourself questions like: When did it go from working to broken? What changed during that time? This will help you.
```

We can not help you until we understand your setup. Just posting an error log is not enough information.

### Should I use a Check or a Task?

**Checks:**

- Run every 2-1440 mins (1 day max)
- Results are naturally graphed, and not logged to the agents "History" tab

**Tasks:**

- Is run using the Windows Task Scheduler on the agent.
- Although multiple times/day can be scheduled it's complicated and will clutter up your "History" tab.
- Best for periodic script runs that run daily/weekly/monthly/onboarding/once

See the checks section in references/checks-tasks-policies.md for full details on check configuration, and the automated tasks section for task scheduling.

### Is Tactical RMM vulnerable to Log4j

No.

### Terminology

**Code Signing:** A windows .exe cryptographic signing process that can't be forged. The only way to reliably whitelist your TRMM agent is to have a Code signed agent that you can give the signers public key to your security software to whitelist.

**Mac/Linux Pre-Compiled binaries:** Are provided by Amidaware so you can install agents on Mac and Linux. This requires sponsorship. If you want to test Mac/Linux agents please contact support and open a ticket to request a 7 day hosted trial.

---

## Tips and Tricks

### Monitor your TRMM Instance via the Built-in Monitoring Endpoint

> For TRMM Release v1.0.0 and later, see the migration guide below.

The health check endpoint provides key metrics and statuses about your RMM instance. It is designed for integration with monitoring tools like Uptime Kuma or other similar solutions.

Generate a random string to be used as a token and append it to the bottom of `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py` like this:

```python
MON_TOKEN = "SuperSekretToken123456"
```

Then restart Django to activate the endpoint with `sudo systemctl restart rmm.service`

Send a GET request to `https://api.yourdomain.com/core/v2/status/` with the `X-Mon-Token` header.

**Example using curl**:

```
curl -H "X-Mon-Token: SuperSekretToken123456" https://api.yourdomain.com/core/v2/status/
```

The endpoint returns a JSON object with the following structure:

**Response Fields**

| **Field**                 | **Type**          | **Description**                                                                                     | **Example**       |
|---------------------------|-------------------|-----------------------------------------------------------------------------------------------------|-------------------|
| `version`                | `str`            | The current version of the RMM software.                                                           | `"1.0.0"`        |
| `latest_agent_version`   | `str`            | The latest available version of the agent.                                                         | `"2.9.0"`         |
| `agent_count`            | `int`            | The total number of agents connected to the RMM instance.                                          | `345`               |
| `client_count`           | `int`            | The total number of clients registered in the RMM.                                                 | `14`               |
| `site_count`             | `int`            | The total number of sites registered in the RMM.                                                   | `34`               |
| `disk_usage_percent`     | `int`            | The percentage of disk space used by the RMM instance.                                             | `43`              |
| `mem_usage_percent`      | `int`            | The percentage of memory usage by the RMM instance.                                                | `54`              |
| `days_until_cert_expires`| `int`            | The number of days until the SSL certificate expires.                                              | `43`              |
| `cert_expired`           | `bool`           | Indicates if the SSL certificate has already expired.                                              | `false`           |
| `redis_ping`             | `bool`           | Indicates if the Redis service is responding.                                                      | `true`            |
| `celery_queue_len`       | `int`            | The current number of tasks in the Celery queue. A high number (> 100) usually means your queue is stuck. | `0`            |
| `celery_queue_health`    | `str`            | The health status of the Celery queue. Possible values are `"healthy"` or `"unhealthy"`.           | `"healthy"`       |
| `nats_std_ping`          | `bool`           | Indicates if the NATS standard service is responding.                                              | `true`            |
| `nats_ws_ping`           | `bool`           | Indicates if the NATS WebSocket service is responding.                                             | `true`            |
| `mesh_ping`              | `bool`           | Indicates if the MeshCentral service is responding.                                                | `true`            |
| `services_running`       | `dict[str, bool]`| A dictionary of service names with their respective running statuses.                              | See below        |

**Example Response**

```json
{
    "version": "1.0.0",
    "latest_agent_version": "2.8.0",
    "agent_count": 345,
    "client_count": 14,
    "site_count":34,
    "disk_usage_percent": 43,
    "mem_usage_percent": 54,
    "days_until_cert_expires": 43,
    "cert_expired": false,
    "redis_ping": true,
    "celery_queue_len": 0,
    "celery_queue_health": "healthy",
    "nats_std_ping": true,
    "nats_ws_ping": true,
    "mesh_ping": true,
    "services_running": {
        "mesh": true,
        "daphne": true,
        "celery": true,
        "celerybeat": true,
        "redis": true,
        "nats": true,
        "nats-api": true
    }
}
```

#### Monitoring Endpoint v2 Migration Guide

Starting with Tactical RMM release v1.0.0, the monitoring endpoint has been upgraded from `/core/status/` to `/core/v2/status/` (v2) with improved response structure and authentication method. The changes include:

- New Endpoint: The URL has changed from `/core/status/` to `/core/v2/status/`.
- Authentication Method: Instead of sending the token in the request body, it must now be included in the `X-Mon-Token` request header.
- HTTP Method Change: The request type has changed from `POST` to `GET`.
- Enhanced Response Data: The new response includes additional fields such as `celery_queue_len`, `celery_queue_health`, `nats_std_ping`, `nats_ws_ping`, and `mesh_ping`.
- Removed fields: The `services_running` response no longer includes `django`, `nginx`, and `postgres` because if any of these services were not running, the monitoring endpoint itself would be inaccessible, making their inclusion redundant. The `mongo` service has also been removed as you should already be using postgresql now.

### Server Monitoring

Monitor Network usage: <https://humdi.net/vnstat/>

Realtime Everything Usage (only run when needed because it uses a lot of resources): <https://learn.netdata.cloud/docs/agent/packaging/installer/methods/kickstart>

### Customize User Interface

At the top right of your web administration interface, click your **Username > preferences**. Set default tab: Servers | Workstations | Mixed

### Use the Filters in the Agent List

The agent list supports filtering to narrow down the view.

### URL Search Filter

You can append `/?search=XXX` to the web URL to create a saved filter. This allows you to:

- Quickly search for specific agents, computers, or clients
- Create bookmarks for frequently accessed filtered views
- Share filtered views with team members via URL

**Example**:

```
https://rmm.yourdomain.com/?search=server01
```

This will automatically populate the search filter with "server01" when the page loads.

### MeshCentral

Tactical RMM is actually 2 products: An RMM service with agent, and a secondary MeshCentral install that handles the `Take Control` and `Remote Background` stuff.

Want to download multiple files?

> ZIP zip's the currently selected file(s) and saves it in the current directory. Then you can download the ZIP. It doesn't download and ZIP on the fly.

If you want to enable automatic clipboard transfers just click the option under the Settings button during a desktop session.

#### Adjust Settings

Right-click the connect button in **Remote Background > Terminal** for shell options.

Right-click the connect button in **Take Control** for connection options.

#### Enable Remote Control Options

> **Note:** These settings are independent of Tactical RMM. Enable features (like auto remove inactive devices) with caution.

If you need to comply with GDPR regulations and ensure employee rights legislation is complied with, you can make sure that users receive a popup to inform them so they are aware when your techs log in and connect to their machine. You can enable a banner that shows when a remote connection is established.

1. Login to meshcentral as the mesh superuser. (Incognito window > Type mesh URL > Login as the superuser creds you got at end of server install). See the MeshCentral integration section in references/architecture.md for details on getting the superuser URL. It should have 5 icons on the left.
2. Click on My Account
3. Click on the device group you want to enable notifications or accept connection etc on (probably TacticalRMM).
4. Next to User Consent click edit (the pencil icon).
5. You can also change features by ticking whatever boxes you want in there (Features: Sync server device name to hostname, Automatically remove inactive devices, Notify/Prompt for Consent/Connection Toolbar settings).
6. Ok your way out

#### Agent Online / Offline logs

In mesh from the agent | General Tab you can view online/offline logs.

#### Sending Custom Keystrokes to Agent

Some of the native hotkeys will not send thru the MeshCentral remote control window (like Alt+Tab). You can right-click the special key list in the bottom left of the Remote Control window.

And add new ones like:

* Alt+Shift+Tab: Task switching between windows
* Win+Tab: Bring up thumbnail based running program switcher

#### Syncing PC name to MeshCentral

If you install TRMM agent, it will add the PC to meshcentral with the current computer name. If you later rename the computer, MeshCentral will not update that PC name by default unless you enable the sync name option in MeshCentral.

### Scripts

#### When Running Scripts

When running scripts (see the scripting section in references/scripting-and-variables.md for script arguments) use the (i) at the end of the script name to:

- Hover: see script parameter syntax help
- Left Click: Opens the script source in Github

### 3rd Party Software Patching

Chocolatey is the default 3rd party software library that is used to populate the software tab. You can install anything that is available at chocolatey.org

It is installed by default during the TRMM agent installation into the default choco install folder (`C:\ProgramData\chocolatey`). If there is an existing choco install or other problem you can delete that folder and fully reinstall by it running the standard choco install script which can be found here: <https://chocolatey.org/install.ps1>

If you're interested in converting your software to Chocolatey managed you will need to look at customizing the `Win_Choco_ConvertToChocoManaged.ps1` script from the community-scripts repository. If you have improvements please contribute.

Once you've made your script, that will take existing software and convert it to Chocolatey managed (see what Chocolatey manages on an agent with):

```batch
choco list
```

Next, you're going to schedule your updates.

Because of community repo limits, you can purchase chocolatey, host your own chocolatey server, or use the `Win_Chocolatey_Manage_Apps_Bulk.ps1` script sparingly using `-Mode upgrade -Hosts x` where x is the max number of machines on an internet connection.

### Run Intervals for Checks

You can modify at several locations / levels:

* **Settings Menu > Automation Manager > Checks tab >** Edit check
* Agent Level: **Edit Agent > Run checks every**
* Edit Check under agent > Run this check every (seconds)

> **Note:** The interval under check will override agent check if set.

See the checks section in references/checks-tasks-policies.md for full details on automated checks.

### Understanding refreshing TRMM data

How to get updated data and see agents last communication time: The main screen shows agent status with last check-in times, and data can be refreshed from the UI.

### Why are usernames in italics?

It's the last logged in user, when italicized it means nobody is currently logged in.

### Getting false SMS and Email alerts from scripts?

Return code `98` is reserved and used by Tactical RMM when a script execution times out. In most cases, a timeout can be interpreted as a transient or non-critical issue, rather than a true failure.

If you commonly experience script timeouts and want to prevent false-positive alerts, consider adding `98` to the list of success return codes.

You can also increase the consecutive failures to 2+.

See the alerting section in references/alerting-and-notifications.md for alert configuration details.

---

## BitDefender GravityZone Deployment

### How to Deploy BitDefender GravityZone

From the UI go to **Settings > Global Settings > CUSTOM FIELDS > Clients**.

Add a Custom Field:

First:
**Target** = `CLIENTS`
**Name** = `bdurl`
**Field Type** = `Text`

See the custom fields section in references/scripting-and-variables.md for general custom field configuration.

Log into your GravityZone and on the left hand side, select **Network > Packages**.

Select the client you are working with and click "Send Download Links" at the top.

Copy the appropriate download link.

Paste download link into the `bdurl` when you right click your target clients name in the RMM.

Right-click the Agent you want to deploy to and **Run Script**. Select **BitDefender GravityZone Install** and set timeout for 1800 seconds.

**Install time will vary based on internet speed and other AV removal by BitDefender BEST deployment**

### How to onboard a new company

Use these procedures to onboard a new company in Bitdefender.

1. Go to Companies > Add Company and fill out the details. The company type is "Customer".
2. Fill out the next tab for the authentication.
3. Fill out the last tab for the licensing. You probably want to use Monthly Subscription so that it's added to your monthly MSP subscription.
4. Next go to Network > Packages > Add to add a new package download for the company. Each company should have a separate download.
5. Select the company > Send download links. The Windows link is needed for the TRMM script to install Bitdefender. The Linux and Mac installer links are also provided but the script is for Windows only.

### Alert types

There are two general types of alerts: email and dashboard. While you may get both types of alerts for an incident, they are not the same and configuring the exclusions are not the same. This section explains both types and how to add the exclusions for each.

#### Process alert

- Bitdefender docs: [notification settings](https://www.bitdefender.com/business/support/en/77209-94325-configuring-notifications-settings.html)

This is a process alert that is emailed and as the name suggests, it kills the process. If the parent process is `C:\Windows\System32\services.exe`, the process is a service that just died. The detection type, ATC/IDS, indicates the exclusion will need to include the ATC/IDS module.

**Detected Exploit**
A harmful process has been detected by Behavior Scan on the following endpoint in your network:

| Detected Exploit Details |                                                       |
|--------------------------|-------------------------------------------------------|
| Company:                 | ACME Company, Inc.                                    |
| Computer Name:           | PC-Desktop01                                          |
| Computer IP:             | 192.168.1.69                                          |
| Installed Agent:         | Bitdefender Endpoint Security Tools                   |
| Command Line:            | C:\Program Files\TacticalAgent\tacticalrmm.exe -m svc |
| Parent Process Path:     | C:\Windows\System32\services.exe                      |
| Parent PID:              | 852                                                   |
| Exploit Type:            | ATC Application                                       |
| Exploit Path:            | C:\Program Files\TacticalAgent\tacticalrmm.exe        |
| Exploit Status:          | ATC/IDS Disinfected                                   |
| Last Blocked:            | 08 December 2022 08:55:59                             |
| Logged User:             | SYSTEM                                                |

Process notifications are configured in Notifications > Settings > ATC/IDS event.

#### Quarantine alert

- Bitdefender docs: [quarantine](https://www.bitdefender.com/business/support/en/77209-89887-quarantine.html)

When a file is detected, it is quarantined by moving it to an encrypted folder on the endpoint. Email notifications cannot be configured for quarantined files, although they are available via the [API](https://www.bitdefender.com/business/support/en/77209-140256-getquarantineitemslist.html). The threat name, Atc4.Detection, indicates the exclusion needs to include the ATC/IDS module.

### Troubleshooting and problem resolution

#### MeshAgent.exe quarantine corrupts Mesh Agent service

When Bitdefender quarantines MeshAgent.exe, the service is corrupted. Here is what the service looks like before the quarantine.

```text
[PC-Desktop3]: PS C:\> Get-CimInstance Win32_Service -Filter 'Name = "Mesh Agent"' | Format-List *


Name                    : Mesh Agent
Status                  : OK
ExitCode                : 0
DesktopInteract         : True
ErrorControl            : Ignore
PathName                : "C:\Program Files\Mesh Agent\MeshAgent.exe"
ServiceType             : Own Process
StartMode               : Auto
Caption                 : Mesh Agent
Description             : Mesh Agent background service
InstallDate             :
CreationClassName       : Win32_Service
Started                 : True
SystemCreationClassName : Win32_ComputerSystem
SystemName              : PC-Desktop3
AcceptPause             : False
AcceptStop              : True
DisplayName             : Mesh Agent
ServiceSpecificExitCode : 0
StartName               : LocalSystem
State                   : Running
TagId                   : 0
CheckPoint              : 0
DelayedAutoStart        : False
ProcessId               : 7612
WaitHint                : 0
PSComputerName          :
CimClass                : root/cimv2:Win32_Service
CimInstanceProperties   : {Caption, Description, InstallDate, Name...}
CimSystemProperties     : Microsoft.Management.Infrastructure.CimSystemProperties
```

This is what the service looks like after `MeshAgent.exe` is quarantined. Notice the `PathName`, `ServiceType`, `StartMode` are "Unknown", and some properties are blank.

```text
[PC-Desktop3]: PS C:\> Get-CimInstance Win32_Service -Filter 'Name = "Mesh Agent"' | Format-List *


Name                    : Mesh Agent
Status                  : OK
ExitCode                : 1067
DesktopInteract         :
ErrorControl            : Unknown
PathName                :
ServiceType             : Unknown
StartMode               : Unknown
Caption                 : Mesh Agent
Description             :
InstallDate             :
CreationClassName       : Win32_Service
Started                 : False
SystemCreationClassName : Win32_ComputerSystem
SystemName              : PC-Desktop3
AcceptPause             : False
AcceptStop              : False
DisplayName             : Mesh Agent
ServiceSpecificExitCode : 0
StartName               :
State                   : Stopped
TagId                   :
CheckPoint              : 0
DelayedAutoStart        :
ProcessId               : 0
WaitHint                : 0
PSComputerName          :
CimClass                : root/cimv2:Win32_Service
CimInstanceProperties   : {Caption, Description, InstallDate, Name...}
CimSystemProperties     : Microsoft.Management.Infrastructure.CimSystemProperties
```

Restoring `MeshAgent.exe` from quarantine will make it "look" normal but will not have any permissions. Renaming, deleting or moving the file results in a permission denied error. After a reboot, the `MeshAgent.exe` will be missing.

```text
[PC-Desktop3]: PS C:\Program Files\Mesh Agent> Rename-Item -Path .\MeshAgent.exe -NewName .\MeshAgent-Restored.exe
Rename-Item : Access to the path is denied.
    + CategoryInfo          : PermissionDenied: (C:\Program File...t\MeshAgent.exe:String) [Rename-Item], Unauthorized
   AccessException
    + FullyQualifiedErrorId : RenameItemUnauthorizedAccessError,Microsoft.PowerShell.Commands.RenameItemCommand
```

The best path for recovery is to leave the file in quarantine and run the [Win_TRMM_Mesh_Install.ps1](https://github.com/amidaware/community-scripts/blob/main/scripts/Win_TRMM_Mesh_Install.ps1) script to have Tactical RMM install the Mesh Agent. The existing config will be used and there will _not_ be duplicates.

---

## Zammad Integration

### Zammad Setup

1. **Install Zammad:**
   Follow the installation instructions provided in the [Zammad documentation](https://docs.zammad.org/en/latest/).

2. **Generate API Token:**
   - Click on your User Initials in Zammad.
   - Navigate to Profile > Token Access.
   - Click "Create".
   - Name the Token "Tactical RMM" and select "Ticket Agent".
   - Click "Create" to generate the token.

3. **Add Customers and Emails:**
   Ensure each customer in Zammad has a corresponding email associated.

### Tactical RMM Setup for Zammad

1. **Add Custom Field in Sites:**
   - Add a custom field under Sites called `Zammad-Email`
   - Populate this field with the corresponding email addresses from Zammad to match up with customers.
   - See the custom fields section in references/scripting-and-variables.md for details on creating custom fields.

2. **Add Webhook:**

   - **URL Pattern:** `https://your_zammad_domain.com/api/v1/tickets`
   - **Method:** POST
   - See the webhooks section in references/alerting-and-notifications.md for details on configuring webhooks.

3. **Request Headers:**

   ```json
   {
       "Content-Type": "application/json",
       "Authorization": "Bearer your_generated_token_here"
   }
   ```

   Replace your_generated_token_here with the actual API token generated from Zammad.

4. **Request Body:**

```json
{
    "title": "{{ alert.severity }} on {{ agent.hostname }}",
    "group": "Users",
    "customer": "{{ client.Zammad-Email }}",
    "article": {
        "subject": "{{ alert.severity }} on {{ agent.hostname }}",
        "body": "Client: {{agent.site.client.name}}, Site: {{agent.site.name}}: {{ alert.message }} at {{ alert.alert_time }}",
        "type": "note",
        "internal": false
    }
}
```

- `{{ alert.severity }}`, `{{ agent.hostname }}`, `{{ alert.message }}`, and `{{ alert.alert_time }}` are placeholders that will be replaced with actual data from Tactical RMM alerts.
- `{{ client.Zammad-Email }}` refers to the custom field you added under Sites where you store the corresponding Zammad email for each customer.

5. **Add Webhook to Alert Policy**:

   - Assign the webhook to the appropriate Alert Policy that is assigned to customers in Tactical RMM.
   - See the alerting section in references/alerting-and-notifications.md for details on alert policies.

### Notes

- Ensure that the API token in the Authorization header (Bearer your_generated_token_here) has the necessary permissions (e.g., ticket.agent) to create tickets in Zammad.
- Adjust the title, group, customer, article fields in the request body as per your specific requirements and Zammad's API capabilities.
- Test the integration thoroughly to ensure that alerts from Tactical RMM are correctly creating tickets in Zammad with the expected data.

---

## Getting Started Guide

Install the server - see the install considerations section in references/architecture.md to choose the best path.

### Post Install

- Setup Email Alerts (see the email/SMS setup section in references/alerting-and-notifications.md)
- Setup SMS Alerts
- Create a Default Alert Template and assign (either Global, or using Automation Policies)
- Set Server Preferences Under `Global Settings > General`
- Review User Settings (see the Customize User Interface section above)
- Set Retention Policies under `Global Settings > Retention`
- Read thru the FAQ (see the FAQ section above)
- Setup AV exclusions in the appropriate Anti-virus products for your managed base

### Setup Automation Policies

- Default Profile for workstations `Settings menu > Global Settings > General`
- Default Profile for servers `Settings menu > Global Settings > General`
- Decide on Windows Updates policy (see the Windows update management section in references/architecture.md)
- Create Onboarding Tasks and apply according to how you want to manage them (see the automated tasks section in references/checks-tasks-policies.md)

### Multiple Users

- Setup Permission Manager `Settings menu > Permission Manager` (see the permissions section in references/settings-and-admin.md)
- Add users to Permission Groups `Settings menu > User Administration`

### Every 75 days

- TRMM Server OS updates
- Reboot TRMM server
- Renew LetsEncrypt Certs
- Update TRMM
- Check your backups. Especially scheduled ones and make sure you're running the latest `./backup.sh` (You're reading the release notes at every update, right?)

### Bi-annually

- Clean up old agents (see the management commands section in references/settings-and-admin.md for bulk delete agents)

### Don't do these things

Your Tactical NoNo List:

- Clone agents with TRMM agent installed. Make your master image with no TRMM agent installed, script the install for first time boot after imaging.
- Do in place distro upgrades or move vms to new hardware, instead use Backup and Restore scripts to move the server to new vm's
- Run `install.sh` or `restore.sh` more than once. They're one-shot scripts to be ran on clean VMs only.
- Use TRMMs powers for Evil. Just don't, make better choices!

---

## Examples: Serial Number URL Actions

### Create Run URL Action to Computer support page

This will create a URL link that will take you to the support page for a computer based on the computers Serial Number.

1. Goto `Settings | Global Settings | Custom Fields`

    Under Agents tab Add Custom Field (CaSe SeNsItIve)

    See the custom fields section in references/scripting-and-variables.md for details.

2. Create Task (best to use `Settings | Automation Manager` if you want to apply it to all computers). Add script that has an output of the data you want.

    See the automated tasks section in references/checks-tasks-policies.md for creating collector tasks.

3. Create URL Action (under `Settings | Global Settings | URL ACTIONS`) for Manufacturer websites

    See the URL actions section in references/settings-and-admin.md for URL action configuration.

**Dell Support Page:**

```
https://www.dell.com/support/home/en-us/product-support/servicetag/{{agent.SerialNumber}}/overview
```

**Lenovo Support Page:**

```
https://pcsupport.lenovo.com/us/en/products/{{agent.SerialNumber}}
```

**HP Support Page:**

It gives an error because the product model doesn't match the serial number. If you figure out a better link please let us know!

```
https://support.hp.com/us-en/product/hp-pro-3500-microtower-pc/5270849/model/5270850?serialnumber={{agent.SerialNumber}}
```

### Setup LAPS - Local Administrator Password Solution

Optional: Create a Global Key to have a custom admin username. See the global key store section in references/scripting-and-variables.md for details.

Create a custom field for storing the password. See the custom fields section in references/scripting-and-variables.md.

Create Task (can use Automation Policy). See the automation policies section in references/checks-tasks-policies.md.

Run however often you'd like admin password reset.

When you need the LAPS password, get from Agent Custom Fields.

---

## BitLocker Recovery Key

It would be useful to add the Windows BitLocker recovery key to the machine summary or in the hard drive section.

### Solution: Use a Collector Task

Use this script as a task on your machines, make it a collector task and store the keys against an Agent custom field. See the custom fields section in references/scripting-and-variables.md for setting up custom fields, and the automated tasks section in references/checks-tasks-policies.md for creating collector tasks.

```powershell
$Volumes = Get-BitLockerVolume

foreach ($vol in $volumes) {
    $volstatus += ($vol.Mountpoint + " " + $vol.ProtectionStatus + " " + $vol.VolumeStatus)
    [string] $volkey += (Get-BitLockerVolume -MountPoint $vol.Mountpoint).KeyProtector.recoverypassword

}
$volstatus += $volkey
write-output $volstatus
```

---

## SNMP Checks

*Version added: Tactical RMM v0.19.0 / Agent v2.8.0*

SNMP monitoring can now be done using the `pysnmplib` library included with the portable python distribution on Windows agents. See the scripting section in references/scripting-and-variables.md for details on the Python on Windows distribution.

Here is a sample script that can be used to query and monitor a printer. It takes the printer's IP address as the first argument.

```python
#!/usr/bin/python3

import sys
from pysnmp.hlapi import *

if len(sys.argv) != 2:
    print("Missing required argument: snmp device IP address")
    sys.exit(1)

printer_ip = sys.argv[1]
community_string = 'public'

oids = {
    'Printer Model': '1.3.6.1.2.1.1.1.0',
    'Total Page Count': '1.3.6.1.2.1.43.10.2.1.4.1.1',
    'Toner Level Black': '1.3.6.1.2.1.43.11.1.1.9.1.1',
    'Toner Level Cyan': '1.3.6.1.2.1.43.11.1.1.9.1.2',
    'Toner Level Magenta': '1.3.6.1.2.1.43.11.1.1.9.1.3',
    'Toner Level Yellow': '1.3.6.1.2.1.43.11.1.1.9.1.4',
    'Device Status': '1.3.6.1.2.1.25.3.2.1.5.1',
    'Serial Number': '1.3.6.1.2.1.43.5.1.1.17.1',
}

for name, oid in oids.items():
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community_string, mpModel=0),
        UdpTransportTarget((printer_ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f'Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1] or "?"}')
    else:
        for varBind in varBinds:
            print(f'{name}: {varBind[1]}')
```

---

## Remote Background

To access: **Right click** on an agent > **Remote Background**

### Terminal Tab

Meshcentral Integration: This will allow you to open a terminal on the remote agent.

Right-clicking will allow:

- Admin Shell
- Admin PowerShell
- User Shell
- User PowerShell
- Ask Admin Shell
- Ask Admin PowerShell
- Ask User Shell
- Ask User PowerShell

> **Tip:** If you don't see any Connect button in the top left the problem is either the TRMM user doesn't have meshcentral permissions or the mesh agent is having connectivity problems. Try either the "Recover Connection" button or script "TacticalRMM - Check Mesh Agent for problems"

### File Browser

Meshcentral Integration: This will allow you to open a File Manager where you can manage and transfer files to and from the agent.

### Services Tab

Right click on a service to show the context menu where you can start/stop/restart services.

Click *Service Details* to bring up the details tab where you can edit more service options.

### Processes Tab

A very basic task manager that shows real time process usage.

**Right click** on a process to end the task.

### Event Log

Allows you to query the Windows Application | System | Security Logs.

---

## Roadmap

### Next Release

- **White Labeling** (GitHub issue #463) - Comprehensive white labeling solution allowing full customization of branding and UI elements.

### Future Releases

- **Windows Update Rework** (GitHub issue #1188) - Complete overhaul of the Windows Update management system for better reliability and performance.
- **Tagging/Groups** (GitHub issue #653)
- **Bulk Edit Agents** (GitHub issue #1149)
- **Customizable columns in the agent list** (GitHub issue #308)
- **Internationalization support** (GitHub issue #39)
