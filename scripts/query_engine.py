import os
from pathlib import Path

class EntityQuery:
    def __init__(self, entities, graph):
        self.entities = entities # List of entity dicts
        self.graph = graph # The GraphQuery instance for traversals

    def __iter__(self):
        return iter(self.entities)
        
    def __len__(self):
        return len(self.entities)
        
    def filter(self, predicate):
        return EntityQuery([e for e in self.entities if predicate(e)], self.graph)
        
    def by_type(self, entity_type):
        return self.filter(lambda e: e.get('entity_type') == entity_type)
        
    def current(self):
        return self.filter(lambda e: e.get('current', False) or e.get('end_date') is None)
        
    def verified(self):
        return self.filter(lambda e: e.get('status') == 'verified' or e.get('confidence') == 'verified')
        
    def market(self, market_name):
        return self.filter(lambda e: market_name in e.get('markets', []))
        
    def supported(self):
        # Has at least one evidence or employment linked to it via SUPPORTED_BY
        supported_ids = set()
        for edge in self.graph.edges:
            if edge.get('type') == 'SUPPORTED_BY' and edge.get('from') in [e['id'] for e in self.entities]:
                supported_ids.add(edge.get('from'))
        return self.filter(lambda e: e['id'] in supported_ids)
        
    def missing(self):
        # Find entities missing evidence? Or just missing in general?
        # Let's say missing evidence (not supported)
        supported_ids = set()
        for edge in self.graph.edges:
            if edge.get('type') == 'SUPPORTED_BY':
                supported_ids.add(edge.get('from'))
        return self.filter(lambda e: e['id'] not in supported_ids)
        
    def get_upstream(self, rel_type=None):
        upstream_entities = []
        for e in self.entities:
            for edge in self.graph.get_edges(target_id=e['id'], rel_type=rel_type):
                if edge['from'] in self.graph.entities_by_id:
                    upstream_entities.append(self.graph.entities_by_id[edge['from']])
        return EntityQuery(upstream_entities, self.graph)
        
    def get_downstream(self, rel_type=None):
        downstream_entities = []
        for e in self.entities:
            for edge in self.graph.get_edges(source_id=e['id'], rel_type=rel_type):
                if edge['to'] in self.graph.entities_by_id:
                    downstream_entities.append(self.graph.entities_by_id[edge['to']])
        return EntityQuery(downstream_entities, self.graph)

class GraphQuery:
    def __init__(self, entities, edges):
        self.entities_by_id = entities
        self.edges = edges
        
        self.indexes = {
            'by_source': {},
            'by_target': {}
        }
        
        for edge in self.edges:
            source = edge['from']
            target = edge['to']
            if source not in self.indexes['by_source']:
                self.indexes['by_source'][source] = []
            self.indexes['by_source'][source].append(edge)
            
            if target not in self.indexes['by_target']:
                self.indexes['by_target'][target] = []
            self.indexes['by_target'][target].append(edge)
            
    def get_edges(self, source_id=None, target_id=None, rel_type=None):
        edges = self.edges
        if source_id:
            edges = self.indexes['by_source'].get(source_id, [])
        if target_id:
            edges = [e for e in edges if e.get('to') == target_id]
        if rel_type:
            edges = [e for e in edges if e.get('type') == rel_type]
        return edges

    def all(self):
        return EntityQuery(list(self.entities_by_id.values()), self)
        
    def claims(self):
        return self.all().by_type('claim')
        
    def employments(self):
        return self.all().by_type('employment')
        
    def evidence(self):
        return self.all().by_type('evidence')
        
    def qualifications(self):
        return self.all().by_type('qualification')
        
    def entity(self, entity_id):
        e = self.entities_by_id.get(entity_id)
        return EntityQuery([e] if e else [], self)

def load_graph(data_dir="career-data"):
    # Avoid circular imports by importing dynamically or ensuring paths
    import sys
    sys.path.append(str(Path(__file__).parent))
    from resolve_graph import build_graph_dict
    
    data_dir = Path(data_dir)
    graph_dict = build_graph_dict(data_dir)
    
    return GraphQuery(graph_dict['entities'], graph_dict['edges'])

