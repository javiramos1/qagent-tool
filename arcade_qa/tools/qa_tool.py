"""
Arcade.dev tool for Domain Q&A Agent
"""

import base64
import json
import logging
import zlib
from typing import Annotated
from arcade.sdk import tool, ToolContext

from .qagent import DomainQAAgent

logger = logging.getLogger(__name__)

@tool(requires_secrets=["ARCADE_API_KEY", "GOOGLE_API_KEY", "SITES_CONFIG"])
async def qa_chat(
    context: ToolContext,
    user_input: Annotated[str, "The question or input from the user"],
    llm_temperature: Annotated[float, "Temperature for the LLM (0.0 to 1.0)"] = 0.0,
    llm_max_tokens: Annotated[int, "Maximum tokens for LLM response"] = 2048,
    llm_timeout: Annotated[int, "Timeout for LLM requests in seconds"] = 60,
    max_search_results: Annotated[int, "Maximum number of search results to return"] = 5,
) -> Annotated[str, "The agent's response to the user's question"]:
    """
    Chat with a domain-specific Q&A agent that searches specific documentation websites.
    
    This tool creates a Q&A agent that can search and answer questions based on 
    predefined knowledge sources defined in a CSV file. The agent uses Google search
    and web scraping through Arcade.dev tools to find relevant information.
    
    Examples:
        qa_chat("How do I create a LangChain agent?")
        qa_chat("What are the best practices for prompt engineering?", max_search_results=5)
    """

    try:
        logger.info(f"Processing qa_chat request: {user_input[:100]}...")
        
        # Get secrets from context
        arcade_api_key = context.get_secret("ARCADE_API_KEY")
        google_api_key = context.get_secret("GOOGLE_API_KEY")
        sites_config_compressed = context.get_secret("SITES_CONFIG")
        
        # Create configuration hash for caching
        config_key = f"{llm_temperature}_{llm_max_tokens}_{llm_timeout}_{max_search_results}"
        
        # Check if agent is already cached in context
        cached_agent = getattr(context, f'_cached_agent_{config_key}', None)
        cached_sites_config = getattr(context, '_cached_sites_config_hash', None)
        
        # Create a simple hash of the compressed config to detect changes
        current_sites_config_hash = hash(sites_config_compressed)
        
        if cached_agent is not None and cached_sites_config == current_sites_config_hash:
            logger.info(f"Using cached agent instance with config: {config_key}")
            agent = cached_agent
        else:
            logger.info("Creating new agent instance...")
            
            # Decompress sites data if needed
            sites_data = getattr(context, '_cached_sites_data', None)
            if sites_data is None or cached_sites_config != current_sites_config_hash:
                logger.info("Decompressing sites configuration data...")
                # Decompress the sites configuration
                # Decode the base64 string back to bytes
                decoded_compressed_data = base64.b64decode(sites_config_compressed)
                # Decompress the bytes
                decompressed_bytes = zlib.decompress(decoded_compressed_data)
                # Parse the JSON
                sites_data = json.loads(decompressed_bytes.decode('utf-8'))
                
                # Cache the decompressed data in context
                context._cached_sites_data = sites_data
                context._cached_sites_config_hash = current_sites_config_hash
                logger.info(f"Sites data decompressed and cached. Found {len(sites_data)} sites.")
            else:
                logger.info(f"Using cached sites data with {len(sites_data)} sites.")
            
            # Create configuration
            config = {
                "arcade_api_key": arcade_api_key,
                "google_api_key": google_api_key,
                "llm_temperature": llm_temperature,
                "llm_max_tokens": llm_max_tokens,
                "llm_timeout": llm_timeout,
                "max_search_results": max_search_results,
            }
            
            logger.info(f"Initializing DomainQAAgent with config: temperature={llm_temperature}, max_tokens={llm_max_tokens}, max_search_results={max_search_results}")
            
            # Initialize the domain Q&A agent
            agent = DomainQAAgent(sites_data=sites_data, config=config)
            
            # Cache the agent instance
            setattr(context, f'_cached_agent_{config_key}', agent)
            logger.info("Agent instance cached for future use.")

        # Process the user input and get response
        logger.info("Processing user input with agent...")
        response = await agent.achat(user_input)
        
        logger.info(f"Agent response generated successfully. Response length: {len(response)} characters")
        return response
        
    except Exception as e:
        error_msg = f"Error in qa_chat: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg
