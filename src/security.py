import os
import platform
import logging
from pathlib import Path
import string
import tkinter as tk
from tkinter import messagebox


class SecurityValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.MAX_PATH_LENGTH = 260 if platform.system() == 'Windows' else 4096
        self.MIN_FREE_SPACE = 100 * 1024 * 1024
        self.MAX_SYMLINK_DEPTH = 20
        self.ALLOWED_CHARS = set(string.ascii_letters + string.digits + '-._() ')
        self.BLOCKED_EXTENSIONS = {
            '.exe', '.dll', '.so', '.dylib', '.bat', '.cmd', '.sh',
            '.vbs', '.pl', '.rb', '.jar', '.msi', '.msp', 'keras', '.h5',
            '.zip', '.tar', '.7z', '.rar', '.gz', '.xz', '.bz2', '.tar.gz',
            '.tar.xz', '.tar.bz2', '.zst','.iso', '.img', '.dmg', '.vhd', '.vhdx', '.ova', '.ovf',
            '.docm', '.xlsm', '.pptm', '.docb', '.dotm',
            '.reg', '.ps1', '.scf', '.lnk', '.sys', '.drv', '.scr',
            '.tmp', '.config', '.ini', '.log', '.bak'
        }

    def is_safe_path(self, path, check_exists=False):
        try:
            path_obj = Path(path)

            if len(str(path_obj)) > self.MAX_PATH_LENGTH:
                return False, f"Path exceeds maximum length of {self.MAX_PATH_LENGTH} characters"

            try:
                resolved_path = path_obj.resolve(strict=False)
            except RuntimeError:
                return False, "Invalid path or too many symbolic links"

            if '..' in str(path_obj.parts):
                return False, "Path traversal attempt detected"

            symlink_depth = 0
            current = path_obj
            while symlink_depth <= self.MAX_SYMLINK_DEPTH:
                if current.is_symlink():
                    symlink_depth += 1
                    current = Path(os.readlink(current))
                else:
                    break
            if symlink_depth > self.MAX_SYMLINK_DEPTH:
                return False, f"Too many symbolic links (max {self.MAX_SYMLINK_DEPTH})"

            abs_path = str(resolved_path.absolute())

            parent_dir = resolved_path.parent
            if check_exists:
                if not parent_dir.exists():
                    return False, "Parent directory does not exist"
                if not os.access(str(parent_dir), os.W_OK):
                    return False, "Parent directory is not writable"

            try:
                if platform.system() == 'Windows':
                    import ctypes
                    free_bytes = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                        ctypes.c_wchar_p(str(parent_dir)),
                        None, None, ctypes.pointer(free_bytes)
                    )
                    free_space = free_bytes.value
                else:
                    st = os.statvfs(str(parent_dir))
                    free_space = st.f_bavail * st.f_frsize

                if free_space < self.MIN_FREE_SPACE:
                    return False, f"Insufficient disk space (minimum {self.MIN_FREE_SPACE / 1024 / 1024}MB required)"
            except Exception as e:
                self.logger.warning(f"Could not check disk space: {str(e)}")

            return True, "Path is safe"

        except Exception as e:
            self.logger.error(f"Error validating path: {str(e)}")
            return False, f"Error validating path: {str(e)}"

    def sanitize_filename(self, filename):
        if not filename:
            return ""

        ext = os.path.splitext(filename)[1].lower()

        if ext in self.BLOCKED_EXTENSIONS:
            root = tk.Tk()
            root.withdraw()
            response = messagebox.askyesno(
                "Blocked Extension Detected",
                f"The file '{filename}' has a blocked extension ({ext}).\n"
                "Do you want to allow it?"
            )
            root.destroy()
            if not response:
                self.logger.info(f"User rejected file creation for: {filename}")
                return None

        sanitized = ''
        for char in filename:
            if char in self.ALLOWED_CHARS:
                sanitized += char
            else:
                sanitized += '_'

        sanitized = sanitized.strip('. ')

        if len(sanitized) > 255:
            base = sanitized[:250]
            ext = sanitized[-4:] if '.' in sanitized[-5:] else ''
            sanitized = base + ext

        if not sanitized:
            sanitized = 'unnamed_file'

        return sanitized

    def is_safe_tree_depth(self, depth):
        MAX_TREE_DEPTH = 20
        return depth <= MAX_TREE_DEPTH, MAX_TREE_DEPTH
