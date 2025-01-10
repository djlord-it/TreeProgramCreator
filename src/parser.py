import logging
from src.security import SecurityValidator


class TreeParser:
    def __init__(self):
        self.validator = SecurityValidator()
        self.logger = logging.getLogger(__name__)

    def parse_tree_line(self, line):
        try:
            line = line.rstrip('\n')
            depth = 0
            while line.startswith('│   ') or line.startswith('    '):
                depth += 1
                if depth > 20:
                    raise ValueError("Directory depth exceeds maximum allowed")
                line = line[4:]

            if line.startswith('├── ') or line.startswith('└── '):
                line = line[4:]

            name = line.strip()
            is_dir = name.endswith('/')

            if is_dir:
                name = name[:-1]

            sanitized_name = self.validator.sanitize_filename(name)
            if sanitized_name is None:
                self.logger.warning(f"File creation skipped for blocked file: {name}")
                return depth, None, is_dir

            return depth, sanitized_name, is_dir

        except Exception as e:
            self.logger.error(f"Error parsing line '{line}': {str(e)}")
            raise
