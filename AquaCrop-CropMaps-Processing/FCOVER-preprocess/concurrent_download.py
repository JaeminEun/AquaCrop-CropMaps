# Jaemin Eun
import concurrent.futures
import requests
import os

# Function to download a file
def download_file(url):
    local_filename = url.split('/')[-1]
    try:
        # Stream the file download
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                    f.write(chunk)
        return f"{local_filename} downloaded"
    except Exception as e:
        return f"Failed to download {url}: {e}"

# Function to read URLs from the file
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

# Main function to handle multiprocessing
def download_files_in_parallel(url_file, num_workers=36):
    urls = read_urls(url_file)

    # Using ThreadPoolExecutor to download files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(download_file, urls))

    # Output the results
    for result in results:
        print(result)

if __name__ == "__main__":
    # Replace with the path to your file containing URLs
    url_file = "urls_CC.txt"

    # Call the function with multiprocessing (default to 36 workers)
    download_files_in_parallel(url_file)

