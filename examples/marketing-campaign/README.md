# Marketing Campaign Manager

The Marketing Campaign Manager is a demonstration AI agent developed with LangGraph, designed to assist in composing and sending emails for a marketing campaign.

It performs the following actions:
* It gathers necessary campaign details from the user through a chat.
* Compose an email leveraging the [Email Composer Agent](../mailcomposer/) as a remote ACP agent.
* It leverages the [IO Mapper Agent](https://github.com/agntcy/iomapper-agnt) to adapt Email Composer Agent output to Email Reviewer Agent.
* Reviews the email leveraging the [Email Reviewer Agent](../email_reviewer/) as a remote ACP agent.
* Send the email to the configured recipient through Twilio sendgrid levaraging the [API Bridge Agent](https://github.com/agntcy/api-bridge-agnt)

## Prerequisites

Before running the application, ensure you have the following:

- **Azure OpenAI API Key**
- **Python 3.9 or higher**
- **Poetry**

## Running the Marketing Campaign Manager

### Preliminary step: Deploying API Bridge Agent

Run the API Bridge Agent configured with sendgrid. See [instructions](https://docs.agntcy.org/pages/syntactic_sdk/api_bridge_agent.html#an-example-with-sendgrid-api)


### Running the agent directly
* Deploy agentic dependencies first:
    * Run Email Composer Agent through the Agent Workflow Server. See [instructions](../mailcomposer/README.md#running-the-email-agent-using-agent-workflow-server).
    * Run Email Reviewer Agent through the Agent Workflow Server. See [instructions](../email_reviewer/README.md#running-the-email-agent-using-agent-workflow-server).
* Install python dependencies  
    ```
    poetry install
    ```
* Run the agent
    ```
    export AZURE_OPENAI_MODEL=gpt-4o-mini
    export AZURE_OPENAI_API_KEY=***YOUR_OPENAI_API_KEY***
    export AZURE_OPENAI_ENDPOINT=***YOUR_OPENAI_ENDPOINT***
    export OPENAI_API_VERSION=2024-07-01-preview 
    export SENDGRID_API_KEY=***YOUR_SENDGRID_API_KEY***
    export MAILCOMPOSER_HOST=***URL TO EMAIL COMPOSER WORKFLOW SERVER e.g. http://0.0.0.0:10100***
    export EMAIL_REVIEWER_HOST=***URL TO EMAIL REVIEWER WORKFLOW SERVER e.g. http://0.0.0.0:10100***
    export MAILCOMPOSER_AGENT_ID==***EMAIL COMPOSER ID**
    export EMAIL_REVIEWER_AGENT_ID=***EMAIL REVIEWER ID**
    export SENDGRID_HOST=***URL TO API BRIDGE AGENT*** 
    
    poetry run python src/marketing_campaign/__main__.py
    ```

## Running the Email Agent using Agent Workflow Server

* Create an environment variable file with the variables described above
    ```commandline
    echo "
    AZURE_OPENAI_MODEL=gpt-4o-mini
    ...
    ...
    " > deploy/.mcm.env
    ```
* Make sure that the workflow server manager cli (`wfsm`) is added to your path
* Start the workflow server
    ```
    cd deploy;
    wfsm deploy -m ./mailcomposer.json -e ./.mcm.env
    ```


