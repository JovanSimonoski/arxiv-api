import os.path

import arxiv
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

"""
      |   
  \  ___  /                           _________
 _  /   \  _    GÉANT                 |  * *  | Co-Funded by
    | ~ |       Trust & Identity      | *   * | the European
     \_/        Incubator             |__*_*__| Union
      =
"""


def search_arxiv_publications(author_name, max_results=3):
    """
    Search for publications on ArXiv by author name.

    Args:
        author_name (str): The name of the author to search for
        max_results (int): Maximum number of results to return

    Returns:
        List of publications matching the search criteria
    """
    search_query = f"au:\"{author_name}\""

    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    client = arxiv.Client()
    results = list(client.results(search))
    return results


def get_coauthors(result):
    """
    Extract coauthors from a publication result.

    Args:
        result (arxiv.Result): A publication result

    Returns:
        list: List of coauthor names
    """
    return [author.name for author in result.authors]


def build_collaboration_network(start_author, max_depth=2):
    """
    Build a collaboration network starting from an author, exploring to max_depth.

    Args:
        start_author (str): The name of the author to start with
        max_depth (int): Maximum depth to explore the network

    Returns:
        nx.Graph: A graph representing the collaboration network
    """
    G = nx.Graph()

    processed_authors = set()

    queue = deque([(start_author, 0)])

    while queue:
        current_author, depth = queue.popleft()

        if current_author in processed_authors:
            continue

        processed_authors.add(current_author)
        print(f"Processing author: {current_author} (depth {depth})")

        if not G.has_node(current_author):
            G.add_node(current_author)

        if depth >= max_depth:
            continue

        results = search_arxiv_publications(current_author)

        if not results:
            continue

        for r in results:
            coauthors = get_coauthors(r)

            for coauthor in coauthors:
                if coauthor != current_author:
                    G.add_edge(current_author, coauthor)

                    if coauthor not in processed_authors:
                        queue.append((coauthor, depth + 1))

    return G


def visualize_network(G, author, max_depth):
    """
    Visualize and save the collaboration network.

    Args:
        G (nx.Graph): The collaboration network graph
        author (str): Author name
        max_depth (int): Maximum depth to explore the network
    """
    plt.figure(figsize=(50, 25))
    pos = nx.spring_layout(G, seed=42, k=0.3, iterations=100)

    nx.draw(G, pos,
            with_labels=True,
            node_color='skyblue',
            node_size=300,
            edge_color='gray',
            font_size=9,
            width=0.8,
            alpha=0.8)

    plt.title("Author Collaboration Network", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

    filename = "images_database/" + "collaboration_network_" + author.replace(" ", "") + "_depth_" + str(
        max_depth) + ".png"

    # plt.savefig(filename, dpi=300)
    # print(f"Graph image saved as {filename}")

    plt.show()
    plt.close()


import csv


def save_edges_to_csv(G, author, max_depth):
    """
    Save the graph edges to a CSV file.

    Args:
        G (nx.Graph): The collaboration network graph
        author (str): author name
        max_depth (int): Maximum depth to explore the network
    """

    filename = "csv_database/" + "collaboration_network_" + author.replace(" ", "") + "_depth_" + str(
        max_depth) + ".csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Author1", "Author2"])

        for u, v in G.edges():
            writer.writerow([u, v])

    print(f"Collaboration edges saved to {filename}")


def main():
    author_name = input("Enter the starting author name: ")
    # author_name = "Yoshua Bengio"
    max_depth = int(input("Enter the maximum depth to explore (1-3 recommended): "))
    # max_depth = 3

    try:
        print(f"Building collaboration network starting from '{author_name}' with depth {max_depth}...")
        G = build_collaboration_network(author_name, max_depth)

        print(f"\nNetwork statistics:")
        print(f"Number of authors: {G.number_of_nodes()}")
        print(f"Number of collaborations: {G.number_of_edges()}")

        save_edges_to_csv(G, author_name, max_depth)
        # visualize_network(G, author_name, max_depth)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
