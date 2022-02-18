from typing import List

mappings = {
    "cv2": "opencv-python",
    "pkg_resources": "setuptools",
    "Requests": "requests",  # requests is commonly lowercased
    "skimage": "scikit-image",
    "taming": "taming-transformers-rom1504",
}


def apply_additional_package_mappings(package_names: List[str]) -> List[str]:
    """
    This list augments the Python import name to package name
    mappings in pipreqs.
    """
    # TODO: contribute these mappings back to pipreqs
    for i, name in enumerate(package_names):
        if name in mappings:
            new_name = mappings[name]
            if new_name in package_names:
                package_names[i] = ""
            else:
                package_names[i] = mappings[name]

    package_names = [p for p in package_names if p]

    return package_names
