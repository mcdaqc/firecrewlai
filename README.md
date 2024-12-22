# Multi-Agent System for Local Code Execution

A multi-agent system capable of developing functional applications. The system employs multiple specialized agents to handle different aspects of application development, from requirement gathering to code generation and testing.

## Key Features

- 🤖 Multiple specialized agents working in coordination
- 🕷️ Advanced Web Scraping with Firecrawl
- 🧠 NVIDIA NeMo integration for advanced language processing
- 🔒 Secure code execution in isolated Docker environments
- 📊 AstraDB integration for data persistence and RAG capabilities
- 🔍 Vector-based search for similar code patterns
- 🔄 Automated error recovery and code regeneration

## Architecture

The system uses a multi-agent architecture where each agent has a specific role:

1. **Requirement Collector**: Processes and structures user requirements
2. **Code Generator**: Creates code based on requirements and examples
3. **Validator**: Tests and validates generated code
4. **Coordinator**: Manages workflow and agent communication

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- NVIDIA GPU/API
- AstraDB account and API credentials
- Firecrawl API key
- NVIDIA API key
