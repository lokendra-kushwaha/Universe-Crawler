import numpy as np

def generate_transition_matrix(web_graph):
    """
    Converts a web graph dictionary into a NumPy transition matrix for PageRank.
    
    This function performs three main tasks:
    1. Indexes all unique URLs (both givers and receivers) to assign them a fixed row/col ID.
    2. Builds an N x N matrix where Columns = Voting Pages (Givers) and Rows = Target Pages (Receivers).
    3. Applies a mathematical patch to "dead-end" pages to prevent Rank Leakage.

    Args:
        web_graph (dict): A dictionary where keys are source URLs and values are lists of outbound URLs.

    Returns:
        tuple: 
            - M (numpy.ndarray): The N x N transition matrix.
            - unique_pages (list): The master list mapping matrix indices to actual URLs.
    """
    unique_pages = []

    # STEP 1: Build the Master Index
    # We must collect BOTH main pages and their links into a single list 
    # to ensure our matrix is perfectly square (N x N).
    for main_page, link_list in web_graph.items():
        if main_page not in unique_pages:
            unique_pages.append(main_page)
        for link in link_list:
            if link not in unique_pages:
                unique_pages.append(link)

    num_pages = len(unique_pages)
    
    # Initialize an N x N grid with 0.0 (Zero Matrix)
    M = np.zeros((num_pages, num_pages))

    # STEP 2: Distribute the Votes (Matrix Population)
    for main_page, link_list in web_graph.items():
        col_index = unique_pages.index(main_page) # Column acts as the Donor/Giver

        if len(link_list) == 0:
            continue

        # Split the page's authority equally among all its outbound links
        vote_weight = 1.0 / len(link_list)
        
        for link in link_list:
            row_index = unique_pages.index(link) # Row acts as the Receiver
            # Use += to accumulate votes in case a page links to the same target multiple times
            M[row_index, col_index] += vote_weight

    # STEP 3: The Master Dead-End Patch (Fixing the Black Holes)
    # Pages with no outbound links absorb rank but give nothing back, draining the system.
    # We fix this by forcing these empty columns to distribute their rank to everyone equally.
    
    col_sums = M.sum(axis=0)            # 1. Calculate the total weight distributed by each column
    dead_ends = (col_sums == 0)         # 2. Identify columns that gave out 0.0 total (The Black Holes)
    M[:, dead_ends] = 1.0 / num_pages   # 3. Fill these empty columns with uniform probabilities (1/N)
    
    return M, unique_pages

def calculate_pagerank(M, num_pages, damping_factor=0.85, max_iterations=100):
    """
    Calculates the PageRank of a network using a scaled Power Iteration algorithm.
    
    This optimized version scales the total system authority to N (Total Pages) 
    rather than 1.0. This prevents floating-point underflow in large web graphs 
    and ensures rapid, stable convergence without requiring micro-tolerances.

    Args:
        M (numpy.ndarray): The N x N transition matrix with the dead-end patch applied.
        num_pages (int): Total number of unique pages (N) in the network.
        damping_factor (float): The probability (0.85) of following matrix links 
                                vs. randomly teleporting to a new page.
        max_iterations (int): Safety limit to prevent infinite loops.

    Returns:
        numpy.ndarray: A 1D array of final PageRank scores where the sum equals N.
    """
    N = num_pages 
    
    # Initialize all pages with a base authority of 1.0 (Total system authority = N)
    rank_vector = np.ones(N)
    
    d = damping_factor
    counter = 0

    while counter < max_iterations:
        # Scaled Core PageRank Equation:
        # (1 - d) is the teleportation factor algebraically balanced for an N-scaled system
        new_rank = (1 - d) + (d * np.dot(M, rank_vector))

        # Convergence Check: Standard 1e-6 tolerance is highly effective on scaled values
        if np.allclose(rank_vector, new_rank, atol=1e-6):
            return new_rank
        
        rank_vector = new_rank
        counter += 1

    return rank_vector