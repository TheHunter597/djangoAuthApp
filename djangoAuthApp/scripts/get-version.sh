#!/bin/bash
VERSION_FILE="__init__.py"

# Extract the current version using grep and awk
CURRENT_VERSION=$(grep "__version__" $VERSION_FILE | awk -F'"' '{print $2}')

# Function to increment the major version
increment_major_version() {
    IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
    major=$((major + 1))
    echo "$major.0.0"
}

# Function to increment the minor version
increment_minor_version() {
    IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
    minor=$((minor + 1))
    echo "$major.$minor.0"
}

# Function to increment the patch version
increment_patch_version() {
    IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
    patch=$((patch + 1))
    echo "$major.$minor.$patch"
}

# Join all arguments into a single string
PARAMETER="$*"

# Check if the parameter contains "major", "minor", or "patch"
if [[ "$PARAMETER" == *"major"* ]]; then
    NEW_VERSION=$(increment_major_version)
    # Update the version in the Python file
    sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" $VERSION_FILE
    echo "$NEW_VERSION"
elif [[ "$PARAMETER" == *"minor"* ]]; then
    NEW_VERSION=$(increment_minor_version)
    # Update the version in the Python file
    sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" $VERSION_FILE
    echo "$NEW_VERSION"
elif [[ "$PARAMETER" == *"patch"* ]]; then
    NEW_VERSION=$(increment_patch_version)
    # Update the version in the Python file
    sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" $VERSION_FILE
    echo "$NEW_VERSION"
else
    echo "Invalid parameter. Use 'major', 'minor', or 'patch'."
fi
