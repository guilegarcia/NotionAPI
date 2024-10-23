**Notion API Python Client**

This project provides a Python class (`NotionAPI`) to interact with the Notion API. It allows you to:

- **Retrieve page content:** Extract the content of the first paragraph from a Notion page.
- **Get child pages:** List the child pages of a given parent page.
- **Set page content:** Update a Notion page's title and main text content (heading and paragraph).

**Installation**

1. Install the `requests` library:

   ```bash
   pip install requests
   ```

2. Clone or download this repository.

**Usage**

1. **Obtain your Notion API token:**
   - Create an integration in your Notion workspace ([invalid URL removed]).
   - Choose a name and select "Integrate with another service."
   - Copy the "Internal Integration Token."

2. **Import the `NotionAPI` class:**

   ```python
   from notion_api import NotionAPI
   ```

3. **Create an instance:**

   ```python
   token = "YOUR_NOTION_TOKEN"
   api = NotionAPI(token)
   ```

### Methods

**`get_page_content(page_id)`**

- Fetches the content of the first paragraph from the specified Notion page.
- Returns the content as a string if successful, or `None` if an error occurs.
- **Example:**

   ```python
   page_id = "YOUR_PAGE_ID"
   content = api.get_page_content(page_id)
   if content:
       print(content)
   else:
       print("Error retrieving content.")
   ```

**`get_child_pages(page_id)`**

- Retrieves a list of child pages (direct descendants) for the provided Notion page ID.
- Returns a list of dictionaries containing `title` and `id` for each child page.
- **Example:**

   ```python
   parent_page_id = "YOUR_PARENT_PAGE_ID"
   child_pages = api.get_child_pages(parent_page_id)
   if child_pages:
       for page in child_pages:
           print(f"Child Page: {page['title']}, ID: {page['id']}")
   else:
       print("No child pages found.")
   ```

**`set_page_content(page_id, title, text)`**

- Updates a Notion page's title and main text content (heading and paragraph).
- Returns the API response containing the status code and any returned data.
- **Example:**

   ```python
   page_id = "YOUR_PAGE_ID"
   new_title = "My Updated Page Title"
   new_content = "This is the updated content for the page."
   response = api.set_page_content(page_id, new_title, new_content)
   if response.status_code == 200:
       print("Page content updated successfully!")
   else:
       print(f"Error updating page content: {response.status_code}")
   ```

**Important Notes**

- The `get_page_content` method currently only retrieves the content of the first paragraph. Consider implementing additional logic to handle more complex page structures.
- The `set_page_content` method currently sets a basic heading and paragraph. You can explore the Notion API documentation for more formatting options and block types ([invalid URL removed]).

**Contributing**

Feel free to fork this repository, make changes, and submit pull requests! We welcome contributions to improve the functionality and features of this library.
