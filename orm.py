from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, event
from sqlalchemy.orm import registry, relationship
import model
import logging

logger = logging.getLogger(__name__)


mapper_registry = registry()
metadata = mapper_registry.metadata

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    logger.info("Starting mappers a ver que pasa")
    lines_mapper = mapper_registry.map_imperatively(model.OrderLine, order_lines)
    batches_mapper = mapper_registry.map_imperatively(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set,
            )
        },
    )
