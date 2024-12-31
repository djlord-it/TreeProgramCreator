import os
import re
import platform
import logging

class SecurityValidator:
    @staticmethod
    def is_safe_path(path, check_exists=False):
        try:
            abs_path = os.path.abspath(os.path.realpath(path))
            if '..' in path:
                return False, "Path contains suspicious patterns"
            parent_dir = os.path.dirname(abs_path)
            if check_exists and not os.access(parent_dir, os.W_OK):
                return False, "Parent directory is not writable"

            try:
                if platform.system() == 'Windows':
                    import ctypes
                    free_bytes = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(parent_dir), 
                        None, None, ctypes.pointer(free_bytes))
                    free_space = free_bytes.value
                else:
                    st = os.statvfs(parent_dir)
                    free_space = st.f_bavail * st.f_frsize
                    
                if free_space < 1024 * 1024:  # 1MB
                    return False, "Insufficient disk space"
            except Exception as e:
                logging.warning(f"Could not check disk space: {str(e)}")
                
            return True, "Path is safe"
            
        except Exception as e:
            if check_exists:
                return False, f"Error validating path: {str(e)}"
            return True, "Path will be created"

    @staticmethod
    def sanitize_filename(filename):
        unsafe_chars = r'[<>:"/\\|?*\x00-\x1f]'
        sanitized = re.sub(unsafe_chars, '_', filename)
        
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
            
        return sanitized.strip()
