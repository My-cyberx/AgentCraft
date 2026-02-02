# AgentCraft

A collection of reusable agent prompts for GitHub Copilot and other AI assistants.

## Available Prompts

### 🔍 Template Variable Extraction Agent
**Location:** `prompts/template-variable-agent.md`

Extract configurable variables from template/theme repositories (e.g., Shopify themes, HTML templates) to make them reusable across multiple projects.

**Use case:** When you have a template repository with hard-coded values (brand names, colors, contact info, etc.) and want to identify all values that should be configurable.

**How to use:**
1. Open your template/theme repository in your IDE
2. Open GitHub Copilot Chat
3. Copy-paste the content of `prompts/template-variable-agent.md` into the chat
4. The agent will scan your repository and produce a structured JSON config schema with all discovered variables

## Usage

Each prompt in the `prompts/` directory is a self-contained markdown file that can be copy-pasted into GitHub Copilot Chat or other AI assistants. Follow the instructions in each prompt file for specific usage details.

## Contributing

Feel free to add more agent prompts to this collection. Each prompt should:
- Be a complete, self-contained instruction set
- Include clear usage instructions
- Specify expected inputs and outputs
- Be saved as a markdown file in the `prompts/` directory