"""
File validation utilities
Validates file size, MIME type, and format
"""

FILE_LIMITS = {
    "max_size": 50 * 1024 * 1024,  # 50 MB
    "allowed_mime_types": [
        "text/plain",
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff"
    ],
    "allowed_extensions": [
        ".txt",
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
        ".tiff"
    ]
}

def validate_file(file_path: str, file_size: int, mime_type: str) -> dict:
    """
    Validate uploaded file
    
    Args:
        file_path: Path to file
        file_size: File size in bytes
        mime_type: MIME type
    
    Returns:
        {valid: bool, error: str|None}
    """
    # Check size
    if file_size > FILE_LIMITS["max_size"]:
        return {
            "valid": False,
            "error": f"Fichier trop volumineux (max {FILE_LIMITS['max_size'] // (1024*1024)} MB)"
        }
    
    # Check MIME type
    if mime_type not in FILE_LIMITS["allowed_mime_types"]:
        return {
            "valid": False,
            "error": f"Type de fichier non supporté: {mime_type}"
        }
    
    # Check extension
    extension = file_path.lower().split('.')[-1] if '.' in file_path else ''
    if f".{extension}" not in FILE_LIMITS["allowed_extensions"]:
        return {
            "valid": False,
            "error": f"Extension non supportée: .{extension}"
        }
    
    return {"valid": True, "error": None}
