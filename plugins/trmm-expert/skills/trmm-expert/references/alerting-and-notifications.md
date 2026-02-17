# Alerting, Email/SMS Notifications, and Webhooks

> Sources: functions/alerting.md, functions/emailsms_alert.md, functions/webhooks.md

## Table of Contents

- [Alerting Overview](#alerting-overview)
  - [Supported Notifications](#supported-notifications)
  - [Alert Severities](#alert-severities)
  - [Creating Alert Templates](#creating-alert-templates)
    - [General Settings](#general-settings)
    - [Alert Action Settings](#alert-action-settings)
    - [Agent Overdue Setting](#agent-overdue-setting)
    - [Check Settings / Automated Task Settings](#check-settings--automated-task-settings)
  - [Applying Alert Templates](#applying-alert-templates)
  - [Alert Template Exclusions](#alert-template-exclusions)
  - [Alert Template Inheritance](#alert-template-inheritance)
  - [Setting up Alert Severities with Scripts](#setting-up-alert-severities-with-scripts)
- [Email and SMS Setup](#email-and-sms-setup)
  - [Email Setup](#email-setup)
    - [Setting up Alerts using Open Relay (MS 365)](#setting-up-alerts-using-open-relay-ms-365)
    - [Setting up Alerts using Username and Password (Gmail)](#setting-up-alerts-using-username-and-password-gmail)
  - [SMS Alerts](#sms-alerts)
- [Webhooks](#webhooks)
  - [Webhook Configuration Fields](#webhook-configuration-fields)
  - [Request Headers](#request-headers)
  - [Request Body](#request-body)
    - [Discord Example](#discord-example)
    - [Simple JSON Example](#simple-json-example)
    - [Microsoft Teams Basic Example](#microsoft-teams-basic-example)
    - [Microsoft Teams Advanced Example](#microsoft-teams-advanced-example)
    - [Slack Example](#slack-example)
    - [Ticketing System Example (Zammad)](#ticketing-system-example-zammad)
  - [Testing Webhooks](#testing-webhooks)

---

## Alerting Overview

Alerting and notifications can be managed centrally using Alert Templates. All an alert template does is configure the Email, Text, and Dashboard alert check boxes on Agents, Checks, and Automated Tasks.

Using Alert Templates also enables additional features like:

- Periodic notifications if an alert is left unresolved.
- Being able to notify on certain alert severities.
- Sending notifications when an alert is resolved.
- Executing scripts when an alert is triggered or resolved.

See the [Email and SMS Setup](#email-and-sms-setup) section below for email alert configuration examples.

### Supported Notifications

- **Email Alerts** - Sends email to configured set of email addresses.
- **SMS Alerts** - Sends text messages to configured set of numbers.
- **Dashboard Alerts** - A notification popup will show up and be visible in the dashboard.
- **Webhooks** - Send an API request. See the [Webhooks](#webhooks) section below.

### Alert Severities

Agent overdue alerts are always of severity: `Error`.

Alert severities are configured directly on the Check or Automated Task. When the Check or Automated Task fails, it will create an alert of the specified severity. The severity types are:

- Informational
- Warning
- Error

### Creating Alert Templates

To create an alert template, go to **Settings > Alerts Manager**, then click **New**.

The available options are:

#### General Settings

- **Name** - The name that is used to identify the Alert Template in the dashboard.
- **Email Recipients** - Sets the list of email recipients. If this isn't set the email recipients in global settings will be used.
- **From Email** - Sets the From email address of the notification. If this isn't set the From address from global settings is used.
- **SMS Recipients** - Sets the list of text recipients. If this isn't set the sms list from global settings is used.

#### Alert Action Settings

For optionally triggering an additional task (Send a Web Hook, Run Script on Agent, Run script on TRMM Server) when desired (can be left blank for no action).

##### Alert Failure Settings / Alert Resolved Settings

##### Send a Web Hook

You can create your own webhooks to be sent out on alert failure/resolved events, like a script check or task failing or an agent going overdue.

You have access to any of the script variables (see references/scripting-and-variables.md) as well as custom fields and global keystore (see references/scripting-and-variables.md) inside the json payload of the webhook as well as in the URL pattern.

1. Create your webhooks (see the [Webhooks](#webhooks) section below).
2. Choose the Web Hook you wish to be ran as the alert failure and/or resolved action.

##### Run Script on Agent

- **Script** - Runs the selected script once. It attempts to run it on the agent in question, but if not online TRMM selects a random agent to run on.
- **Script arguments** - Optionally pass in arguments to the script.
- **Script environment vars** - Optionally pass in env vars to the script.
- **Action Timeout** - Sets the timeout for the script.

##### Run Script on Server

> **Warning:** This is a dangerous feature and you must ensure permissions are appropriate for your environment. See the Permissions section in references/settings-and-admin.md for details on permissions with extra security implications.

This runs the script on your TRMM server. To ensure proper execution, you must specify the interpreter for your script using a shebang line at the top of each script. Also make sure that the specified interpreter is installed on your TRMM server.

Just like with webhooks, you also have access to the same script variables (see references/scripting-and-variables.md) as well as custom fields and global keystore (see references/scripting-and-variables.md) in the script's arguments or environment variables.

**Python (included with TRMM):**

Shell type: `Shell`

```py
#!/rmm/api/env/bin/python

import sys

print(sys.version)
```

**Python (system python):**

Shell type: `Shell`

```py
#!/usr/bin/python3
import sys

print(sys.version)
```

**Bash:**

Shell type: `Shell`

```bash
#!/usr/bin/env bash

echo "hello world"
```

**Powershell (7 PWSH):**

To install, see: https://learn.microsoft.com/en-us/powershell/scripting/install/install-debian

Shell type: `Powershell`

```powershell
#!/usr/bin/pwsh

Write-Output "Hello World"
```

**Node (included with TRMM):**

Shell type: `Shell`

```
#!/usr/bin/node

console.log("Hello World")
```

**Deno (must be installed):**

Shell type: `Deno`

```
#!/usr/bin/env -S /usr/local/bin/deno run --allow-allow

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

- **Script** - Runs the selected script once on the TRMM server.
- **Script arguments** - Optionally pass in arguments to the script.
- **Script environment vars** - Optionally pass in env vars to the script.
- **Action Timeout** - Sets the timeout for the script.

##### Run Actions Only On

Turn the switch on if you want the above Alert Failure/Alert Resolved script to run on:

- **Agents** - If Enabled, will run script failure / resolved actions on agent overdue alerts, else no alert actions will be triggered for agent overdue alerts.
- **Checks** - If Enabled, will run script failure / resolved actions on check alerts, else no alert actions will be triggered check alerts.
- **Tasks** - If Enabled, will run script failure / resolved actions on automated task alerts, else no alert actions will be triggered automated task alerts.

#### Agent Overdue Setting

- **Email** - When **Enabled**, will send an email notification and override the Email Alert checkbox on the Agent / Check / Task. When **Not Configured**, the Email Alert checkbox on the Agent / Check / Task will take effect. If **Disabled**, no email notifications will be sent and will override any Email alert checkbox on the Agent / Check / Task.
- **Text** - When **Enabled**, will send a text notification and override the SMS Alert checkbox on the Agent / Check / Task. When **Not Configured**, the SMS Alert checkbox on the Agent / Check / Task will take effect. If **Disabled**, no SMS notifications will be sent and will override any SMS Alert checkbox on the Agent / Check / Task.
- **Dashboard** - When **Enabled**, will send a dashboard notification and override the Dashboard Alert checkbox on the Agent / Check / Task. When **Not Configured**, the Dashboard Alert checkbox on the Agent / Check / Task will take effect. If **Disabled**, no dashboard notifications will be sent and will override any Dashboard Alert checkbox on the Agent / Check / Task.
- **Alert again if not resolved after (days)** - This sends another notification if the alert isn't resolved after the set amount of days. Set to 0 to disable this.
- **Alert on severity** - Only applicable to Check and Task alert notifications. This will only send alerts when they are of the configured severity.

> **Important:** Alert on Severity needs to be configured for check and task notifications to be sent!

#### Check Settings / Automated Task Settings

- **Email** - If enabled, sends an email notification when an alert is resolved.
- **Text** - If enabled, sends a text message when an alert is resolved.

### Applying Alert Templates

Alert templates can be configured:

- Globally at the Server Level (see the Global Settings section in references/settings-and-admin.md)
- By Automation Policy (see references/checks-tasks-policies.md)
- Manually at the Client Level
- Manually at the Site Level

To apply **Globally**, navigate to **Settings > Global Settings**. Set the **Alert Template** dropdown and save.

You can configure an alert template on an automation policy by navigating to **Settings > Automation Manager**, and clicking the **Assign Alert Template** click on the policy, or right-clicking the policy and selecting **Assign Alert Template**.

To configure on a Client or Site right-click on one in the Client / Site tree view and select **Assign Alert Template**.

### Alert Template Exclusions

You can exclude Clients, Sites, and Agents from Alert Templates. To do this you can:

- Right-click on the **Alert Template** in **Alerts Manager** and select **Exclusions**.
- Select the **Alert Exclusions** link in the Alert Template row.

You can also **Exclude Desktops** from the alert template. This is useful if you only care about servers.

### Alert Template Inheritance

Alerts are applied in the following order. The agent picks the closest matching alert template.

1. Policy w/ Alert Template applied to Site
2. Site
3. Policy w/ Alert Template applied to Client
4. Client
5. Default Alert Template

### Setting up Alert Severities with Scripts

If scripting for alert severities, follow these steps:

1. Create a script with exit codes. The exit codes can be anything other than 0 (which is reserved for passing). Below we are using 2 as a Warning and 5 as Informational, any other code will be assumed to be an Error.

    ```ps
    If (!(test-path c:\ProgramData\TacticalRMM\temp)) {
        New-Item -ItemType Directory -Force -Path "C:\ProgramData\TacticalRMM\temp"
        $exitcode = 2
        $host.SetShouldExit($exitcode)
        exit
    }
    Else {
        Write-Output "found folder"
        $exitcode = 5
        $host.SetShouldExit($exitcode)
        exit
    }
    ```

2. Setup a script check and fill in the corresponding Warning and Informational codes (don't forget to hit enter).
3. Save script check and you should now have the different Severities.

---

## Email and SMS Setup

### Email Setup

Under **Settings > Global Settings > Email Alerts**

#### Setting up Alerts using Open Relay (MS 365)

MS 365 in this example:

1. Log into Tactical RMM
2. Go to Settings
3. Go to Global Settings
4. Click on Alerts
5. Enter the email address (or addresses) you want to receive alerts to eg info@EXAMPLE.COM
6. Enter the from email address (this will need to be part of your domain on 365, however it doesn't need a license) eg rmm@EXAMPLE.COM
7. Go to MXToolbox.com and enter your domain name in, copy the hostname from there and paste into Host
8. Change the port to 25
9. Click Save
10. Login to admin.microsoft.com
11. Go to Exchange Admin Centre
12. Go to "Connectors" under "Mail Flow"
13. Click to + button
14. In From: select "Your organizations email server"
15. In To: select "Office 365"
16. Click Next
17. In the Name type in RMM
18. Click By Verifying that the IP address...
19. Click +
20. Enter your IP and Click OK
21. Click Next
22. Click OK

#### Setting up Alerts using Username and Password (Gmail)

Gmail in this example:

1. Log into Tactical RMM
2. Go to Settings
3. Go to Global Settings
4. Click on Alerts
5. Enter the email address (or addresses) you want to receive alerts to eg info@EXAMPLE.COM
6. Enter the from email address myrmm@gmail.com
7. Tick the box "My server requires Authentication"
8. Enter your username e.g. myrmm@gmail.com
9. Enter your password
10. Change the port to 587
11. Click Save

### SMS Alerts

Under **Settings > Global Settings > SMS Alerts**

Currently Twilio is the only supported SMS service.

Setup an Auth Token, and copy the data to the relevant fields.

---

## Webhooks

To apply webhooks and run them on Agent overdue and Check/Task failures, use Alert Templates (see the [Alert Action Settings](#alert-action-settings) section above).

### Webhook Configuration Fields

- `Name`: Name of the webhook.
- `Description`: Notes about the webhook.
- `URL Pattern`: For webhooks, you need a URL where the Tactical RMM can send HTTP requests when an event occurs. This URL should be a server endpoint configured to accept HTTP requests.

### Request Headers

Request headers allow the server to learn more about the request context. Here are some common headers used in webhook configurations:

- **Content-Type**: Describes the nature of the data being sent. For JSON data, you use `application/json`.
- **Authorization**: If your endpoint requires authentication, you might use a token or other credentials in this header.
- **User-Agent**: Identifies the application making the request.

```json
{
    "Content-Type": "application/json"
}
```

### Request Body

The request body must contain valid JSON and can include anything you want. Here are some examples:

#### Discord Example

Discord: Edit a channel > Integrations > Webhooks

```json
{
    "content": "Agent hasn't checked in for {{agent.overdue_time}} minutes.",
    "username": "{{agent.hostname}}",
    "avatar_url": "https://cdn3.emoji.gg/emojis/PogChamp.png",
    "embeds": [
        {
            "title": "Agent {{agent.hostname}} Client: {{agent.site.client.name}}",
            "description": "This is an embed",
            "color": 15258703,
            "fields": [
                {
                    "name": "Field1",
                    "value": "Some value",
                    "inline": true
                },
                {
                    "name": "Field2",
                    "value": "Another value",
                    "inline": true
                }
            ]
        }
    ]
}
```

#### Simple JSON Example

```json
{
    "text": "{{agent.hostname}}: {{alert.message}}"
}
```

#### Microsoft Teams Basic Example

Microsoft Teams uses Office 365 Connectors for its incoming webhooks. The format for Teams is slightly more complex, allowing for potentially richer content.

Reference: https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook

```json
{
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Issue 176715375",
    "themeColor": "0078D7",
    "title": "Issue opened: \"Push notifications not working\"",
    "sections": [{
        "activityTitle": "Mona Lisa",
        "activitySubtitle": "On Project XYZ",
        "activityImage": "https://teamsnodesample.azurewebsites.net/static/img/image5.png",
        "facts": [{
            "name": "Assigned to",
            "value": "Unassigned"
        }, {
            "name": "Due date",
            "value": "2016-08-29T04:31:32.993Z"
        }],
        "markdown": true
    }]
}
```

#### Microsoft Teams Advanced Example

Uses Adaptive Cards for richer formatting.

Reference: https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook

```json
{
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": null,
            "content": {
                "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "msteams": {
                    "width": "Full"
                },
                "body": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "Image",
                                        "style": "person",
                                        "url": "https://amidaware.com/images/amidaware.jpg",
                                        "altText": "TacticalRMM",
                                        "size": "small"
                                    }
                                ],
                                "width": "auto"
                            },
                            {
                                "type": "Column",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "weight": "bolder",
                                        "text": "TacticalRMM",
                                        "wrap": true,
                                        "size": "heading"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "spacing": "none",
                                        "text": "Created date here",
                                        "isSubtle": true,
                                        "wrap": true
                                    }
                                ],
                                "width": "stretch"
                            }
                        ]
                    },
                    {
                        "type": "ColumnSet",
                        "isVisible": true,
                        "columns": [
                            {
                                "type": "Column",
                                "isVisible": true,
                                "items": [
                                    {
                                        "type": "RichTextBlock",
                                        "inlines": [
                                            {
                                                "type": "TextRun",
                                                "text": "first column more text",
                                                "wrap": true,
                                                "color": "default",
                                                "weight": "bolder"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "isVisible": true,
                                "items": [
                                    {
                                        "type": "RichTextBlock",
                                        "inlines": [
                                            {
                                                "type": "TextRun",
                                                "text": "Second column",
                                                "wrap": true
                                            },
                                            {
                                                "type": "TextRun",
                                                "text": "second column more text",
                                                "wrap": true,
                                                "color": "default",
                                                "weight": "bolder"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "style": "emphasis",
                                "minHeight": "40px",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "The minimal message!",
                                        "wrap": true
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "auto",
                                "verticalContentAlignment": "center",
                                "isVisible": false,
                                "items": [
                                    {
                                        "type": "ActionSet",
                                        "isVisible": false,
                                        "actions": []
                                    },
                                    {
                                        "type": "ActionSet",
                                        "isVisible": false,
                                        "actions": []
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]
}
```

#### Slack Example

Reference: https://api.slack.com/messaging/webhooks

You can also send more complex messages with attachments, buttons, etc., by using Slack's rich messaging format.

```json
{
    "text": "Hello, world! This is a line of text.\nAnd this is another one."
}
```

#### Ticketing System Example (Zammad)

See the Zammad integration section in references/integrations-and-tips.md for how to open a ticket in Zammad with a webhook alert.

### Testing Webhooks

Use the test button to make sure your webhook is working. Note: `{{alert.XXX}}` variables will NOT be available in testing mode.
