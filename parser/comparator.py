class Comparator:
    def compare(self, old_data: dict, new_data: dict) -> dict:
        added = {}
        removed = {}
        updated = {}

        for title, new_value in new_data.items():

            if title not in old_data:
                added[title] = new_value

            elif old_data[title] != new_value:
                updated[title] = {
                    "old": old_data[title],
                    "new": new_value,
                }

        for title, old_value in old_data.items():

            if title not in new_data:
                removed[title] = old_value

        return {
            "added": added,
            "removed": removed,
            "updated": updated,
        }