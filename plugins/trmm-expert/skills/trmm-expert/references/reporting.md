# Reporting (Enterprise Edition)

> Sources: ee/reporting/reporting_overview.md, ee/reporting/functions/reporting_basics.md, ee/reporting/functions/reporting_basetemplates.md, ee/reporting/functions/reporting_dataqueries.md, ee/reporting/functions/reporting_variables.md, ee/reporting/functions/reporting_assets.md, ee/reporting/functions/examples.md, ee/reporting/functions/tipsntricks.md, ee/reporting/functions/faq.md

> **Note:** Reporting is an Enterprise Edition feature. It requires a sponsorship tier (Tier 2 or higher, Tier 1 for Non-Profits) and a valid code signing token. Existing sponsors as of Oct 31, 2023 received a Founders Edition perpetual reporting license.

## Table of Contents

- [Reporting Overview](#reporting-overview)
- [The Basics](#the-basics)
  - [Reporting Formats](#reporting-formats)
  - [The Toolbar](#the-toolbar)
  - [Variables](#variables-basics)
  - [Data Queries (Basics)](#data-queries-basics)
  - [Report Output Format](#report-output-format)
  - [CSS](#css)
  - [Report Assets (Basics)](#report-assets-basics)
  - [Base Templates (Basics)](#base-templates-basics)
  - [Template Dependencies](#template-dependencies)
  - [Report Preview](#report-preview)
  - [Running a Report](#running-a-report)
- [Base Templates](#base-templates)
  - [Adding Base Templates](#adding-base-templates)
  - [Using a Base Template](#using-a-base-template-in-your-report-template)
  - [Using Blocks](#using-blocks)
  - [Multiple Blocks](#multiple-blocks)
  - [Variable Analysis (Base Templates)](#variable-analysis-base-templates)
- [Data Queries](#data-queries)
  - [Introduction](#introduction)
  - [Template Dependencies in Data Queries](#template-dependencies-in-data-queries)
  - [Data Query Editor](#data-query-editor)
  - [Syntax Reference](#syntax)
  - [Relations](#relations)
- [Variables](#variables)
  - [Sample Variables](#some-sample-variables-and-how-to-use-them-in-the-template)
  - [Dependencies](#dependencies)
  - [Variable Analysis](#variable-analysis)
  - [Python Modules Available](#python-modules-available-in-template)
  - [Custom Jinja Filters](#custom-jinja-filters)
  - [Custom Processors](#custom-processors)
- [Report Assets](#report-assets)
  - [Managing Assets](#managing-assets)
  - [Using Assets in Templates](#using-assets-in-report-templates)
- [Example Reports](#example-reports)
  - [Agent Uptime](#agent-uptime)
  - [Windows 11 Upgrade Compatible List](#windows-11-upgrade-compatible-list)
  - [Antivirus Report](#antivirus-report)
  - [NOC Dashboard](#noc-dashboard)
  - [Software Inventory](#software-inventory)
- [Tips and Tricks](#tips-and-tricks)
  - [Formatting Matters](#formatting-matters)
  - [Quick Report Generation](#quickly-generate-reports-from-clientsite-tree)
  - [Change PDF Orientation to Landscape](#change-pdf-orientation-to-landscape)
  - [Making API Calls from Within a Report Template](#making-api-calls-from-within-a-report-template)
- [Reporting FAQ](#reporting-faq)
  - [Pricing](#pricing)
  - [Enabling Reporting as a New Sponsor](#how-do-i-enable-reporting-as-a-new-sponsor)
  - [Charts and Graphs](#how-do-i-add-chartsgraphs-to-my-report-templates)

---

## Reporting Overview

*Released in TRMM v0.17.0 (Nov 1, 2023)*

The reporting addon allows you to access your Tactical RMM data and represent it in the format of your choice. This could be a PDF file, a simple CSV, or a complex interactive web dashboard.

It is best to get started with using the shared templates (available at the `amidaware/reporting-templates` GitHub repository) and go from there -- you can import these directly from the TRMM web UI with 1 click. The sections below will help you get familiar with the terminology and the syntax.

---

## The Basics

Report templates are built using the Jinja templating engine. A reference guide can be found at the Jinja documentation site (jinja.palletsprojects.com).

### Reporting Formats

You can write report templates using **Markdown**, **HTML**, or **Plain Text**. HTML and Markdown reports will look the same regardless of choice. Templates cannot be converted between formats, but it would be easy enough to do the conversion manually between markdown and HTML.

#### Markdown templates

HTML is valid in markdown and should be used when the Markdown syntax doesn't do exactly what you need. An example would be for using the `<table>` tag.

The markdown is rendered to HTML. See the Daring Fireball Markdown syntax reference for details.

#### Plain text templates

Plain Text templates are a great choice if you just want to generate some text without all of the formatting. This is very useful if you want a CSV export of some data.

### The Toolbar

The toolbar along the top of the editor provides some shortcuts for commonly used functions. Most of the buttons are used for text formatting, but there are some shortcuts for adding/editing data queries, base templates, and inserting charts and tables. Hovering over the button will display its function.

### Variables (Basics)

You can add in variables in the right editor pane. The variables pane can be toggled on/off using the *vars* button on the toolbar. The variables are added in YAML format and can be referenced using `{{variable_name}}` in the template. The value of the variable will be substituted when the template is rendered. If the value of the variables is nested within an object, you can use dot notation to render the value like `{{ object.variable_name }}`. If there is a space in the name you can use `{{ object["variable name"] }}`.

#### Variable analysis

With data sources and other dynamic sources, it can be difficult to view what the data looks like to use in report templates. With variable analysis, the query is run and the available properties are returned. Click on the `>` arrow on the top left of the editor window (under the toolbar) to see the available properties from the variables section. You can then click on them to copy and you can paste them into the template.

For array values, you can click the **For loop** button and paste in a Jinja for loop to easily loop over the properties.

### Data Queries (Basics)

Data queries are a way to save commonly used queries and use them in templates. Data queries are added under the `data_sources` key in the variables section. If the key doesn't exist, it will be created.

#### Adding data queries

Using the **Add Data Query** button on the toolbar, it will open the data query editor. This editor will let you know the valid syntax of the query and supports auto-complete. If you are stumped and need to know all of the values that are supported you can press Ctrl+Space and a dropdown will show. Once you add the query, it will be auto-inserted into the template.

You can also add a data query from the **Report Manager** and open the Data Queries button along the top. This is the same function as using the toolbar, but it will save the query to allow it to be used in templates.

#### Inserting saved data queries

You can insert a saved data query using the **Insert Data Query** button on the toolbar. You just have to select the data query from the drop down and it will insert it into the template.

#### Editing data queries

You can edit data queries in the template by clicking the **Edit Data Query** button on the toolbar. This will list the currently added data_sources into a dropdown and allow you to edit them in the auto complete editor. Clicking save will replace the data query in the variables with the updated one.

### Report Output Format

Reports can be output in either **HTML**, **PDF**, or in **Plain Text** format.

#### HTML and Markdown Template types

HTML and Markdown template types can be output in PDF or HTML formats. These template types don't support plain text output.

#### Plain Text

Plain text template types can be output in PDF or text. This template type doesn't support HTML output. Putting markdown or anything else in a plain text template will just output the same markdown. It isn't processed through the markdown library.

### CSS

CSS can be embedded in the report template using the CSS tab on the top right on the report template editor. The CSS class can be referenced in the report template for styling.

If you are using markdown, you can add ids and classes to HTML elements by using `{#id_name}` and `{.class_name}` beside the template.

This will render an h1 HTML tag with an id of 'id-name': `{#id-name}`

This will render an h1 HTML tag with a class of 'class-name': `{.class-name}`

### Report Assets (Basics)

Assets can be served from your Tactical RMM instance. They will need to be uploaded to the Asset Manager first. This can be accessed from the Reporting Manager windows by clicking on the Report Assets.

Once uploaded, click on the *Image* button on the toolbar and select the **Report Asset** radio button. From there you can click on an asset and go to Insert.

### Base Templates (Basics)

Base Templates allow you to use the same report structure throughout multiple reports. The base template should be a full HTML document enclosed in an html tag. To specify content that should be overridden in the child template, you can use Jinja blocks in the base template. See the Jinja documentation on template inheritance for details.

You can add a base template from the report template editor by clicking the *base* button on the toolbar.

When you select a base template (using the dropdown) in a report template, the **extends** block will automatically be inserted. You can click on the variable analysis button (top-left arrow) to see which blocks in the base template need to be overridden yet. Clicking on the block in variable analysis will copy the text to the clipboard and will need to be copied into the template.

### Template Dependencies

Sometimes you need to provide data during a report's runtime. This could be a specific client, a date range, etc. This is achievable by setting a template dependency using the **Template Dependencies** dropdown on the report editor. The default values are Client, Site, and Agent. You can type additional values that are required for the report.

In your variables and report template, you can use these dependencies by enclosing the name of the dependency like so: `{{agent.hostname}}` or `{{client.name}}`. For custom dependencies you can just type in `{{ dependency_name }}`. These are case sensitive.

### Report Preview

You can easily see what a report is going to look like by pressing the Preview button on the top right of the editor window. You can choose between an HTML or PDF output using the radio buttons.

If you have report dependencies, a dialog box will show asking you to fill in the values that should be used to generate the report.

#### Debug

If you need additional info showing the values of the variables and the rendered HTML, you can check the debug button. This will show at the bottom of the preview window.

### Running a Report

Running a report can be done from the Reporting Manager by right-clicking on the report template and either running as an HTML or PDF report. The report will open up in a separate window. If there are report dependencies, a dialog will prompt to populate the values.

You can save the URL or bookmark it to easily generate the same report without having to populate the dependencies.

If you have a Client, Site, or Agent dependency specified in the report, you can also right-click on the respective entity in Tactical RMM and go to **Integrations > Run Report**. You can then specify a report output type and the entity that you right-clicked on will automatically populate as a dependency.

---

## Base Templates

Base Templates are used to apply the same formatting to multiple templates. The base template will declare one or more "blocks" that are then filled in by the child template. Base templates use the Jinja syntax for inheriting and extending. See the Jinja documentation on template inheritance for details.

> Even though the examples for base templates are in HTML, you can use any format you want.

### Adding Base Templates

To add a base template you can browse to **Reports Manager > Base Templates > Add**. From there you can create your base template in the editor and click save.

### Using a Base Template in Your Report Template

To use the base template, we will need to open up the Report Template editor (**Reports Manager > double-click on the template**), then select the base template from the dropdown.

> This will automatically add the `{% extends ... %}` tag at the beginning of the report template on the backend. If you are looking through the Jinja base template documentation, you can omit that line.

### Using Blocks

See below for a basic base template that specifies one block.

```html
<html>
    <head>
        <style>
            {{css}}
        </style>
    </head>
    <body>
        {% block content%}{% endblock %}
    </body>
</html>
```

In the template that is inheriting the base template above, you can fill in these blocks like so:

```
{% block content%}
This will show up between the <body> tags in the base template/
{% endblock %}
```

### Multiple Blocks

We can also fill in multiple blocks if they are specified in the base template. Any blocks that aren't used will just be blank.

```html
<html>
    <head>
        <style>
            {{css}}
        </style>
    </head>
    <body>
        <div id="header">
        {% block header %}{% endblock %}
        </div>

        <div id="content">
        {% block content %}{% endblock %}
        </div>

        <div id="footer">
        {% block footer %}{% endblock %}
        </div>
    </body>
</html>
```

In the template, we just need to use the same blocks and it will fill in the data.

```
{% block header %}
This is the header
{% endblock %}

{% block content %}
This is the content
{% endblock %}

{% block footer %}
This is the footer
{% endblock %}
```

### Variable Analysis (Base Templates)

In the Report Template editor, you can quickly see what blocks the base template has available. You can click on the `>` button in the top-left of the editor (under the report name field) and at the top it will give a warning if it doesn't see the blocks listed. You can also click on the blocks to copy them to the clipboard to be pasted into the template.

---

## Data Queries

### Introduction

Data queries allow you to pull information from the Tactical RMM database to use in your templates. Data queries are defined in the variables editor under the `data_sources` object. There is a predefined format that the data query must follow and it is defined using a JSON or YAML syntax.

At its simplest form, a data query just specifies a model. Doing this will pull all of the records and columns available from the table.

This is an example of a data query that pulls all columns and rows from the sites table:

```yaml
data_sources:
    sites:
        model: site
```

Once this is specified in the variables, you can use this data in the template like this: `{{data_sources.sites}}`. This will just dump the data into the template, but it isn't very useful. We can actually loop over this data query to format it using a Jinja for loop.

```
{% for item in data_sources.sites %}
{{item.name}}
{% endfor %}
```

This will print out the name of every site on a new line.

We can have multiple data_sources specified also like so:

```yaml
data_sources:
    sites:
        model: site
    clients:
        model: client
```

The same rules apply for the second query. You can reference it in your templates using `{{data_sources.clients}}`.

### Template Dependencies in Data Queries

Template dependencies allow you to pass information to a report at runtime. This could be a client, site, or agent. You can use template dependencies in your data queries by using the `{{ }}` in place of the data you want to replace. See the example below for a client dependency:

```yaml
data_sources:
    sites:
        model: site
        filter:
            client_id: '{{ client.id }}'
```

> Note that quotes are required around `{{}}` tags in the variables section.

### Data Query Editor

There is a data query editor that supports auto-complete so that you can more easily determine which columns and relations are available. *It is recommended to always use this editor to avoid typos and errors when generating reports.* You can open the query editor by going to **Reports Manager > Data Queries > New** or in the template editor by clicking **Add Data Query** or **Edit Data Query** toolbar button in the template.

The Query Editor uses JSON syntax to provide the auto-complete functionality. You can either start typing to trigger the auto-complete list, or press the Ctrl+Alt key.

### Syntax

Below are the allowed properties in a data query. You can combine these properties together in the same data query unless specifically noted.

#### model - string

The only required field for a data query is the **model**. This tells the system which database table to pull the data from. The available models are:

* agent
* agentcustomfield
* agenthistory
* note
* alert
* auditlog
* automatedtask
* check
* checkhistory
* checkresult
* chocosoftware
* client
* clientcustomfield
* debuglog
* globalkvstore
* pendingaction
* policy
* site
* taskresult
* winupdate
* winupdatepolicy

#### only - array of strings

**Only** is useful for only pulling certain columns. This is recommended if you are pulling data from the agents table since **services** and **wmi_detail** columns are very large and can take a long time to run.

A few examples of using only:

```yaml
data_sources:
    sites:
        model: site
        only:
          - name
          - failing_checks
    clients:
        model: client
        only:
          - name
          - failing_checks
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
```

#### defer

To not load some fields by default to limit data from being pulled, unless it is needed later for some reason.

#### custom_fields - array of strings

This is only applicable to the **client**, **site**, and **agent** model. You can pass an array of strings with names of custom fields and it will inject them into the data.

Lets say we have these custom fields configured:

Client:
- custom_field
- Custom Field 2

Site:
- another Custom Field
- no_spaces

Agent:
- agent_custom_field

We can pull this data in a data query like this:

```yaml
data_sources:
    clients:
        model: client
        only:
          - name
          - failing_checks
        custom_fields:
          - custom_field
          - Custom Field 2
    sites:
        model: site
        only:
          - name
          - failing_checks
        custom_fields:
          - another Custom Field
          - no_spaces
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
        custom_fields:
          - agent_custom_field
```

The custom field names are case sensitive and the custom field must be configured in the system or no custom data will be pulled. A `custom_fields` object is added to the data and is accessible in the template.

You can access the custom field data for the clients data query like this:

```
{% for item in data_source.clients %}
{{ item.custom_fields.custom_field }}
{{ item.custom_fields["Custom Field 2"] }}
{% endfor %}
```

Note that you can't use dot notation for a property if it has spaces. See the above example for the **Custom Field 2** property.

#### properties - array of strings

This will allow injecting model @property fields into the data. The current supported fields are:

**Agent**

* client
* timezone
* is_posix
* arch
* status
* checks
* pending_actions_count
* cpu_model
* graphics
* local_ips
* make_model
* physical_disks
* serial_number

**AgentCustomField**

* value

**Alert**

* assigned_agent
* site
* client
* get_result

**Policy**

* is_default_server_policy
* is_default_workstation_policy

**Automated Task**

* schedule

**Check**

* readable_desc

**CheckResult**

* history_info

**Client**

* live_agent_count

**Site**

* live_agent_count

**Client Custom Field**

* value

**Site Custom Field**

* value

We can pull this data in a data query like this:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
        properties:
          - status
          - is_posix
          - make_model
          - cpu_model
    checks:
      model: check
      properties:
        - readable_desc
```

You can access the property data directly on the agent in the template like this:

```
{% for item in data_source.agents %}
{{ item.status }}
{{ item.make_model }}
{% endfor %}
```

#### filter - object

Using the filter property, you can filter the amount of rows that are returned. This is useful if you only want agents for a particular client or site, or you only want agents that are pending a reboot.

See below for an example:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        filter:
            needs_reboot: True
```

This data query will only return agents that need a reboot. We can also add a second filter like so:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        filter:
            needs_reboot: True
            plat: "windows"
```

The above is just doing an *equals* comparison to make sure the rows match. You can also use other operations like greater than, contains, etc.

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        filter:
            operating_system__contains: "22H2"
```

To use the contains filter, we need to append two underscores (_) and type in the field lookup. This uses the Django built-in field lookups. A full list can be found in the Django documentation for field lookups.

#### exclude - object

We can use this to exclude rows from our data. The same rules that apply for filter apply here.

Example:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        exclude:
            plat: "linux"
```

#### limit - number

This will limit the number of returned rows in the data.

Example:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        limit: 400
```

#### get - boolean

Instead of returning a list, the data query will attempt to return a single object. This is best used with a filter that guarantees a single row returned, i.e: filtering by id. This will error out if the query returns more than one object.

Example:

```yaml
data_sources:
    agent:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        filter:
          agent_id: hjk1hj23hj23hkj2hjh3j2h3
        get: true
```

In the template, you can use the properties directly instead of looping:

```
{{data_sources.agent.hostname}}
{{data_sources.agent.operating_system}}
```

#### first - boolean

This will return the first row in a table. This is guaranteed to always return one result. You can apply other properties (like filter or exclude) also to limit the data.

Example:

```yaml
data_sources:
    agent:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        first: true
```

In the template, you can use the properties directly instead of looping:

```
{{data_sources.agent.hostname}}
{{data_sources.agent.operating_system}}
```

#### count - boolean

This allows you to return the number of rows found. Can be used with filter or exclude.

Example:

```yaml
data_sources:
    agent:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        count: true
```

#### order_by - string

This allows you to sort/reorder the returned data based on a specific column. Putting a `-` before the column puts it in descending order and the default is ascending order.

Ascending Example:

```yaml
data_sources:
    agent:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        order_by: hostname
```

Descending Example:

```yaml
data_sources:
    agent:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
        order_by: -hostname
```

#### csv - boolean | object

This is a shorthand to return a string formatted as a CSV.

Example:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
          - site__name
          - site__client__name
        filter:
            site__client__name: "Client Name"
        csv: true
```

This will add a **site__name** and **site__client__name** column on the returned data. We use a double underscore every time we want to go to another table. The site column exists directly on the agents table. So in order to get the name (which resides on the sites table) we need to use the double underscore. Same thing with the client name. We need to go through the sites table in order to get the client name so we use another double underscore.

Usage in template:

`{{data_sources.agents}}`

Output will look something like:

```
hostname,operating_system, plat,needs_reboot,site__name,site__client__name
data,data,data,data,data,data
```

You can also rename the columns by passing a mapping into csv like so:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
          - site__name
          - site__client__name
        filter:
            site__client__name: "Client Name"
        csv:
            hostname: Hostname
            operating_system: Operating System
            plat: Platform
            needs_reboot: Needs Reboot
            site__name: Site Name
            site__client__name: Client Name
```

Which would return something like:

```
Hostname,Operating System,Platform,Needs Reboot,Site Name,Client Name
data,data,data,data,data,data
```

#### json - boolean

This will return a JSON string representation of the object. This is useful if you are passing the data source to be processed by javascript.

Example:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
          - site__name
          - site__client__name
        filter:
            site__client__name: "Client Name"
        json: true
```

Usage in template:

`{{data_sources.agents}}`

### Relations

You can include columns from a related model by using the double underscore syntax. You may have a data query using the agents table, but want to include the Site name and the Client name. See the example below:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
          - site__name
          - site__client__name
```

This will add a **site__name** and **site__client__name** column on the returned data. We use a double underscore every time we want to go to another table. The site column exists directly on the agents table. So in order to get the name (which resides on the sites table) we need to use the double underscore. Same thing with the client name. We need to go through the sites table in order to get the client name so we use another double underscore.

All available combinations are listed in the query editor.

To display these columns in the template you can do this:

```
{% for item in data_source.agents %}
{{ item.site__name }}
{{ item.site__client__name }}
{% endfor %}
```

We can also filter based on relations. See below:

```yaml
data_sources:
    agents:
        model: agent
        only:
          - hostname
          - operating_system
          - plat
          - needs_reboot
          - site__name
          - site__client__name
        filter:
            site__client__name: "Client Name"
```

---

## Variables

Variables provide a way to enrich your report with data. Variables are entered using YAML syntax and can be edited directly in the template by using the variables editor on the right. Everything with YAML is case-sensitive, so make sure to check for typos!

YAML syntax and features reference can be found at quickref.me/yaml.

### Some Sample Variables and How to Use Them in the Template

**Variables**

```yaml
title: Title Name
listOfData: [12, 13, 14]
an_object:
    key: value
    key2: value2
    key with a space: value3
an_array_of_objects:
    - key: value
      key2: value2
      the space: value3
    - key: value
      key2: value2
      the space: value3
```

**Markdown Template**

```md
# {{title}}

## A list of numbers
{% for item in listOfData %}
* {{item}}
{% endfor %}

## List the object keys
* {{an_object.key}}
* {{an_object.key2}}
* {{an_object["key with a space"]}}

## List of objects
{% for item in an_array_of_objects %}
* {{item.key}}
* {{item.key2}}
* {{item["the space"]}}
{% endfor %}
```

**Rendered Output**

```md
# Title Name

## List of numbers
* 12
* 13
* 14

# List the object keys
* value
* value2
* value3

## List of objects
* value
* value2
* value3
* value
* value2
* value3
```

### Dependencies

Dependencies offer a way to provide information to the templating engine at the report's runtime. The three built-in dependencies are **client**, **site**, and **agent**. The dependencies dropdown also allows for custom values to be entered. When you run the report, a dialog box will show that requires you to provide the values for the dependencies. If you ran the report from a right-click context menu item for client, site, or agent, the dependency will auto-populate in the report.

Dependencies are actually merged into the variables behind the scenes, so any properties on the dependency are available to the template to use.

#### Built-in dependencies

You can access the built-in dependencies directly in the template using `{{client.name}}`, `{{agent.hostname}}`, etc.

#### Custom dependencies

You can type in custom dependencies in the dropdown to prompt for other information at report runtime. Custom dependencies only support string values at this time and are referenced in the template using `{{ custom_dependency_name }}`.

#### Using Template Dependencies in variables

You can use dependencies in data queries to filter data. See the Data Queries section above.

You can also use dependencies in the variables section. The syntax is still the same as using them in the template, but you need to make sure that the `{{}}` is surrounded with quotes.

Example with client and a custom_dep dependency:

```yaml
title: '{{client.name}} Summary'
dependency: '{{custom_dep}} some value'
```

### Variable Analysis

If you want to see what your data will look like and how to use it in your template, you can click on the `>` icon on the top-left of the editor windows. (Under the Template Name field). This will run the report template variables server-side and send the results back. This is really useful for data queries and other dynamic information that isn't immediately apparent.

You can also click on the property to copy the template tag to the clipboard. There is also a button for arrays to generate a for loop. You can click on the loop button and it will put the text in the clipboard to be pasted into the template.

If you are using dependencies, you will need to click on the Preview tab and fill in the dependencies before the variables analysis will run.

### Python Modules Available in Template

#### datetime

See the Python datetime documentation for all properties and functions.

Formatted dates use `strftime`:

```py
{{ datetime.datetime.fromtimestamp(item.boot_time, ZoneInfo('America/New_York')).strftime('%Y-%m-%d %H:%M:%S') }}
```

##### datetime.datetime

Example usage in template:

`{{ datetime.datetime.now() }}`

##### datetime.date

Example usage in template:

`{{ datetime.date.today() }}`

##### datetime.timedelta

Example usage in template:

`{{ datetime.datetime.now() - datetime.timedelta(days=30) }}`

#### re

See the Python re module documentation for all properties and functions.

Example usage in template:

```
{% set matches = re.search('this', 'inthisstring') %}
{{matches}}
```

#### ZoneInfo

See the Python zoneinfo documentation for all properties and functions.

Example usage in template:

```
{% for item in data_sources.agentsList %}
    {% set pst_zone = ZoneInfo('America/Los_Angeles') %}
    {% set last_seen_pst = item.last_seen.astimezone(pst_zone) %}
    Last seen in PST: {{ last_seen_pst.strftime('%Y-%m-%d %H:%M:%S %Z') }}
{% endfor %}
```

### Custom Jinja Filters

In addition to the builtin Jinja filters, TRMM also ships with custom Jinja filters. Custom filters can be requested via the developers in Discord or on GitHub. The list of custom Jinja filters can be found in the TRMM source code at `api/tacticalrmm/ee/reporting/custom_filters.py`.

Available custom filters include:

- **as_tz** - Convert timestamps to a specific timezone
- **local_ips** - Extract local IP addresses

### Custom Processors

Custom processors are provided to the YAML parser and allow shortcuts or provide functionality that isn't possible using the template and variables alone.

#### !now

Provides a timestamp at the report runtime.

Example:

```yaml
report_run_timestamp: !now
```

You can also get a timestamp in the future or the past by passing a parameter. The supported time intervals are:

* weeks
* days
* hours
* minutes
* seconds
* microseconds

If you want a timestamp in the future 5 days you would do:

```yaml
five_days_from_now: !now days=5
```

If you want a timestamp 4 hours in the past you would do:

```yaml
four_hours_ago: !now hours=-4
```

You can also specify a value from a dependency.

Note: The `!now` must be outside of the quotes.

```yaml
last_seen_time: !now 'hours=-{{last_seen}}'
```

If we ran the report and put in 5 it would output:

```yaml
last_seen_time: !!now 'hours=-5'
```

---

## Report Assets

The Reports Manager gives the ability to upload and store static assets for use in any report. These can be used in HTML or PDF reports.

In Report Templates, report assets are referenced by their unique ID so they can be renamed and moved without messing up the links.

### Managing Assets

Open **Reports Manager** and click on the **Report Assets** button at the top. This will take you to the root of the reporting assets directory. You can drill into folders by double-clicking and there is a right-click menu to perform other operations.

#### Adding folders

Navigate to the directory you want to create the folder. Use the **Add Folder** button at the top and give the folder a name. The folder will show up in the list.

#### Uploading assets

Navigate to the directory you want to upload the file(s). Click on the **Upload** button at the top and a dialog will open. You can specify multiple assets and click Upload. If there is a name conflict, a set of random characters will be appended.

#### Downloading assets

Use the right-click menu item to download report assets. If you download a folder it will zip it prior to download. Downloading a file will download the file without zipping.

#### Deleting assets

There are two ways to delete assets. You can use the right-click menu to select a folder or asset to delete. This will remove the folder and anything under it.

There is also a bulk delete option by selecting multiple items. Select all of the items you want to delete and click the **Bulk Actions** button. Select **Delete** and confirm.

#### Renaming assets

Use the right-click menu to rename folders or files. If there is a name conflict, a set of random characters will be appended.

### Using Assets in Report Templates

In the Report Template editor, click on the **Image** button on the toolbar. Select the **Report Assets** radio button and browse to the asset you want to add. Select it and press insert. This will add a link with a URL that looks something like `asset://{uuid}`. The reporting engine will resolve this URL to the asset and generate an appropriate URL based on if the report output format is HTML or PDF.

---

## Example Reports

### Agent Uptime

1. Import the `Agent Uptime_By Client (html)` report from the Shared Templates Report library
2. Check at least one overdue item in agent settings
3. Run report and enjoy!

### Windows 11 Upgrade Compatible List

To get a Windows 10 upgrade to Windows 11 compatibility list you'll want to:

1. Create an agent custom field (see the Custom Fields section in references/scripting-and-variables.md)
2. Create an automation policy that applies to all your workstations (see the Automation Policies section in references/checks-tasks-policies.md)
3. Import one of the `Windows 11 Compatible` Reports
4. Enjoy!

### Antivirus Report

To get a report of the active Antivirus on an agent you'll want to:

1. Create an agent custom field (see the Custom Fields section in references/scripting-and-variables.md)
2. Clone `Antivirus - Verify Status` Community script and add the `-customField` Script arg (see the Scripting section in references/scripting-and-variables.md)
3. Create an automation policy that applies to all your workstations (see the Automation Policies section in references/checks-tasks-policies.md)
4. Import one of the `Antivirus` Reports
5. Enjoy!

### NOC Dashboard

Got a TV? Load it up for the team!

Want quick searchable agent status with more data? Load it locally!

The `Restrict Summary` button is for only showing agents that are offline and have an overdue alert set (e.g. critical machines). If it's on a hands-off device make sure you set the refresh every so it's reloading data regularly.

### Software Inventory

`Software Inventory_By Software Name` - Search for software, sort by different columns.

`Software Report - Advanced DataTables` - Advanced software reporting with DataTables integration.

---

## Tips and Tricks

### Formatting Matters

Make sure your tabs are at the right level. Incorrect indentation in YAML variables will cause errors.

### Quickly Generate Reports from Client/Site Tree

Right click on a client or site to quickly run/download a report.

### Change PDF Orientation to Landscape

PDF reports can be set to landscape orientation. See the TRMM documentation or video tutorials for step-by-step instructions.

### Making API Calls from Within a Report Template

If you plan to make API calls (e.g., using axios or fetch) from within a report template, you need to configure additional settings to ensure proper functionality.

Append the following code to `/rmm/api/tacticalrmm/tacticalrmm/local_settings.py`:

```python
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = (
  *default_headers,
  "x-api-key",
)
```

Then restart the rmm service:

```bash
sudo systemctl restart rmm
```

For more details on the TRMM API, see the API section in references/api.md.

---

## Reporting FAQ

### Pricing

Existing sponsors as of Oct 31, 2023: As a thank you for all your support and patience, you will get the Founders Edition perpetual reporting license which will be included in your existing sponsorship. To enable reporting, simply update your instance as you normally do and reporting will automatically be enabled.

For all others, Reporting will be included for all Tier 2 and higher packages. Exceptions will be made for Non-Profits who will only require Tier 1.

### How Do I Enable Reporting as a New Sponsor?

1. Make sure your server has an appropriate code signing token saved (Settings > Code Signing).

2. Run the update script with the `--force` flag (see instructions below for standard vs docker installs).

3. Hard reload the web page. Make sure you use your browser's reload button to hard reload the page.

**Standard install:**

```bash
cd ~
wget -N https://raw.githubusercontent.com/amidaware/tacticalrmm/master/update.sh
chmod +x update.sh
./update.sh --force
```

**Docker install:**

```bash
docker compose down
docker compose up -d
```

If there's a problem, open a ticket at support.amidaware.com.

### How Do I Add Charts/Graphs to My Report Templates?

A bug was discovered with the chart/graph implementation right before release and it had to be pulled. It will be released in a future update.
