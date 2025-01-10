import os
import logging
from src.security import SecurityValidator
from src.parser import TreeParser


class DirectoryCreator:
    def __init__(self):
        self.validator = SecurityValidator()
        self.parser = TreeParser()
        self.logger = logging.getLogger(__name__)

    def create_structure_from_tree(self, tree_lines, base_path='.'):
        stack = []
        created_items = []

        try:
            root_line = tree_lines[0].strip()
            if not root_line.endswith('/'):
                raise ValueError("The root directory must be specified and end with a slash ('/').")

            root_name = root_line[:-1]
            root_path = os.path.join(base_path, root_name)

            is_safe, message = self.validator.is_safe_path(root_path, check_exists=False)
            if not is_safe:
                raise ValueError(f"Invalid root path: {message}")

            os.makedirs(root_path, exist_ok=True)
            stack.append(root_path)
            created_items.append(root_path)
            self.logger.info(f"Created root directory: {root_path}")

            for line in tree_lines[1:]:
                if not line.strip():
                    continue

                depth, name, is_dir = self.parser.parse_tree_line(line)

                # Skip if name is None (blocked or invalid file)
                if name is None:
                    self.logger.warning("Skipping creation of blocked or invalid file.")
                    continue

                while len(stack) - 1 > depth:
                    stack.pop()

                parent_dir = stack[-1]
                current_path = os.path.join(parent_dir, name)

                is_safe, message = self.validator.is_safe_path(current_path, check_exists=False)
                if not is_safe:
                    self.logger.warning(f"Invalid path '{current_path}': {message}. Skipping.")
                    continue

                try:
                    if is_dir:
                        os.makedirs(current_path, exist_ok=True)
                        stack.append(current_path)
                    else:
                        os.makedirs(parent_dir, exist_ok=True)
                        if not os.path.exists(current_path):
                            with open(current_path, 'w') as f:
                                pass
                    created_items.append(current_path)
                    self.logger.info(f"Created: {current_path}")
                except OSError as e:
                    self.logger.error(f"Error creating {current_path}: {str(e)}")
                    self.cleanup_created_items(created_items)
                    raise

            return True, "Directory structure created successfully, with some files skipped if blocked."

        except Exception as e:
            self.logger.error(f"Error in create_structure_from_tree: {str(e)}")
            self.cleanup_created_items(created_items)
            return False, f"Error creating structure: {str(e)}"

    def cleanup_created_items(self, items):
        for item in reversed(items):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    if not os.listdir(item):
                        os.rmdir(item)
            except Exception as e:
                self.logger.error(f"Error during cleanup of {item}: {str(e)}")
