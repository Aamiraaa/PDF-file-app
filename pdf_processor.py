import requests
import json

class PDFProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ilovepdf.com/v1/"

    def _get_auth_headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    def _send_request(self, endpoint, params=None, method="POST"):
        url = self.base_url + endpoint
        headers = self._get_auth_headers()

        if method == "POST":
            response = requests.post(url, headers=headers, json=params)
        elif method == "GET":
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None

    def combine_pdfs(self, file_ids, output_filename):
        endpoint = "merge"
        params = {"files": file_ids, "outputfilename": output_filename}
        response = self._send_request(endpoint, params)
        if response:
            return response["server_filename"]
        return None

    def split_pdf(self, file_id):
        endpoint = f"split/{file_id}"
        response = self._send_request(endpoint, method="GET")
        return response

    def remove_password(self, file_id, output_filename):
        endpoint = "unlock"
        params = {"file": file_id, "outputfilename": output_filename}
        response = self._send_request(endpoint, params)
        if response:
            return response["server_filename"]
        return None

    def extract_text(self, file_id, output_filename):
        endpoint = "extract/text"
        params = {"file": file_id, "outputfilename": output_filename}
        response = self._send_request(endpoint, params)
        if response:
            return response["server_filename"]
        return None

    def image_to_pdf(self, image_files, output_filename):
        endpoint = "image/pdf"
        params = {"files": image_files, "outputfilename": output_filename}
        response = self._send_request(endpoint, params)
        if response:
            return response["server_filename"]
        return None

def main():
    # Load the API key from creds.json
    with open("creds.json.txt", "r") as creds_file:
        creds = json.load(creds_file)
        api_key = creds["api_key"]

    pdf_processor = PDFProcessor(api_key)

    while True:
        print("\nSelect an option:")
        print("1. Combine PDFs")
        print("2. Split PDF")
        print("3. Remove PDF Password")
        print("4. Extract Text from PDF")
        print("5. Convert Images to PDF")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Combine PDFs
            file_ids = input("Enter the file IDs to combine (comma-separated): ").split(",")
            output_filename = input("Enter the output filename: ")
            pdf_processor.combine_pdfs(file_ids, output_filename)

        elif choice == "2":
            # Split PDF
            file_id = input("Enter the file ID to split: ")
            pdf_processor.split_pdf(file_id)

        elif choice == "3":
            # Remove PDF Password
            file_id = input("Enter the file ID to remove the password: ")
            output_filename = input("Enter the output filename: ")
            pdf_processor.remove_password(file_id, output_filename)

        elif choice == "4":
            # Extract Text from PDF
            file_id = input("Enter the file ID to extract text: ")
            output_filename = input("Enter the output filename: ")
            pdf_processor.extract_text(file_id, output_filename)

        elif choice == "5":
            # Convert Images to PDF
            image_files = input("Enter the image file paths to convert (comma-separated): ").split(",")
            output_filename = input("Enter the output filename: ")
            pdf_processor.image_to_pdf(image_files, output_filename)

        elif choice == "6":
            # Exit the application
            break

if __name__ == "__main__":
    main()
