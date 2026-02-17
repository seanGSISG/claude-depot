# Checks, Tasks, Automation Policies, and Maintenance Mode

> Sources: functions/automated_checks.md, functions/automated_tasks.md, functions/automation_policies.md, functions/maintenance_mode.md

## Table of Contents

- [Checks](#checks)
  - [Checks vs Tasks](#checks-vs-tasks)
  - [How Often Are Checks Run](#how-often-are-checks-run)
  - [Best Practices](#best-practices)
- [Automated Tasks](#automated-tasks)
  - [Task Triggers](#task-triggers)
  - [Task Actions](#task-actions)
  - [Collector Tasks](#collector-tasks)
- [Automation Policies](#automation-policies)
  - [Creating Automation Policies](#creating-automation-policies)
  - [Policy Inheritance](#policy-inheritance)
  - [Adding Windows Patch Management Policy](#adding-windows-patch-management-policy)
- [Maintenance Mode](#maintenance-mode)
  - [Putting Server into Maintenance Mode](#putting-server-into-maintenance-mode)

---

## Checks

### Checks vs Tasks

#### When to Use Checks for Scripts
- Define custom return codes for **Information** and **Warning** levels.
- Configure alerts only after a specified number of consecutive failures.

#### When to Use Tasks for Scripts
- Execute multiple commands and/or scripts in sequence.
- Leverage advanced scheduling options for flexibility.

### How Often Are Checks Run

The frequency of checks is controlled at two levels:

1. **Per Check Configuration**
   Each check has a **Run Check Every (seconds)** setting. Setting this to 0 defaults to the agent's global value.

2. **Agent Default Configuration**
   The default check frequency for the agent is set under **Edit Agent > General** in the **Run Checks Every** field. The default value is 120 seconds.

### Best Practices

- Use Automation Policies (see the [Automation Policies](#automation-policies) section below) to apply checks efficiently.
- Customize the frequency of individual checks as needed.

---

## Automated Tasks

An **Automated Task** allows you to run scripts and/or commands on an agent, with flexible scheduling options.

### Task Triggers

#### Time-Based
- **Daily, Weekly, or Monthly**: Schedule tasks to run at regular intervals, as expected. Note: On Linux and macOS, tasks will execute based on the "Start Time" field, ignoring the date portion. For example, a daily task set to start at 12:55 PM will run at that time every day starting from when the task is created.
- **Run Once**:
    - For future dates, tasks run as scheduled.
    - For past dates, tasks are created to run 5 minutes after being registered with the Windows Task Scheduler. This ensures the task runs at least once, as the scheduler will not execute tasks with past "Run Once" dates.

#### On Check Failure
Automatically trigger a script to address issues when a Check fails.

#### Onboarding
Use this type of task to execute "Run Once" scripts during agent onboarding. These tasks run immediately after the task is created on the agent, which happens a few minutes after the install of a new agent.

Ideal for:
- Setting workstation defaults
- Installing software
- Configuring machines

Integrate these tasks with Automation Policies (see the [Automation Policies](#automation-policies) section below) to streamline the setup of new devices.

#### Manual
Manually triggered tasks for on-demand operations.

Example: A **Windows Defender Cleanup Task** might perform the following when manually triggered:

1. Delete all Shadow Copies from VSS.
2. Create a new VSS Snapshot.
3. Clear Defender logs to prevent duplicate alerts.
4. Run a full Defender scan.

This is useful for addressing alerts about Defender detections (e.g., malware or adware in download folders).

### Task Actions

- Execute any script from your **Script Library**, or use Batch or PowerShell commands.
- Configure multiple scripts/commands to run sequentially.
  - Optionally continue or halt the sequence based on errors.

### Collector Tasks

Collector tasks allow you to save script output directly to a custom field.

#### How to Create Collector Tasks
1. Add the task to an Automation Policy (see the [Automation Policies](#automation-policies) section below) or directly to an agent.
2. During task creation:
   - Select the **Collector** checkbox.
   - Choose the custom field where the output should be saved.

> **Note:** Currently, you can only save data to agent-level custom fields.

For more details, see the Custom Fields and Scripting sections in references/scripting-and-variables.md.

---

## Automation Policies

Automation policies in Tactical RMM allow for mass deployment of Checks, Automated Tasks, Patch Policies, and Alert Templates. You can apply Automation Policies to:

- Global Settings
- Client
- Site
- Agent

You can also see a list of Relations that show what policy is applied to what Clients / Sites / Agents.

Before you ask, [multiple automation policies](https://github.com/amidaware/tacticalrmm/issues/665) per level is in the todo list.

### Creating Automation Policies

In the dashboard, navigate to **Settings > Automation Manager**. Use the **Add** button to create a blank Automation Policy. The options available are:

- **Name** - The name that will be used to identify the automation policy in the dashboard.
- **Description** - Optional description of the automation policy.
- **Enabled** - Specifies if the automation policy is active or not.
- **Enforced** - Specifies that the automation policy should overwrite any conflicting checks configured directly on the agent.

### Policy Inheritance

They get applied in this order:

1. Global Settings
2. Client
3. Site
4. Agent

At each level you can block policy inheritance from the level above using checkboxes in the appropriate screens.

### Adding Windows Patch Management Policy

Under the Automation Manager you can create a Patch Policy and control what patches are applied, when, and if the computer is rebooted after. See the Windows Update Management section in references/architecture.md for details on patch categories.

> **Note:** Most "regular" Windows patches are listed in the "Other" category.

---

## Maintenance Mode

Enabling maintenance mode for an agent will prevent any overdue/check/task email/sms alerts from being sent.

It will also prevent clients/sites/agents from showing up as red in the dashboard if they have any failing checks or are overdue.

To enable maintenance mode for all agents in a client/site, **Right Click** on a client / site and choose **Enable Maintenance Mode**.

To enable maintenance mode for a single agent, **Right Click** on the agent and choose **Enable Maintenance Mode**.

### Putting Server into Maintenance Mode

Follow the instructions in the Management Commands section of references/settings-and-admin.md to activate the python virtual env, then run the management command using one of the options below:

```
python manage.py server_maint_mode [options]
```

| Options              | Description                                                                                                                                                   |
|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--enable`        | **Enable Maintenance Mode.** Sets all agents to maintenance mode and saves their current states.                                                            |
| `--disable`       | **Disable Maintenance Mode.** Restores agents to their previous states before maintenance mode was enabled.                                                 |
| `--force-enable`  | **Force Enable Maintenance Mode.** Unconditionally sets all agents to maintenance mode, ignoring any previously saved states.                              |
| `--force-disable` | **Force Disable Maintenance Mode.** Unconditionally disables maintenance mode for all agents, removing any saved state information.                        |

**Note**: Only one of the above options should be used at a time to avoid conflicts.
