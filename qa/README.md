<div style="display: flex; justify-content: center; align-items: center;">
  <img
    src="https://docs.arcade.dev/images/logo/arcade-logo.png"
    style="width: 250px;"
  >
</div>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
  <img src="https://img.shields.io/github/v/release/javiramos1/qa" alt="GitHub release" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" style="margin: 0 2px;">
  <img src="https://img.shields.io/pypi/v/arcade_qa" alt="PyPI version" style="margin: 0 2px;">
</div>
<div style="display: flex; justify-content: center; align-items: center;">
  <a href="https://github.com/javiramos1/qa" target="_blank">
    <img src="https://img.shields.io/github/stars/javiramos1/qa" alt="GitHub stars" style="margin: 0 2px;">
  </a>
  <a href="https://github.com/javiramos1/qa/fork" target="_blank">
    <img src="https://img.shields.io/github/forks/javiramos1/qa" alt="GitHub forks" style="margin: 0 2px;">
  </a>
</div>

<br>
<br>

# Arcade Q&A Toolkit

A domain-specific Q&A agent tool built with [Arcade.dev](https://arcade.dev) that intelligently searches predefined documentation websites to answer questions about specific technologies and frameworks.

## Overview

This toolkit provides a powerful Q&A agent that:
- **Searches specific documentation domains** using Google Search with site restrictions
- **Scrapes web content** when search results need more detail
- **Uses Google Gemini** for intelligent question processing and response generation
- **Leverages Arcade.dev tools** for web search and scraping capabilities
- **Supports configurable knowledge sources** through compressed JSON configuration

## Features

- 🔍 **Smart Documentation Search**: Automatically searches relevant documentation sites based on question context
- 🌐 **Web Scraping Integration**: Falls back to scraping when search results are insufficient
- 🤖 **AI-Powered Responses**: Uses Google Gemini 2.0 Flash for intelligent question understanding and response generation
- ⚡ **Arcade.dev Integration**: Built as an Arcade.dev tool for easy deployment and scaling
- 🔧 **Configurable**: Supports custom knowledge sources and LLM parameters
- 💾 **Intelligent Caching**: Caches agent instances and decompressed configuration for performance

## Architecture

The toolkit consists of two main components:

### 1. DomainQAAgent (`qagent.py`)
A sophisticated agent that:
- Creates structured chat agents using LangChain
- Integrates Google Search and web scraping tools from Arcade.dev
- Manages domain-specific knowledge sources
- Provides async chat functionality

### 2. Arcade.dev Tool (`qa_tool.py`)
An Arcade.dev tool that:
- Exposes the Q&A agent as a callable tool
- Handles secret management (API keys, configuration)
- Implements intelligent caching for performance
- Manages compressed configuration data

## Installation

### For End Users

Install this toolkit using pip:

```bash
pip install arcade_qa
```

### For Development

If you want to contribute or develop with this toolkit, clone the repository and use the provided Make commands:

```bash
# Clone the repository
git clone https://github.com/javiramos1/qa.git
cd qa

# Install development environment with Poetry
make install

# View all available commands
make help
```

#### Available Make Commands

- `make install` - Install the poetry environment and install the pre-commit hooks
- `make build` - Build wheel file using poetry
- `make test` - Test the code with pytest
- `make coverage` - Generate coverage report
- `make check` - Run code quality tools (linting, type checking)
- `make bump-version` - Bump the version in the pyproject.toml file
- `make clean-build` - Clean build artifacts

## Usage

### As an Arcade.dev Tool

The primary way to use this toolkit is through Arcade.dev:

```python
from langchain_arcade import ArcadeToolManager

# Initialize Arcade tool manager
manager = ArcadeToolManager(api_key="your_arcade_api_key")

# Load the Q&A tool
tools = manager.init_tools(tools=["arcade_qa.qa_chat"])

# Use the tool
response = await tools[0].arun("How do I create a LangChain agent?")
print(response)
```

### Direct Usage

You can also use the agent directly:

```python
from arcade_qa.tools.qagent import DomainQAAgent

# Define your knowledge sources
sites_data = [
    {
        "site": "LangChain Documentation",
        "domain": "python.langchain.com",
        "description": "Official LangChain documentation"
    },
    # ... more sites
]

# Configuration
config = {
    "arcade_api_key": "your_arcade_api_key",
    "google_api_key": "your_google_api_key",
    "llm_temperature": 0.0,
    "llm_max_tokens": 2048,
    "llm_timeout": 60,
    "max_search_results": 5
}

# Create and use the agent
agent = DomainQAAgent(sites_data=sites_data, config=config)
response = await agent.achat("How do I create a LangChain agent?")
print(response)
```

## Configuration

### Required Secrets (for Arcade.dev deployment)

- `ARCADE_API_KEY`: Your Arcade.dev API key
- `GOOGLE_API_KEY`: Google AI Studio API key for Gemini models
- `SITES_CONFIG`: Compressed JSON configuration of knowledge sources

### Knowledge Sources Format

The knowledge sources should be provided as a list of dictionaries:

```json
[
    {
        "site": "LangChain Documentation",
        "domain": "python.langchain.com",
        "description": "Official LangChain Python documentation"
    },
    {
        "site": "LangChain JS Documentation", 
        "domain": "js.langchain.com",
        "description": "Official LangChain JavaScript documentation"
    }
]
```

### Tool Parameters

- `user_input` (str): The question or input from the user
- `llm_temperature` (float, default: 0.0): Temperature for the LLM (0.0 to 1.0)
- `llm_max_tokens` (int, default: 2048): Maximum tokens for LLM response
- `llm_timeout` (int, default: 60): Timeout for LLM requests in seconds
- `max_search_results` (int, default: 5): Maximum number of search results to return

## How It Works

1. **Question Analysis**: The agent analyzes the user's question to determine relevant domains/topics
2. **Targeted Search**: Uses Google Search with `site:` operators to search only within specified documentation domains
3. **Smart Scraping**: If search results are insufficient, scrapes the most relevant URL for detailed content
4. **AI Response**: Uses Google Gemini to generate comprehensive, well-sourced answers

## Example Workflow

```
User: "How do I create a LangChain agent?"

1. Agent searches: "LangChain agents site:python.langchain.com"
2. Finds relevant documentation pages
3. If needed, scrapes specific pages for detailed examples
4. Generates comprehensive response with code examples and explanations
```

## Deployment

### Deploying to Arcade.dev

To deploy this toolkit as an Arcade.dev tool, follow these steps:

1. **Set up your worker configuration** in `worker.toml`:

```toml
[[worker]]

[worker.config]
id = "qa-worker"
enabled = true
timeout = 90
retries = 3
secret = "your_secret_key_here"

[worker.local_source]
packages = ["./qa"]
```

2. **Configure your secrets** by adding them to your Arcade.dev account:
   - `ARCADE_API_KEY`: Your Arcade.dev API key
   - `GOOGLE_API_KEY`: Google AI Studio API key for Gemini models
   - `SITES_CONFIG`: Compressed JSON configuration of your knowledge sources

3. **Deploy the tool**:

```bash
# Install the Arcade CLI if you haven't already
pip install arcade-ai

# Deploy your tool
arcade deploy
```

4. **Test your deployment**:

```python
from langchain_arcade import ArcadeToolManager

# Initialize with your deployed tool
manager = ArcadeToolManager(api_key="your_arcade_api_key")
tools = manager.init_tools(tools=["your_username.qa_chat"])

# Test the tool
response = await tools[0].arun("How do I create a LangChain agent?")
print(response)
```

For more detailed deployment instructions, see:
- [Create a Toolkit Guide](https://docs.arcade.dev/home/build-tools/create-a-toolkit)
- [Arcade Deploy Documentation](https://docs.arcade.dev/home/local-deployment/configure/arcade-deploy)

## Development

### Project Structure

```
arcade_qa/
├── tools/
│   ├── qagent.py          # Main Q&A agent implementation
│   └── qa_tool.py         # Arcade.dev tool wrapper
└── README.md
```

### Key Dependencies

- `langchain`: For agent orchestration and prompt management
- `langchain-google-genai`: Google Gemini integration
- `langchain-arcade`: Arcade.dev tools integration
- `arcade-sdk`: Arcade.dev SDK for tool creation

## Contributing

Contributions are welcome! Please ensure your code follows the existing patterns and includes appropriate error handling and logging.

## License

This project is licensed under the MIT License.

## Related Links

- [Arcade.dev Documentation](https://docs.arcade.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://aistudio.google.com/)