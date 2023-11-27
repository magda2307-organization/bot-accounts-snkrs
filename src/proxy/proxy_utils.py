def read_proxies_from_file(file_path="proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
        return proxies
    except Exception as e:
        raise ValueError(f"Error reading proxies file: {e}")

def get_proxy_for_item(item, proxies, last_used_proxy_index):
    if not proxies:
        return None

    last_used_proxy_index = (last_used_proxy_index + 1) % len(proxies)
    return proxies[last_used_proxy_index]
