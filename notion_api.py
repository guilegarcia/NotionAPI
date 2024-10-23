import requests


class NotionAPI:
    """
    Class to interact with the Notion API.
    """
    NOTION_VERSION = "2022-06-28"

    def __init__(self, token: str):
        """
        Initializes the class with the authentication token and block ID.

        :param token: Notion API authentication token.
        """
        self.token = token
        self.base_url = f"https://api.notion.com/v1/"
        self.headers = {
            "Notion-Version": self.NOTION_VERSION,
            "Authorization": f"Bearer {self.token}"
        }

    def get_page_content(self, page_id):
        """
        Makes a GET request to the Notion API and returns the page content.

        :param page_id: ID of the page.
        :return: Content of the first paragraph of the page, or None if error.
        """
        url = self.base_url + f"blocks/{page_id}/children?page_size=100"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        print(data)
        if data and 'results' in data:
            try:
                return data['results'][0]['paragraph']['rich_text'][0]['text']['content']
            # TODO e se a página tiver conteúdo e subpáginas? possívelmente vai dar erro na extração de subpáginas
            # SOLUÇÃO criar a requisição na própria subpages
            except (KeyError, IndexError):
                print("Não foi possível acessar o conteúdo do bloco.")
                return data
        return None

    def get_child_pages(self, page_id: str):
        """
        Returns the child pages of a Notion page.

        :param page_id: ID of the parent page.
        :return: List of child pages.
        """
        data = self.get_page_content(page_id)
        child_pages = list()

        # Verifique se o 'results' existe
        if 'results' in data:
            # Percorra cada item em 'results'
            for item in data['results']:
                # Verifique se o tipo é 'child_page' e se 'child_page' existe
                if item.get('type') == 'child_page' and 'child_page' in item:
                    # Imprima o título
                    page = {
                        'title': item['child_page']['title'],
                        'id': item['id']
                    }
                    child_pages.append(page)
                else:
                    # Se não for 'child_page', pule para o próximo item
                    continue
        return child_pages

    def set_page_content(self, page_id: str, title: str, text: str):
        """
        Sets the content of a page in Notion.

        This method sends a PATCH request to the Notion API to update the specified page with a new title and content.
        The content is structured as a heading and a paragraph.

        :param page_id: The ID of the page to be updated.
        :type page_id: str
        :param title: The title to be set for the page.
        :type title: str
        :param text: The main content to be added to the page.
        :type text: str
        :return: The response from the API, which includes the status of the request and any returned data.
        :rtype: dict
        """
        url = self.base_url + f"blocks/{page_id}/children"
        data = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": title}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": text
                                    # "link": {"url": "https://en.wikipedia.org/wiki/Lacinato_kale"}
                                }
                            }
                        ]
                    }
                }
            ]
        }
        # response = requests.patch(url, headers=headers, data=json.dumps(data))
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.status_code, response.text)
        return response.json()