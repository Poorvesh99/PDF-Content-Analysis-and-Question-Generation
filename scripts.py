import fitz
import json
import os
from huggingface_hub import InferenceClient
import base64
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()
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
    model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
    client = InferenceClient(model=model_id)
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    question_file = {}

    for page_num, page in enumerate(data):
        images = []

        for image in page['images']:
            with open(image, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
            images.append(img_b64)

        payload = {
            "inputs": (f"""
        <image>{images[0] if len(images)>0 else " "}</image>\n\n"
        Based on the image and the text below, generate one multiple-choice question for a Grade 1 student.

        Text: {page['text']}

        Return your answer in JSON format like:
        {{"question": "...","options": ["A", "B", "C", "D"],"answer": "B"}}
        Begin your final answer with FINAL ANSWER:.
        Don't include anthing but only answer
        """)}
        attempt = 0
        while attempt < 4:
            try:
                # retriving context from image
                response = client.post(json=payload)
            except:
                attempt += 1

        # creating question based on context
        messages = [
            ("system",
             "Create a question from human input in format like:{'question': '...','options': ['A', 'B', 'C', 'D'],'answer': 'B'}"),
            ("human", json.loads(response.decode("utf-8"))[-1].get('generated_text')),
        ]

        result = model.invoke(messages)
        try:
            question_file[page_num] = json.loads(result.content[14:])
        except:
            print(result.content[14:])
            continue
        print(result.content[14:])

    with open('questions.json', 'w') as f:
        json.dump(question_file, f, indent=4)
    print('file_created')