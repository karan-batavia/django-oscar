# Generated by Django 5.1.4 on 2025-02-17 12:47

from django.db import migrations, connection

def create_materialized_view(apps, schema_editor):
    """Creates a materialized view for PostgreSQL."""
    print("Ja ik ga dinges aanmaken jeweeet", connection.vendor)
    if connection.vendor == "postgresql":
        print("JAAA IK MAAK M AAN !!!@" * 30)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE MATERIALIZED VIEW IF NOT EXISTS catalogue_product_category_hierarchy AS
                WITH RECURSIVE category_hierarchy AS (
                    SELECT id, path FROM catalogue_category
                )
                SELECT DISTINCT 
                    CONCAT(p.id, '-', parent_categories.id) AS id,
                    p.id AS product_id, 
                    parent_categories.id AS category_id
                FROM catalogue_productcategory pc
                JOIN catalogue_category child_categories ON pc.category_id = child_categories.id
                JOIN catalogue_category parent_categories 
                    ON child_categories.path LIKE parent_categories.path || '%'
                JOIN catalogue_product p ON p.id = pc.product_id;
                
            """)


def create_index(apps, schema_editor):
    """Creates a unique index for PostgreSQL (outside Django transaction)."""
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS catalogue_product_category_hierarchy_idx
                ON catalogue_product_category_hierarchy (product_id, category_id);
            """)


def drop_materialized_view(apps, schema_editor):
    """Drops the materialized view if rolling back."""
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("DROP MATERIALIZED VIEW IF EXISTS catalogue_product_category_hierarchy;")


class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ("catalogue", "0029_product_code"),
    ]

    operations = [
         migrations.RunPython(create_materialized_view, drop_materialized_view),
         migrations.RunSQL(
             sql="CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS catalogue_product_category_hierarchy_idx "
                 "ON catalogue_product_category_hierarchy (product_id, category_id);",
             reverse_sql="DROP INDEX IF EXISTS catalogue_product_category_hierarchy_idx;",
         ),
     ]
