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

    @staticmethod
    def _extract_blocks_content(content):
        """
        Extracts plain text content from a list of blocks within a notion page.
        """
        content_list = list()

        for block in content['results']:
            block_type = block['type']

            # Check if the block has content (rich_text)
            if block[block_type]['rich_text']:
                # Extract plain_text from each rich_text object within the block
                for rich_text in block[block_type]['rich_text']:
                    content_list.append(rich_text['plain_text'])

        # Join the content list into a single string with line breaks
        return "\n".join(content_list)

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

        if data and 'results' in data:
            try:
                content = self._extract_blocks_content(data)
                return content
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
            return None
        return response.json()
