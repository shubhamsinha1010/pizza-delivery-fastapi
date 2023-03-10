# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv

load_dotenv()

# Import the Cloudinary libraries
# ==============================
import cloudinary,os
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True
# ==============================
# config = cloudinary.config(secure=True)
config = cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=os.environ.get("CLOUDINARY_SECURE")
)


# Log the configuration
# ==============================
# print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")


def upload_image(image_path,username):
    # Upload the image and get its URL
    # ==============================

    # Upload the image.
    # Set the asset's public ID and allow overwriting the asset with new versions
    cloudinary.uploader.upload(image_path,
                               public_id=f"{username}", unique_filename=False, overwrite=True)

    # Build the URL for the image and save it in the variable 'src_url'
    src_url = cloudinary.CloudinaryImage(f"{username}").build_url()

    # Log the image URL to the console.
    # Copy this URL in a browser tab to generate the image on the fly.
    print("****2. Upload an image****\nDelivery URL: ", src_url, "\n")


def get_asset_info(username):
    # Get and use details of the image
    # ==============================

    # Get image details and save it in the variable 'image_info'.
    image_info = cloudinary.api.resource(f"{username}")
    print("****3. Get and use details of the image****\nUpload response:\n", json.dumps(image_info, indent=2), "\n")

    # Assign tags to the uploaded image based on its width. Save the response to the update in the variable 'update_resp'.
    if image_info["width"] > 900:
        update_resp = cloudinary.api.update(f"{username}", tags="large")
    elif image_info["width"] > 500:
        update_resp = cloudinary.api.update(f"{username}", tags="medium")
    else:
        update_resp = cloudinary.api.update(f"{username}", tags="small")

    # Log the new tag to the console.
    print("New tag: ", update_resp["tags"], "\n")
    return json.dumps(image_info, indent=2)


def create_image_tag(username):
    # Transform the image
    # ==============================

    # Create an image tag with transformations applied to the src URL.
    image_tag = cloudinary.CloudinaryImage(f"{username}").image(radius="max", effect="sepia")

    # Log the image tag to the console
    print("****4. Transform the image****\nTransfrmation URL: ", image_tag, "\n")

