import multiprocessing
import requests

request_url = "https://server.atomicalmarket.com/mainnet/v1/atommap/block/"
max_retry = 3


def split_range_into_chunks(start, end, chunk_size):
    chunks = []
    for i in range(start, end, chunk_size):
        chunk_start = i
        chunk_end = min(i + chunk_size, end)
        chunks.append((chunk_start, chunk_end))
    return chunks


def worker_function(start, end):
    print(f"{start}:{end}")
    result = []
    for num in range(start, end):
        retry = 0
        while True:
            try:
                if retry >= max_retry:
                    break
                response = requests.get(request_url + str(num))
                if response.status_code == 200:
                    print(response.json())
                    mint_data = response.json()['isError']
                    if mint_data:
                        result.append(num)
                        break
                else:
                    print(f"Request failed with status code {response.status_code}:{response.text}")
                    retry = retry + 1
            except Exception as e:
                retry = retry + 1
                print(e)
    return result


def handler(start, end, num_processes):
    chunk_size = (end - start) // num_processes
    chunks = split_range_into_chunks(start, end, chunk_size)
    print(chunks)
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.starmap(worker_function, chunks)
    merged_array = []
    for arr in results:
        merged_array.extend(arr)
    with open('output.txt', 'w') as file:
        for item in merged_array:
            file.write(str(item) + "\n")


if __name__ == '__main__':
    handler(4000, 5000, 128)
