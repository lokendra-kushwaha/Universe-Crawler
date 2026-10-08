def calculate_pagerank(web_graph):
    """
    Calculates PageRank using the Power Iteration method with sparse data structures.
    
    This implementation completely avoids dense N x N matrices, eliminating 
    MemoryErrors for large scale web graphs. It utilizes dictionaries and sets 
    to achieve highly efficient O(N + E) time complexity per iteration and 
    O(N) space complexity.

    Args:
        web_graph (dict): Adjacency list representation of the web graph. 
                          Keys are source URLs (str), values are lists of target URLs (str).

    Returns:
        tuple: A 3-element tuple containing:
            - None: Placeholder to maintain backward compatibility with legacy app.py.
            - list: A strictly ordered list of all unique pages (URLs) in the network.
            - list: The calculated PageRank scores corresponding to the unique pages.
    """
    
    # ==========================================
    # STEP 1: Build the Master Index
    # ==========================================
    # Using a set for O(1) insertions and to ensure strictly unique URLs.
    unique_pages_set = set()

    for main_page, link_list in web_graph.items():
        unique_pages_set.add(main_page)
        unique_pages_set.update(link_list)  # Instantly adds all target links without duplicates

    num_pages = len(unique_pages_set)

    # Convert set to a list to guarantee consistent ordering for the final output array
    unique_pages = list(unique_pages_set)

    # ==========================================
    # STEP 2: Initialize Ranks
    # ==========================================
    # Distribute the initial rank equally among all pages (1.0 / N)
    current_rank = {}
    for unique_page in unique_pages:
        current_rank[unique_page] = 1.0

    # ==========================================
    # STEP 3: Identify Dangling Nodes (Dead Ends)
    # ==========================================
    # Pages with no outgoing links. Their rank needs to be redistributed fairly.
    dangling_nodes = set()
    for unique_page in unique_pages:
        if unique_page not in web_graph or len(web_graph[unique_page]) == 0:
            dangling_nodes.add(unique_page)

    # ==========================================
    # STEP 4: Power Iteration Loop
    # ==========================================
    d = 0.85  # Damping factor (probability of a surfer clicking a random link)
    tolerance = 1e-6  # Convergence threshold to stop the loop early
    
    for _ in range(100):
        # Calculate the total rank held by all dangling nodes in this iteration
        dangling_sum = 0.0
        for node in dangling_nodes:
            dangling_sum += current_rank[node]

        # Prepare a fresh dictionary for the updated ranks of this round
        new_rank = {}
        for unique_page in unique_pages:
            new_rank[unique_page] = 0.0

        # 4.1: Distribute rank to outgoing links (Network Traversal)
        for main_page, target_links in web_graph.items():
            if len(target_links) > 0:
                share = current_rank[main_page] / len(target_links)
                for link in target_links:
                    if link in new_rank:  # Safety check to prevent KeyErrors
                        new_rank[link] += share

        # 4.2: Apply the Master Equation and calculate convergence error
        error = 0.0
        for page in unique_pages:
            # PageRank Formula: (Rank from links) + (Rank from dead ends) + (Teleportation Base)
            new_rank[page] = (d * new_rank[page]) + (d * dangling_sum / num_pages) + (1.0 - d)
            
            # Accumulate the absolute difference to check for stability
            error += abs(new_rank[page] - current_rank[page])
            
        # 4.3: Prepare for the next round
        current_rank = new_rank
        
        # 4.4: Break early if ranks have stabilized below the tolerance limit
        if error < tolerance:
            break
    
    # ==========================================
    # STEP 5: Final Output
    # ==========================================
    # Extract final ranks ensuring they precisely match the exact order of unique_pages
    final_ranks_list = [current_rank[page] for page in unique_pages]
    
    return unique_pages, final_ranks_list