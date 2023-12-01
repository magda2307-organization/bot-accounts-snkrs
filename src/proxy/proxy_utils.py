def read_proxies_from_file(file_path="config/proxies.txt"):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip().split(':') for line in file.readlines()]
            proxies = [{'ip': proxy[0], 'port': proxy[1], 'username': proxy[2], 'password': proxy[3]} for proxy in proxies]
        return proxies
    except Exception as e:
        raise ValueError(f"Error reading proxies file: {e}")

def get_proxy_for_item(item, proxies, last_used_proxy_index):
    if not proxies:
        return None

    last_used_proxy_index = (last_used_proxy_index + 1) % len(proxies)
    return proxies[last_used_proxy_index]
