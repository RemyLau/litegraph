class Graph:
    """A light weight (undirected and weighted) graph object."""

    def __init__(self):
        self.data = []
        self.ids = []
        self.idmap = {}
        self._number_of_nodes = 0
        self._number_of_edges = 0

    @property
    def nodes(self):
        return self.ids.copy()

    @property
    def number_of_nodes(self):
        return self._number_of_nodes

    @property
    def number_of_edges(self):
        return self._number_of_edges

    def _add_node(self, node):
        self.idmap[node] = self.number_of_nodes
        self.ids.append(node)
        self.data.append({})
        self._number_of_nodes += 1

    def add_node(self, node):
        if node in self.idmap:
            import warnings
            warnings.warn(
                "{node!r} (index = {self.idmap[node]}) already exists",
                RuntimeWarning
            )
        else:
            self._add_node(node)

    def get_node_idx(self, node):
        if node not in self.idmap:
            self._add_node(node)

        return self.idmap[node]

    def add_edge(self, node1, node2, weight):
        idx1 = self.get_node_idx(node1)
        idx2 = self.get_node_idx(node2)
        self.data[idx1][idx2] = self.data[idx2][idx1] = weight
        self._number_of_edges += 1

    def get_connected_components(self):
        """Find connected components via BFS search.

        Return:
            Sorted list of connected components by size in ascending order

        """
        unvisited = set(range(self.number_of_nodes))
        components = []

        while unvisited:
            seed_node = next(iter(unvisited))
            next_level_nodes = [seed_node]
            component_membership = []

            while next_level_nodes:
                curr_level_nodes = next_level_nodes[:]
                next_level_nodes = []

                for node in curr_level_nodes:
                    if node in unvisited:
                        for nbr in self.data[node]:
                            if nbr in unvisited:
                                next_level_nodes.append(nbr)
                        component_membership.append(node)
                        unvisited.remove(node)

            components.append(component_membership)

        return sorted(components, key=len, reverse=True)

    def subgraph(self):
        raise NotImplementedError
