import json
import logging
from typing import Any, Dict, List, Tuple

import mcp.types as types


logger = logging.getLogger(__name__)


def get_single_param_type_from_schema(param_schema: Dict[str, Any]) -> str:
    """
    Get the type of a parameter from the schema.
    If the schema is a union type, return the first type.
    """
    if "anyOf" in param_schema:
        types = {schema.get("type") for schema in param_schema["anyOf"] if schema.get("type")}
        if "null" in types:
            types.remove("null")
        if types:
            return next(iter(types))
        return "string"
    return param_schema.get("type", "string")


def resolve_schema_references(schema_part: Dict[str, Any], reference_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolve schema references in OpenAPI schemas.

    Args:
        schema_part: The part of the schema being processed that may contain references
        reference_schema: The complete schema used to resolve references from

    Returns:
        The schema with references resolved
    """
    # Make a copy to avoid modifying the input schema
    schema_part = schema_part.copy()

    # Handle $ref directly in the schema
    if "$ref" in schema_part:
        ref_path = schema_part["$ref"]
        # Standard OpenAPI references are in the format "#/components/schemas/ModelName"
        if ref_path.startswith("#/components/schemas/"):
            model_name = ref_path.split("/")[-1]
            if "components" in reference_schema and "schemas" in reference_schema["components"]:
                if model_name in reference_schema["components"]["schemas"]:
                    # Replace with the resolved schema
                    ref_schema = reference_schema["components"]["schemas"][model_name].copy()
                    # Remove the $ref key and merge with the original schema
                    schema_part.pop("$ref")
                    schema_part.update(ref_schema)

    # Recursively resolve references in all dictionary values
    for key, value in schema_part.items():
        if isinstance(value, dict):
            schema_part[key] = resolve_schema_references(value, reference_schema)
        elif isinstance(value, list):
            # Only process list items that are dictionaries since only they can contain refs
            schema_part[key] = [
                resolve_schema_references(item, reference_schema) if isinstance(item, dict) else item for item in value
            ]

    return schema_part


def clean_schema_for_display(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean up a schema for display by removing internal fields.

    Args:
        schema: The schema to clean

    Returns:
        The cleaned schema
    """
    # Make a copy to avoid modifying the input schema
    schema = schema.copy()

    # Remove common internal fields that are not helpful for LLMs
    fields_to_remove = [
        "allOf",
        "anyOf",
        "oneOf",
        "nullable",
        "discriminator",
        "readOnly",
        "writeOnly",
        "xml",
        "externalDocs",
    ]
    for field in fields_to_remove:
        if field in schema:
            schema.pop(field)

    # Process nested properties
    if "properties" in schema:
        for prop_name, prop_schema in schema["properties"].items():
            if isinstance(prop_schema, dict):
                schema["properties"][prop_name] = clean_schema_for_display(prop_schema)

    # Process array items
    if "type" in schema and schema["type"] == "array" and "items" in schema:
        if isinstance(schema["items"], dict):
            schema["items"] = clean_schema_for_display(schema["items"])

    return schema


def generate_example_from_schema(schema: Dict[str, Any]) -> Any:
    """
    Generate a simple example response from a JSON schema.

    Args:
        schema: The JSON schema to generate an example from

    Returns:
        An example object based on the schema
    """
    if not schema or not isinstance(schema, dict):
        return None

    # Handle different types
    schema_type = schema.get("type")

    if schema_type == "object":
        result = {}
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                # Generate an example for each property
                prop_example = generate_example_from_schema(prop_schema)
                if prop_example is not None:
                    result[prop_name] = prop_example
        return result

    elif schema_type == "array":
        if "items" in schema:
            # Generate a single example item
            item_example = generate_example_from_schema(schema["items"])
            if item_example is not None:
                return [item_example]
        return []

    elif schema_type == "string":
        # Check if there's a format
        format_type = schema.get("format")
        if format_type == "date-time":
            return "2023-01-01T00:00:00Z"
        elif format_type == "date":
            return "2023-01-01"
        elif format_type == "email":
            return "user@example.com"
        elif format_type == "uri":
            return "https://example.com"
        # Use title or property name if available
        return schema.get("title", "string")

    elif schema_type == "integer":
        return 1

    elif schema_type == "number":
        return 1.0

    elif schema_type == "boolean":
        return True

    elif schema_type == "null":
        return None

    # Default case
    return None

def convert_openapi_to_mcp_tools(
    openapi_schema: Dict[str, Any],
    describe_all_responses: bool = False,
    describe_full_response_schema: bool = False,
) -> Tuple[List[types.Tool], Dict[str, Dict[str, Any]]]:
    """
    Convert OpenAPI operations to MCP tools.

    Args:
        openapi_schema: The OpenAPI schema
        describe_all_responses: Whether to include all possible response schemas in tool descriptions
        describe_full_response_schema: Whether to include full response schema in tool descriptions

    Returns:
        A tuple containing:
        - A list of MCP tools
        - A mapping of operation IDs to operation details for HTTP execution
    """
    # Resolve all references in the schema at once
    resolved_openapi_schema = resolve_schema_references(openapi_schema, openapi_schema)

    tools = []
    operation_map = {}

    # Process each path in the OpenAPI schema
    for path, path_item in resolved_openapi_schema.get("paths", {}).items():
        for method, operation in path_item.items():
            # Skip non-HTTP methods
            if method not in ["get", "post", "put", "delete", "patch"]:
                logger.warning(f"Skipping non-HTTP method: {method}")
                continue

            # Get operation metadata
            operation_id = operation.get("operationId")
            if not operation_id:
                logger.warning(f"Skipping operation with no operationId: {operation}")
                continue

            # Save operation details for later HTTP calls
            operation_map[operation_id] = {
                "path": path,
                "method": method,
                "parameters": operation.get("parameters", []),
                "request_body": operation.get("requestBody", {}),
            }

            summary = operation.get("summary", "")
            description = operation.get("description", "")

            # Build tool description
            tool_description = f"{summary}" if summary else f"{method.upper()} {path}"
            if description:
                tool_description += f"\n\n{description}"

            # Add response information to the description
            responses = operation.get("responses", {})
            if responses:
                response_info = "\n\n### Responses:\n"

                # Find the success response
                success_codes = range(200, 300)
                success_response = None
                for status_code in success_codes:
                    if str(status_code) in responses:
                        success_response = responses[str(status_code)]
                        break

                # Get the list of responses to include
                responses_to_include = responses
                if not describe_all_responses and success_response:
                    # If we're not describing all responses, only include the success response
                    success_code = next((code for code in success_codes if str(code) in responses), None)
                    if success_code:
                        responses_to_include = {str(success_code): success_response}

                # Process all selected responses
                for status_code, response_data in responses_to_include.items():
                    response_desc = response_data.get("description", "")
                    response_info += f"\n**{status_code}**: {response_desc}"

                    # Highlight if this is the main success response
                    if response_data == success_response:
                        response_info += " (Success Response)"

                    # Add schema information if available
                    if "content" in response_data:
                        for content_type, content_data in response_data["content"].items():
                            if "schema" in content_data:
                                schema = content_data["schema"]
                                response_info += f"\nContent-Type: {content_type}"

                                # Clean the schema for display
                                display_schema = clean_schema_for_display(schema)

                                # Try to get example response
                                example_response = None

                                # Check if content has examples
                                if "examples" in content_data:
                                    for example_key, example_data in content_data["examples"].items():
                                        if "value" in example_data:
                                            example_response = example_data["value"]
                                            break
                                # If content has example
                                elif "example" in content_data:
                                    example_response = content_data["example"]

                                # If we have an example response, add it to the docs
                                if example_response:
                                    response_info += "\n\n**Example Response:**\n```json\n"
                                    response_info += json.dumps(example_response, indent=2)
                                    response_info += "\n```"
                                # Otherwise generate an example from the schema
                                else:
                                    generated_example = generate_example_from_schema(display_schema)
                                    if generated_example:
                                        response_info += "\n\n**Example Response:**\n```json\n"
                                        response_info += json.dumps(generated_example, indent=2)
                                        response_info += "\n```"

                                # Only include full schema information if requested
                                if describe_full_response_schema:
                                    # Format schema information based on its type
                                    if display_schema.get("type") == "array" and "items" in display_schema:
                                        items_schema = display_schema["items"]

                                        response_info += "\n\n**Output Schema:** Array of items with the following structure:\n```json\n"
                                        response_info += json.dumps(items_schema, indent=2)
                                        response_info += "\n```"
                                    elif "properties" in display_schema:
                                        response_info += "\n\n**Output Schema:**\n```json\n"
                                        response_info += json.dumps(display_schema, indent=2)
                                        response_info += "\n```"
                                    else:
                                        response_info += "\n\n**Output Schema:**\n```json\n"
                                        response_info += json.dumps(display_schema, indent=2)
                                        response_info += "\n```"

                tool_description += response_info

            # Organize parameters by type
            path_params = []
            query_params = []
            header_params = []
            body_params = []

            for param in operation.get("parameters", []):
                param_name = param.get("name")
                param_in = param.get("in")
                required = param.get("required", False)

                if param_in == "path":
                    path_params.append((param_name, param))
                elif param_in == "query":
                    query_params.append((param_name, param))
                elif param_in == "header":
                    header_params.append((param_name, param))

            # Process request body if present
            request_body = operation.get("requestBody", {})
            if request_body and "content" in request_body:
                content_type = next(iter(request_body["content"]), None)
                if content_type and "schema" in request_body["content"][content_type]:
                    schema = request_body["content"][content_type]["schema"]
                    if "properties" in schema:
                        for prop_name, prop_schema in schema["properties"].items():
                            required = prop_name in schema.get("required", [])
                            body_params.append(
                                (
                                    prop_name,
                                    {
                                        "name": prop_name,
                                        "schema": prop_schema,
                                        "required": required,
                                    },
                                )
                            )

            # Create input schema properties for all parameters
            properties = {}
            required_props = []

            # Add path parameters to properties
            for param_name, param in path_params:
                param_schema = param.get("schema", {})
                param_desc = param.get("description", "")
                param_required = param.get("required", True)  # Path params are usually required

                properties[param_name] = {
                    "type": param_schema.get("type", "string"),
                    "title": param_name,
                    "description": param_desc,
                }

                if param_required:
                    required_props.append(param_name)

            # Add query parameters to properties
            for param_name, param in query_params:
                param_schema = param.get("schema", {})
                param_desc = param.get("description", "")
                param_required = param.get("required", False)

                properties[param_name] = {
                    "type": get_single_param_type_from_schema(param_schema),
                    "title": param_name,
                    "description": param_desc,
                }
                if "default" in param_schema:
                    properties[param_name]["default"] = param_schema["default"]

                if param_required:
                    required_props.append(param_name)

            # Add body parameters to properties
            for param_name, param in body_params:
                param_schema = param.get("schema", {})
                param_required = param.get("required", False)

                properties[param_name] = {
                    "type": get_single_param_type_from_schema(param_schema),
                    "title": param_name,
                }
                if "default" in param_schema:
                    properties[param_name]["default"] = param_schema["default"]

                if param_required:
                    required_props.append(param_name)

            # Create a proper input schema for the tool
            input_schema = {"type": "object", "properties": properties, "title": f"{operation_id}Arguments"}

            if required_props:
                input_schema["required"] = required_props

            # Create the MCP tool definition
            tool = types.Tool(name=operation_id, description=tool_description, inputSchema=input_schema)

            tools.append(tool)

    return tools, operation_map
