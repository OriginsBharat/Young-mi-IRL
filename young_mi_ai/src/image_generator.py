import aiohttp
import logging
import json

class ImageGenerator:
    def __init__(self, config):
        self.api_url = config.get('comfyui_api_url')
        self.session = aiohttp.ClientSession()

    async def generate_image(self, prompt):
        """
        Sends a prompt to the ComfyUI API to generate an image.
        This function assumes a very basic 'text-to-image' workflow is loaded in ComfyUI.
        You will need to adapt the 'api_format.json' file to match your specific workflow.
        """
        if not self.api_url:
            logging.error("ComfyUI API URL is not configured.")
            return None

        try:
            # Load the ComfyUI API workflow format from a file
            with open('comfyui_workflow.json', 'r') as f:
                workflow = json.load(f)
        except FileNotFoundError:
            logging.error("comfyui_workflow.json not found. This file is required to structure the API request for ComfyUI.")
            return None
        except json.JSONDecodeError:
            logging.error("Error decoding comfyui_workflow.json. Please ensure it is valid JSON.")
            return None

        # Inject the user's prompt into the correct node in the workflow
        # This part is highly dependent on your ComfyUI workflow.
        # You must find the ID of your 'positive prompt' node and set it here.
        # For this example, we assume the positive prompt node is ID "6".
        try:
            positive_prompt_node = workflow.get("6") # Check your workflow for the correct ID
            if positive_prompt_node:
                positive_prompt_node["inputs"]["text"] = prompt
            else:
                logging.error("Could not find the positive prompt node (ID 6) in your comfyui_workflow.json.")
                return None
        except KeyError:
            logging.error("The node with ID 6 in your comfyui_workflow.json is malformed.")
            return None

        payload = {"prompt": workflow}

        try:
            logging.info(f"Sending image generation request to ComfyUI for prompt: {prompt}")
            async with self.session.post(f"{self.api_url}/prompt", json=payload) as response:
                if response.status == 200:
                    # ComfyUI is async, so we need to fetch the result
                    # For simplicity, we are not implementing the full websocket logic here.
                    # This is a fire-and-forget approach. The image will be generated in ComfyUI.
                    # A more advanced implementation would listen for the 'executed' event.
                    logging.info("Image generation task submitted to ComfyUI successfully.")
                    # In a real app, you would need to get the image name from the response
                    # and then fetch it from the /view endpoint.
                    # This is a simplified placeholder.
                    return "I've started making an image for you, babe. It should appear in ComfyUI's output folder."
                else:
                    error_text = await response.text()
                    logging.error(f"Error from ComfyUI API: {response.status} - {error_text}")
                    return "I tried to make an image, but something went wrong with the art tablet..."

        except aiohttp.ClientConnectorError as e:
            logging.error(f"Could not connect to ComfyUI API at {self.api_url}. Is it running? Error: {e}")
            return "I can't connect to my art tools right now. Is ComfyUI running?"
        except Exception as e:
            logging.error(f"An unexpected error occurred while contacting ComfyUI: {e}")
            return "Something went wrong while I was trying to draw..."

    async def close_session(self):
        """Closes the aiohttp session."""
        await self.session.close()