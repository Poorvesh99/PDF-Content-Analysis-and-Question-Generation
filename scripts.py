import fitz
import json
import os
from huggingface_hub import InferenceClient



def extract_content_from_pdf(pdf_path: str) -> list:
    """
    extract text and image from given pdf
    :param pdf_path: str having path to pdf
    :return: extracted information in list having json object for every page
    """
    doc = fitz.open(pdf_path)
    os.makedirs("extracted_images", exist_ok=True)

    total_text = []
    output = []
    page_num = 0
    for page in doc:
        # extract and store text
        text = page.get_text().encode("utf8")
        total_text.append(text)

        # extract and save images
        image_list = page.get_images(full=True)
        image_paths = []

        for img_index, img in enumerate(image_list[1:]):  # form 2nd index due to redundunt image
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"extracted_images/page{page_num + 1}_image{img_index + 1}.{image_ext}"

            # Save image
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_path)

        page_num += 1

        # creates page output
        page_content = {
            "page": page_num + 1,
            "text": str(text.strip()),
            "images": image_paths
        }
        # attach to final_output
        output.append(page_content)

        # save final_output
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        print("Extraction is Done!")

        return output


def generate_questions(data:list):
    model_id = "Qwen/Qwen2.5-VL-72B-Instruct"
    client = InferenceClient(model=model_id)

    for page in data:



        # Prepare your image (must be a URL or base64-encoded data)
        image_url = "https://example.com/your-image.jpg"

        payload = {
            "inputs": "Describe what's happening in the image.",
            "parameters": {"image": image_url}
        }

        response = client.post(json=payload)
