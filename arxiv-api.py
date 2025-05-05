import arxiv

"""
      |   
  \  ___  /                           _________
 _  /   \  _    GÉANT                 |  * *  | Co-Funded by
    | ~ |       Trust & Identity      | *   * | the European
     \_/        Incubator             |__*_*__| Union
      =
"""


def search_arxiv_publications(author_name, max_results=50):
    """
    Search for publications on ArXiv using the same parameters as the web interface.

    Args:
        author_name (str): The name of the author to search for
        max_results (int): Maximum number of results to return

    Returns:
        List of publications matching the search criteria
    """
    search_query = f"au:\"{author_name}\""
    # search_query = 'au:name+AND+au:surname'

    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    client = arxiv.Client()
    results = list(client.results(search))
    return results


def display_publication_info(results):
    """
    Display the title, year, field, and authors for each publication.

    Args:
        results (list): List of arxiv.Result objects
    """
    if not results:
        print("No publications found for this author.")
        return

    print(f"Found {len(results)} publications:")
    print("-" * 80)

    for i, result in enumerate(results, 1):
        pub_year = result.published.year

        categories = ", ".join(result.categories)

        authors = ", ".join(author.name for author in result.authors)

        print(f"Publication #{i}:")
        print(f"Title: {result.title}")
        print(f"Year: {pub_year}")
        print(f"Field: {categories}")
        print(f"Authors: {authors}")
        print(f"URL: {result.entry_id}")
        print("-" * 80)


def main():
    author_name = input("Enter the author name: ")

    max_results = 50

    try:
        print(f"Searching for publications by '{author_name}'...")
        results = search_arxiv_publications(author_name, max_results)

        display_publication_info(results)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
