#!/bin/bash
PREFIX=$(dirname $0)
# Function to generate a random password
generate_password() {
    if [ $((RANDOM % 2)) -eq 0 ]; then
        # 50% chance to select a password from the common_passwords.txt file
        shuf -n 1 "${PREFIX}/common_passwords.txt"
    else
        # 50% chance to generate a random password of random length 8-16
        cat /dev/urandom | tr -dc '[:alnum:]' | fold -w $((RANDOM % 8 + 8)) | head -n 1
    fi
}

# Function to generate a random username
generate_username() {
    first_name=$(shuf -n 1 "${PREFIX}/common_first_names.txt" | tr -d '[:space:]')
    last_name=$(shuf -n 1 "${PREFIX}/common_last_names.txt" | tr -d '[:space:]')
    random_numbers=$(shuf -i 0-9 -n 2 | tr -d '[:space:]')

    echo "${first_name:0:4}${last_name:0:2}${random_numbers}"
}

# List of common passwords
# Removed common passwords list, as it's read from common_passwords.txt now.

# Number of users to create
num_users=15

# Create users
for ((i=1; i<=num_users; i++)); do
    username=$(generate_username)
    password=$(generate_password)
    useradd -m -s /bin/bash -p $(echo "$password") "$username"
    echo "User $username created with password: $password"
done

echo "User creation complete."
