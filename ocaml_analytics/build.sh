#!/bin/bash
# Build script for OCaml analytics module

echo "Building OCaml analytics module..."

# Check if OCaml is installed
if ! command -v ocaml &> /dev/null; then
    echo "OCaml is not installed. Please install OCaml to build this module."
    echo "You can install it using: sudo apt-get install ocaml"
    exit 1
fi

# Check if dune is installed
if command -v dune &> /dev/null; then
    echo "Using dune for building..."
    cd "$(dirname "$0")"
    dune build
    if [ $? -eq 0 ]; then
        echo "Build successful! Binary available at: _build/default/analytics.exe"
        # Copy to current directory for easier access
        cp _build/default/analytics.exe ./analytics.exe
        echo "Copied to: ./analytics.exe"
    else
        echo "Build failed!"
        exit 1
    fi
else
    # Fallback to ocamlopt
    echo "Dune not found. Using ocamlopt for building..."
    cd "$(dirname "$0")"
    ocamlopt -o analytics.exe analytics.ml
    if [ $? -eq 0 ]; then
        echo "Build successful! Binary: analytics.exe"
    else
        echo "Build failed!"
        exit 1
    fi
fi
