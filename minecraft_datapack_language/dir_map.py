
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class DirMap:
    function: str
    advancement: str
    recipe: str
    loot_table: str
    predicate: str
    item_modifier: str
    structure: str
    tags_function: str
    tags_item: str
    tags_block: str
    tags_entity_type: str
    tags_fluid: str
    tags_game_event: str

def get_dir_map(pack_format: int) -> DirMap:
    """Return the correct directory mapping based on datapack pack_format.
    >=48 (1.21) uses singular folders and new tag subfolders.
    <48 uses legacy plural folders.
    """
    if pack_format >= 48:
        return DirMap(
            function="function",
            advancement="advancement",
            recipe="recipe",
            loot_table="loot_table",
            predicate="predicate",
            item_modifier="item_modifier",
            structure="structure",
            tags_function="tags/function",
            tags_item="tags/item",
            tags_block="tags/block",
            tags_entity_type="tags/entity_type",
            tags_fluid="tags/fluid",
            tags_game_event="tags/game_event",
        )
    else:
        return DirMap(
            function="functions",
            advancement="advancements",
            recipe="recipes",
            loot_table="loot_tables",
            predicate="predicates",
            item_modifier="item_modifiers",
            structure="structures",
            tags_function="tags/functions",
            tags_item="tags/items",
            tags_block="tags/blocks",
            tags_entity_type="tags/entity_types",
            tags_fluid="tags/fluids",
            tags_game_event="tags/game_events",
        )
