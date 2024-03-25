# import webbrowser

# def website_opener(domain):
#     try:
#         url = 'https://www.' + domain
#         print(f"Trying to open URL: {url}")
#         webbrowser.open(url)
#         return True
#     except webbrowser.Error as e:
#         print(f"Error opening {url}: {e}")
#         return False

import webbrowser

def website_opener(domain):
    try:
        url = 'https://www.' + domain
        print(f"Trying to open URL: {url}")
        webbrowser.open(url)
        return True
    except webbrowser.Error as e:
        print(f"Error opening {url}: {e}")
        return False


# Example usage
# domain_to_open = 'example.com'
# open_result = website_opener(domain_to_open)
# print(open_result)
