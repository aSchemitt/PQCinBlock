#!/bin/bash

LANGUAGES=()
SIMULATOR=false

# List to store parameters to forward to Python or Java
ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --language)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do                
                if [[ "$1" != "python" && "$1" != "java" ]]; then
                    echo "Error: invalid language '$1'. Allowed values: python, java"
                    exit 1
                fi

                LANGUAGES+=("$1")

                # Check for maximum number of languages
                if [[ ${#LANGUAGES[@]} -gt 2 ]]; then
                    echo "Error: too many languages specified. Only 'python', 'java', or both."
                    exit 1
                fi

                # Check for duplicates
                if [[ $(printf "%s\n" "${LANGUAGES[@]}" | sort | uniq -d) ]]; then
                    echo "Error: duplicated language '$1'. Only 'python' and/or 'java' are allowed, without repetition."
                    exit 1
                fi

                shift
                
            done
            ;;
        --simulator)
            SIMULATOR=true
            shift
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done


echo "#########################"
echo "Selected languages: ${LANGUAGES[*]}"
echo "Simulator: $SIMULATOR"
echo "Arguments for Python/Java: ${ARGS[*]}"
echo "#########################"


if [[ ${#LANGUAGES[@]} -eq 0 ]]; then
    echo "Error: --language must be specified with 'python' and/or 'java'"
    exit 1
fi


for lang in "${LANGUAGES[@]}"; do
    case "$lang" in
        python)
            echo "Running Python..."
            
            source sig-python/venv/bin/activate
            
            python sig-python/main.py "${ARGS[@]}"
            
            deactivate
            ;;
        java)
            echo "Running Java..."
            
            # java -jar main.jar "${ARGS[@]}"
            ;;
    esac
done



if [[ "$SIMULATOR" == true ]]; then
    echo "Running simulator..."
    # Add simulator command here
fi
