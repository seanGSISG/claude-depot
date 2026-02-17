# Scripting, Variables, Custom Fields, and Keystore

> Sources: functions/scripting.md, script_variables.md, functions/custom_fields.md, functions/keystore.md

## Table of Contents

- [Scripting](#scripting)
  - [Adding Scripts](#adding-scripts)
  - [Downloading Scripts](#downloading-scripts)
  - [Community Scripts](#community-scripts)
  - [Using Scripts](#using-scripts)
  - [Using Dashboard Data in Scripts](#using-dashboard-data-in-scripts)
  - [Script Snippets](#script-snippets)
  - [PowerShell 7](#powershell-7)
  - [Python](#python)
  - [Nushell](#nushell)
  - [Deno](#deno)
  - [Example Scripts](#example-scripts)
- [Script Variables](#script-variables)
  - [Agent Variables](#agent)
  - [Client Variables](#client)
  - [Site Variables](#site)
  - [Alert Variables](#alert)
  - [Custom Fields as Variables](#custom-fields-as-variables)
- [Custom Fields](#custom-fields)
  - [Adding Custom Fields](#adding-custom-fields)
  - [Using Custom Fields in the Dashboard](#using-custom-fields-in-the-dashboard)
  - [Using Custom Fields in Scripts](#using-custom-fields-in-scripts)
  - [Populating Custom Fields Automatically](#populating-custom-fields-automatically)
- [Global Key Store](#global-key-store)

---

## Scripting

Tactical RMM supports uploading existing scripts or creating new scripts from within the web interface.

Windows agent languages supported:

- PowerShell
- Windows Batch
- Python
- [Nushell](https://www.nushell.sh/)
- [Deno](https://deno.com/)

There is RunAsUser functionality for Windows. See the architecture overview in references/architecture.md for details.

Linux/Mac languages supported:

- Any language that is installed on the remote machine (use a shebang at the top of the script to set the interpreter)
- nu
- deno (Javascript and TypeScript)

### Adding Scripts

In the dashboard, browse to **Settings > Scripts Manager**. Click the **New** button and select either Upload Script or New Script. The available options for scripts are:

- **Name** - This identifies the script in the dashboard.
- **Description** - Optional description for the script.
- **Category** - Optional way to group similar scripts together.
- **Type** - This sets the language of the script. Available options are:
    - PowerShell
    - Windows Batch
    - Python
    - Shell (use for Linux/macOS scripts)
    - Nushell
    - Deno

- **Script Arguments** - Optional way to set default arguments for scripts. These will auto populate when running scripts and can be changed at runtime. Logged on Windows Event Viewer > Applications and Services Logs > Microsoft > Windows> PowerShell > Operational
- **Environment vars** - Optional way to set default arguments for scripts using Environment Variables. These will auto populate when running scripts and can be changed at runtime. Not logged, better to use when passing data you don't want logged
- **Default Timeout** - Sets the default timeout of the script and will stop script execution if the duration surpasses the configured timeout. Can be changed at script runtime.
- **Favorite** - Favorites the script.

### Downloading Scripts

To download a Tactical RMM Script, click on the script in the Script Manager to select it. Then click the **Download Script** button on the top. You can also right-click on the script and select download.

### Community Scripts

These are script that are built into Tactical RMM. They are provided and maintained by the [Tactical RMM community](https://github.com/amidaware/community-scripts). These scripts are updated whenever Tactical RMM is updated and can't be modified or deleted in the dashboard.

#### Hiding Community Scripts

You can choose to hide community script throughout the dashboard by opening **Script Manager** and clicking the **Show/Hide Community Scripts** toggle button.

### Using Scripts

#### Manual run on agent

In the **Agent Table**, you can right-click on an agent and select **Run Script**. You have the options of:

- **Wait for Output** - Runs the script and waits for the script to finish running and displays the output.
- **Fire and Forget** - Starts the script and does not wait for output.
- **Email Output** - Starts the script and will email the output. Allows for using the default email address in the global settings or adding a new email address.
- **Save as Note** - Saves the output as a Note that can be views in the agent Notes tab.
- **Collector** - Saves to output to the specified custom field.

There is also an option on the agent context menu called **Run Favorited Script**. This will pre-populate the script run dialog with the script of your choice.

For details on the script execution process, see the Windows Agent section in references/architecture.md.

#### Script Arguments

The `Script Arguments` field should be pre-filled with information for any script that can accept or requires parameters. See references/integrations-and-tips.md for tips on using scripts.

Where `[]` indicates an optional parameter

and `{}` indicates a parameter with several preconfigured parameter

and `()` indicates a default parameter if none is specified.

Starting with 0.15.4 you can use environment variables to pass them too!

##### Examples

Script Arguments

```
-hello world
-foo bar
-data {{agent.public_ip}}
```

Environment vars

```
ehello=eworld
efoo=ebar
edata={{agent.hostname}}
```

=== ":material-language-python: Batch"

    Script

    ```batch
    @echo off
    setlocal

    rem Parameters. Batch only accepts positional params not named ones
    set hello=%1
    set foo=%2
    set data=%3

    echo Script Args
    echo hello: %hello%
    echo foo: %foo%
    echo data: %data%

    echo.
    echo Environment Vars
    echo ehello: %ehello%
    echo efoo: %efoo%
    echo edata: %edata%

    endlocal
    ```

=== ":material-powershell: Powershell"

    Script

    ```ps
    param(
        [string]$hello,
        [string]$foo,
        [string]$data
    )

    Write-Output "Script Args"
    Write-Output "hello: $hello"
    Write-Output "foo: $foo"
    Write-Output "data: $data"

    Write-Output ""
    Write-Output "Environment Vars"
    Write-Output "ehello: $env:ehello"
    Write-Output "efoo: $env:efoo"
    Write-Output "edata: $env:edata"
    ```

=== ":material-language-python: Python"

    Script

    ```python
    #!/usr/bin/python3

    import os
    import argparse

    #Note: named args in python require -- and = between name and value eg
    # --hello=world
    # --foo=bar
    # --data={{agent.public_ip}}
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process some strings.")
    parser.add_argument("--hello", type=str, help="Value for hello")
    parser.add_argument("--foo", type=str, help="Value for foo")
    parser.add_argument("--data", type=str, help="Value for data")

    args = parser.parse_args()

    # Script Args
    print("Script Args")
    print(f"hello: {args.hello}")
    print(f"foo: {args.foo}")
    print(f"data: {args.data}")

    # Environment Vars
    print("\nEnvironment Vars")
    print(f"ehello: {os.getenv('ehello')}")
    print(f"efoo: {os.getenv('efoo')}")
    print(f"edata: {os.getenv('edata')}")
    ```

=== ":material-bash: Shell"

    Script

    ```bash
    #!/bin/bash

    #Bash only accepts positional params not named ones
    hello="$1"
    foo="$2"
    data="$3"

    echo "Script Args"
    echo "hello: $hello"
    echo "foo: $foo"
    echo "data: $data"

    echo ""
    echo "Environment Vars"
    echo "ehello: $ehello"
    echo "efoo: $efoo"
    echo "edata: $edata"
    ```

#### Run Script on many agents at once

Under the `Tools menu` -> `Bulk Script` you can execute scripts against Clients/Sites/Selected Agents/All based on All/Servers/Workstations. The history is saved in the history tab of the agent. The history can also be retrieved from the API from the `/agents/history/` endpoint.

#### Run Command on many agents at once

Under the `Tools menu` -> `Bulk Command` you can execute a command against Clients/Sites/Selected Agents/All based on All/Servers/Workstations. The history is saved in the history tab of the agent. The history can also be retrieved from the API from the `/agents/history/` endpoint.

#### Automated Tasks

Tactical RMM allows scheduling tasks to run on agents. This leverages the Windows Task Scheduler and has the same scheduling options.

See references/checks-tasks-policies.md for configuring automated tasks.

#### Script Checks

Scripts can also be run periodically on an agent and trigger an alert if it fails in case you want any kind of warning code to alert you.

Important: When utilizing PowerShell scripts and manually assigning an exit code, it's essential to define the exit code using the following syntax: `$host.SetShouldExit(EXITCODE)`. Here, EXITCODE represents the desired exit code number. For instance, to assign an exit code of 3, use `$host.SetShouldExit(3)`.

#### Alert Failure/Resolve Actions

Scripts can be triggered when an alert is triggered and resolved.

For configuring Alert Templates, see references/alerting-and-notifications.md.

See below for populating dashboard data in scripts and the available options.

### Using Dashboard Data in Scripts

Tactical RMM allows passing in dashboard data to scripts as arguments or environment variables. The below PowerShell arguments will get the client name of the agent and also the agent's public IP address.

```
-ClientName {{client.name}} -PublicIP {{agent.public_ip}}
```

!!!info
    Everything between {{}} is CaSe sEnSiTive

See the [Script Variables](#script-variables) section below for a full list of possible built-in variables.

#### Getting Custom Field values

Tactical RMM supports pulling data from custom fields using the {{model.custom_field_name}} syntax.

See the [Using Custom Fields in Scripts](#using-custom-fields-in-scripts) section below.

#### Getting values from the Global Keystore

Tactical RMM supports getting values from the global key store using the {{global.key_name}} syntax.

See the [Global Key Store](#global-key-store) section below.

### Script Snippets

Script Snippets allow you to create common code blocks or comments and apply them to all of your scripts. This could be initialization code, common error checking, or even code comments.

#### Adding Script Snippets

In the dashboard, browse to **Settings > Scripts Manager**. Click the **Script Snippets** button.

- **Name** - This identifies the script snippet in the dashboard
- **Description** - Optional description for the script snippet
- **Shell** - This sets the language of the script. Available options are:
    - PowerShell
    - Windows Batch
    - Python

#### Using Script Snippets

When editing a script, you can add template tags to the script body that contains the script snippet name. For example, if a script snippet exists with the name "Check WMF", you would put {{Check WMF}} in the script body and the snippet code will be replaced.

!!!info
    Everything between {{}} is CaSe sEnSiTive

The template tags will only be visible when Editing the script. When downloading or viewing the script code the template tags will be replaced with the script snippet code.

### PowerShell 7

<https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process?view=powershell-7.2>

Shell Type: PowerShell

Command: `Start-Process nohup 'pwsh -noprofile -c "1..120 | % { Write-Host . -NoNewline; sleep 1 }"'`

### Python

#### Python on Windows

Tactical ships with a portable python distribution on windows.

| OS | Version |
| --- | --- |
| Windows >= 8.1 | 3.11.9 |
| Windows < 8.1 | 3.8.7 |

The following 3rd party packages are also bundled with this distribution:

- [cryptography](https://github.com/pyca/cryptography)
- [httpx](https://github.com/encode/httpx)
- [msgpack](https://github.com/msgpack/msgpack-python)
- [psutil](https://github.com/giampaolo/psutil)
- [pysnmplib](https://github.com/pysnmp/pysnmp)
- [pywin32](https://github.com/mhammond/pywin32)
- [pywin32-ctypes](https://github.com/enthought/pywin32-ctypes)
- [requests](https://github.com/psf/requests)
- [websockets](https://github.com/python-websockets/websockets)
- [WMI](https://timgolden.me.uk/python/wmi/index.html)
- [validators](https://github.com/python-validators/validators)

#### Python on POSIX

How do you target a specific version? The shebang can specify the interpreter on macOS and Linux, but since Windows does not use the shebang, the interpreter needs to be specified by the calling program.

Ok, so how do you use the shebang? Take this hello world script for example. The shebang `#!` in this script will use `/usr/bin/python3`. This is easy enough until you run across a system where the system Python is not the expected 3.8 or later.

```bash
#!/usr/bin/python3
print("Hello World!")
```

This is where `env` comes into play. `env` will search the `$PATH` for the executable that matches the argument. In this case, the script will be run by the first "python3" found in $PATH. However, what if `python3` points to `python3.6`? You're in the same boat you were in before.

```bash
#!/usr/bin/env python3
print("Hello World!")
```

Or are you? If you read the env man page, it states you can add parameters to the command line. In case you didn't know, the shebang is the command line! `env` will modify the `$PATH` before searching for `python3`, allowing you to use a custom python location.

```bash
#!/usr/bin/env PATH="/opt/my-python/3.8/:$PATH" python3
print("Hello World!")
```

Wait! Isn't the shebang a shell script, not a Python script? In TRMM, a "Shell" script and a "Python" script are treated the same _except_ that Python scripts also work on Windows. On Linux and macOS, "Shell" and "Python" scripts are treated the same.

| Script Type | OS      | Supported |
| ----------- | ------- | --------- |
| Python      | Windows | Yes       |
| Python      | Linux   | Yes       |
| Python      | macOS   | Yes       |
| Shell       | Windows | **No**    |
| Shell       | Linux   | Yes       |
| Shell       | macOS   | Yes       |

#### Python version references

- Python 2 was sunset in January 2020.
- Python 3.7 is end of life in June 2023.

| OS                                      | Python version               | Installed by TRMM |
| --------------------------------------- | ---------------------------- | ----------------- |
| Windows                                 | 3.11                         | Yes               |
| Linux, Debian 10 (Buster) (end of life) | 3.7                          | No                |
| Linux, Debian 11 (Bullseye)             | 3.9                          | No                |
| Linux, Debian 12 (Bookworm)             | 3.12                         | No                |
| Linux, Ubuntu 20.04 LTS                 | 3.8                          | No                |
| Linux, Ubuntu 22.04 LTS                 | 3.10                         | No                |
| macOS Ventura                           | 3.8                          | No                |
| macOS Monterey 12.3                     | 2.7 removed                  | No                |
| macOS Catalina 10.15                    | 2.7 (not recommended to use) | No                |

#### Targeting a specific version

Python compiles the script into bytecode and then executes it. Because of the compilation step, errors due to language constructs introduced in a later version of Python will cause the script to fail. For example, Python 3.10 introduced the "match" term as their version of a case or switch statement.

```Python
#!/usr/bin/env python3

match "term":
    case "Nope":
        print("No match found")
    case "term":
        print("Found match!")
    case _:
        print("Default if nothing matches")
```

The same code will work on Python 3.10.

```bash
$ python3.10 test-python-version.py
Found match!
```

The same code fails on versions prior to 3.10.

```bash
$ python3.6 test-python-version.py
  File "test-python-version.py", line 3
    match "term":
               ^
SyntaxError: invalid syntax
```

### Nushell

Nu is a new type of shell. Like PowerShell, Nu passes objects from one command to the next. For example, this script will list processes that are more than 100MB.

```nu
ps | where mem >= 100MB
```

There are some important points to keep in mind when writing Nu scripts. See the [Thinking in Nu](https://www.nushell.sh/book/thinking_in_nu.html) for details. Some highlights:

1. The `>` is the greater-than operator, not redirection. Use `| save some-file.txt`
2. Variables are immutable, or constant. Use [`mut`](https://www.nushell.sh/commands/docs/mut.html#frontmatter-title-for-core) to make a variable mutable.
3. Currently Nu does not support background tasks. `long-running-command &` will not work.

Nu has a [Discord](https://discord.gg/NtAbbGn) server if you have questions.

To disable this feature, add the following to `local_settings.py`:

```python
INSTALL_NUSHELL = False
```

#### Example Nushell Script

The below script find processes sorted by greatest cpu utilization.

```nu
ps | sort-by cpu | reverse
```

### Deno

Deno is considered to be the next iteration of Node.js. Deno uses ECMAScript modules (a.k.a ES Modules or ESM) syntax, not CommonJS (CJS). I.e. use `import * from https://example.com/package/module.ts` instead of `require('./local/file.js')`.

Tactical RMM runs Deno scripts with the following permissions:

```
DENO_PERMISSIONS=--allow-all
```

See the [documentation on permissions](https://docs.deno.com/runtime/manual/basics/permissions) for details.

To override this, either:

1. Add the `DENO_DEFAULT_PERMISSIONS` string variable with the permissions requested to `local_settings.py`
or
2. Set the `DENO_PERMISSIONS` environment variable to the permissions requested in your script.

To disable this feature, add the following to `local_settings.py`:

```python
INSTALL_DENO = False
```

#### Example Deno Script

The below script prints basic system information:

```typescript
async function gatherSystemInfo() {
  const os = Deno.build.os;
  const arch = Deno.build.arch;
  const memory = Deno.systemMemoryInfo();


  const info = `
OS: ${os}
Architecture: ${arch}
Total Memory: ${(await memory).total / 1024 / 1024} MB
Free Memory: ${(await memory).free / 1024 / 1024} MB
`;

  console.log(info);
}

gatherSystemInfo().catch(console.error);
```

### Example Scripts

#### Example PowerShell Script

The below script takes five named values. The arguments will look like this: `-SiteName {{site.name}}` `-ClientName {{client.name}}` `-PublicIP {{agent.public_ip}}` `-CustomField {{client.AV_KEY}}` `-Global {{global.API_KEY}}`

```powershell
param (
   [string] $SiteName,
   [string] $ClientName,
   [string] $PublicIp,
   [string] $CustomField,
   [string] $Global
)

Write-Output "Site: $SiteName"
Write-Output "Client: $ClientName"
Write-Output "Public IP: $PublicIp"
Write-Output "Custom Fields: $CustomField"
Write-Output "Global: $Global"
```

#### Example Shell Script

The below script prints the user running the script.

```bash
#!/usr/bin/env bash
whoami
```

---

## Script Variables

Tactical RMM allows passing dashboard data into script as arguments or environment variables. This uses the syntax `{{model.field}}`.

!!!info
    Nested relations are followed so something like `{{agent.site.name}}` will work.

For a full list of available fields, refer to the variables in the `models.py` files:

!!!info
    @property functions under the model will work as well

- [Agent](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/agents/models.py#L60)
- [Client](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/clients/models.py#L18)
- [Site](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/clients/models.py#L93)
- [Alert](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/alerts/models.py#L29)
- [Check](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/checks/models.py#L30)
- [CheckResult](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/checks/models.py#L281)
- [AutomatedTask](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/autotasks/models.py#L51)
- [TaskResult](https://github.com/amidaware/tacticalrmm/blob/89aceda65a1c54fea7b18250ca63614f091eac6e/api/tacticalrmm/autotasks/models.py#L464)

Below are some examples of available fields:

!!!info
    Everything between {{}} is CaSe sEnSiTive

### Agent

- **{{agent.version}}** - Tactical RMM agent version.
- **{{agent.operating_system}}** - Agent operating system example: *Windows 10 Pro, 64 bit (build 19042.928)*.
- **{{agent.plat}}** - Will show the platform example: *windows*.
- **{{agent.hostname}}** - The hostname of the agent.
- **{{agent.local_ips}}** - Local IP address of agent.
- **{{agent.public_ip}}** - Public IP address of agent.
- **{{agent.agent_id}}** - agent ID in database.
- **{{agent.last_seen}}** - Date and Time Agent last seen.
- **{{agent.total_ram}}** - Total RAM on agent. Returns an integer - example: *16*.
- **{{agent.boot_time}}** - Uptime of agent. Returns unix timestamp. example: *1619439603.0*.
- **{{agent.logged_in_username}}** - Username of logged in user.
- **{{agent.last_logged_in_user}}** - Username of last logged in user.
- **{{agent.monitoring_type}}** - Returns a string of *workstation* or *server*.
- **{{agent.description}}** - Description of agent in dashboard.
- **{{agent.mesh_node_id}}** - The mesh node id used for linking the tactical agent to mesh.
- **{{agent.overdue_email_alert}}** - Returns true if overdue email alerts is enabled in TRMM.
- **{{agent.overdue_text_alert}}** - Returns true if overdue SMS alerts is enabled in TRMM.
- **{{agent.overdue_dashboard_alert}}** - Returns true if overdue agent alerts is enabled in TRMM.
- **{{agent.offline_time}}** - Returns offline time setting for agent in TRMM.
- **{{agent.overdue_time}}** - Returns overdue time setting for agent in TRMM.
- **{{agent.check_interval}}** - Returns check interval time setting for agent in TRMM.
- **{{agent.needs_reboot}}** - Returns true if reboot is pending on agent.
- **{{agent.choco_installed}}** - Returns true if Chocolatey is installed.
- **{{agent.patches_last_installed}}** - The date that patches were last installed by Tactical RMM.
- **{{agent.timezone}}** - Returns timezone configured on agent.
- **{{agent.maintenance_mode}}** - Returns true if agent is in maintenance mode.
- **{{agent.block_policy_inheritance}}** - Returns true if agent has block policy inheritance.
- **{{agent.alert_template}}** - Returns true if agent has block policy inheritance.
- **{{agent.site}}** - The site that the agent belongs too. Can be used for nesting. See Site above for properties

### Client

- **{{client.name}}** - Returns name of client.

### Site

- **{{site.name}}** - Returns name of Site.
- **{{site.client}}** - The client that the site belongs too. Can be used for nesting. See Client above for properties

### Alert

!!!info
    Only available in failure and resolve actions on alert templates!

- **{{alert.alert_time}}** - Time of the alert.
- **{{alert.message}}** - Alert message.
- **{{alert.severity}}** - Severity of the alert *info, warning, or error*.
- **{{alert.alert_type}}** - The type of alert. Will be *availability, check, task, or custom*.
- **{{alert.snoozed}}** - Returns true if the alert is snoozed.
- **{{alert.snoozed_until}}** - Returns the datetime that the alert is unsnoozed.
- **{{alert.email_sent}}** - Returns true if this alert has triggered a failure email.
- **{{alert.resolved_email_sent}}** - Returns true if this alert has triggered a resolved email.
- **{{alert.sms_sent}}** - Returns true if this alert has triggered a failure text.
- **{{alert.resolved_sms_sent}}** - Returns true if this alert has triggered a resolved text.
- **{{alert.hidden}}** - Returns true if this alert is hidden. It won't show in the alerts icon in the dashboard
- **{{alert.action_run}}** - Returns datetime that an alert failure action was run.
- **{{alert.action_stdout}}** - Returns standard output of the alert failure action results.
- **{{alert.action_stderr}}** - Returns error output of the alert failure action results.
- **{{alert.action_retcode}}** - Returns return code of the alert failure action.
- **{{alert.resolved_action_run}}** - Returns datetime that an alert resolved action was run.
- **{{alert.resolved_action_stdout}}** - Returns standard output of the alert resolved action results.
- **{{alert.resolved_action_stderr}}** - Returns error output of the alert resolved action results.
- **{{alert.resolved_action_retcode}}** - Returns return code of the alert resolved action.

- **{{alert.agent}}** - The agent that triggered the alert. Can be used for nesting. See Agent above for properties.
- **{{alert.assigned_check}}** - The check that triggered the alert. Can be used for nesting. See Check above for properties.
- **{{alert.assigned_check.readable_desc}}** - This will return the name that is used in the UI for the check.
- **{{alert.assigned_task}}** - The automated task that triggered the alert. Can be used for nesting. See Automated Task above for properties.
- **{{alert.assigned_task.name}}** - This will return the name that is used in the UI for the automated task.
- **{{alert.site}}** - The site associated with the agent that triggered the alert. Can be used for nesting. See Site above for properties.
- **{{alert.client}}** - The client associated with the agent that triggered the alert. Can be used for nesting. See Client above for properties.

- **{{alert.get_result}}** - Will return the results of the associated check or automated task. Can be used for nesting. See CheckResult or TaskResult above for properties. This will be blank for agent availability alerts. For example to get the standard output of the check that failed, do **``{{ alert.get_result.stdout }}``**

### Custom Fields as Variables

You can use custom fields as variables by referencing the object that contains the custom field and using the exact name of the field as the property. For example, {{agent.Custom field Name}}. This reference is case sensitive, and spaces in the field name are supported.

Currently, custom fields are supported only for the following objects: Client, Site, and Agent. If the custom field cannot be found, the text will be passed as-is to the script.

---

## Custom Fields

!!!warning
    `\` is an escape character, if you want to use that in a custom field you will need to use `\\` instead.

### Adding Custom Fields

In the dashboard, go to **Settings > Global Settings > Custom Fields** and click **Add Custom Field**.

!!!info
    Everything between {{}} is CaSe sEnSiTive.

The following options are available to configure on custom fields:

- **Model** - This is the object that the custom field will be added to. The available options are:
    - Agent
    - Site
    - Client
- **Name** - Sets the name of the custom field. This will be used to identify the custom field in the dashboard and in scripts.
- **Field Type** - Sets the type of field. Below are the allowed types.
    - Text
    - Number
    - Single select dropdown
    - Multi-select dropdown
    - Checkbox (`1` = Checked or `$null` = Unchecked)
    - DateTime
- **Input Options** - *Only available on Single and Multiple-select dropdowns*. Sets the options to choose from.
- **Default Value** - If no value is found when looking up the custom field; this value will instead be supplied.
- **Required** - This makes the field required when adding new Clients, Sites, and Agents *If this is set a default value will need to be set as well*.
- **Hide in Dashboard** - This will not show the custom field in Client, Site, and Agent forms in the dashboard. This is useful if the custom field's value is updated by a collector task and only supplied to scripts.

### Using Custom Fields in the Dashboard

Once the custom fields are added, they will show up in the Client, Site, and Agent Add / Edit forms.

### Using Custom Fields in Scripts

Tactical RMM allows for passing various database fields for Clients, Sites, and Agents in scripts. This includes custom fields as well!

!!!warning
    The characters within the brackets are case-sensitive!

In your script's arguments, use the notation `{{client.AV_KEY}}`. This will lookup the client for the agent that the script is running on and find the custom field named `AV_KEY` and replace that with the value.

The same is also true for `{{site.no_patching}}` and `{{agent.Another Field}}`.

For more information see the [Scripting](#scripting) section above.

### Populating Custom Fields Automatically

Tactical RMM supports automatically collecting information and saving them directly to custom fields. This is made possible by creating **Collector Tasks**. These are just normal Automated Tasks, but instead they will save the last line of the standard output to the custom field that is selected.

!!!info
    To populate a multiple select custom field, return a string with the options separated by a comma `"This,will,be,an,array"`.

For more information on Collector Tasks, see references/checks-tasks-policies.md.

---

## Global Key Store

The key store is used to store values that need to be referenced from multiple scripts. This also allows for easy updating of values since scripts reference the values at runtime.

To Add/Edit values in the Global Key Store, browse to **Settings > Global Settings > KeyStore**.

You can reference values from the key store in script arguments by using the {{global.key_name}} syntax.

!!!info
    Everything between {{}} is CaSe sEnSiTive. `global.` must be all lower case.

See the [Scripting](#scripting) section above for more information.
