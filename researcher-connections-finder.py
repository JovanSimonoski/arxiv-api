import os
import csv
import networkx as nx

"""
      |   
  \  ___  /                           _________
 _  /   \  _    GÉANT                 |  * *  | Co-Funded by
    | ~ |       Trust & Identity      | *   * | the European
     \_/        Incubator             |__*_*__| Union
      =
"""


def load_all_csv_edges(csv_folder="csv_database"):
    """
    Load all CSV edge files from a folder into a single graph.

    Args:
        csv_folder (str): Path to the folder containing CSV edge files.

    Returns:
        nx.Graph: Combined graph from all CSVs.
    """
    G = nx.Graph()

    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(csv_folder, filename)
            print(f"Loading edges from {filename}...")

            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)

                for row in reader:
                    if len(row) == 2:
                        G.add_edge(row[0], row[1])

    print(f"\nTotal nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    return G


def find_connection(G, author1, author2):
    """
    Find and print the shortest path between two authors.

    Args:
        G (nx.Graph): The graph to search in
        author1 (str): First author
        author2 (str): Second author
    """
    if not G.has_node(author1):
        print(f"Author '{author1}' not found in the network.")
        return

    if not G.has_node(author2):
        print(f"Author '{author2}' not found in the network.")
        return

    try:
        path = nx.shortest_path(G, source=author1, target=author2)
        print(f"\nConnection found between '{author1}' and '{author2}':")
        for i, author in enumerate(path):
            if i == 0:
                print(f"  {author}")
            else:
                print(f"  ↳ {author}")
        print(f"\nDegrees of separation: {len(path) - 1}")
    except nx.NetworkXNoPath:
        print(f"No connection found between '{author1}' and '{author2}'.")


def main():
    G = load_all_csv_edges()

    print("\n=== Coauthor Connection Finder ===")
    author1 = input("Enter the first researcher's name: ").strip()
    author2 = input("Enter the second researcher's name: ").strip()

    find_connection(G, author1, author2)


if __name__ == "__main__":
    main()
