from app.schemas.diagram import DiagramNode, DiagramEdge, EdgeMetadata, NodeMetadata

def test_schemas():
    node = DiagramNode(
        id="n1",
        label="Node 1",
        metadata=NodeMetadata(tooltip_title="T1", tooltip_description="D1")
    )
    edge = DiagramEdge(
        id="e1",
        source="n1",
        target="n2",
        metadata=EdgeMetadata(tooltip_title="ET1", relationship_type="dependency")
    )
    print("Node metadata:", node.metadata.tooltip_title)
    print("Edge metadata:", edge.metadata.tooltip_title)
    print("Edge relationship:", edge.metadata.relationship_type)

if __name__ == "__main__":
    test_schemas()
