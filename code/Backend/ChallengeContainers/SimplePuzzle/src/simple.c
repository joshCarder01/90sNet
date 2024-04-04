#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <sys/file.h>

#define INPUT_SIZE 30

#define INPUT_ERROR(name) printf("There was an error in handling input for " name " please try again later!\n")

int make_flag(char *flag_name);
int get_inputs(char *username, char *password);

int main()
{
    sqlite3 *db;
    char *err_message = 0;
    char *sql_template = "SELECT uid, admin FROM users WHERE username = '%s' AND password = '%s'";
    char *query;
    char username[INPUT_SIZE];
    char password[INPUT_SIZE];

    // Open SQLite database
    int rc = sqlite3_open("example.db", &db);

    if (rc)
    {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return (1);
    }

    // Now we begin an authentication of this
    puts("Welcome to the UC database interaction system\nThis should be used by admins only!");

    if (get_inputs(username, password))
        goto main_error;

    // Want to use the transaction to try and prevent shenanigans
    rc = sqlite3_exec(db, "BEGIN TRANSACTION", 0, 0, &err_message);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to begin transaction: %s\n", err_message);
        sqlite3_free(err_message);
        sqlite3_close(db);
        return 1;
    }

    // Assemble SQL statement
    asprintf(&query, sql_template, username, password);

    // Check if the query returned a uid
    int uid;
    sqlite3_stmt *stmt;
    rc = sqlite3_prepare_v2(db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_free(query);
        sqlite3_close(db);
        return 1;
    }
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW)
    {
        uid = sqlite3_column_int(stmt, 0);
        printf("Logged in - User ID: %d\n", uid);

        // now check if the user has admin
        uid = sqlite3_column_int(stmt, 1);
        if (uid)
        {
            printf("\nAdmin Account Detected\nEnter Flag to Win: ");
            char flag[60];

            fgets(flag, 59, stdin);
            flag[59] = '\0';

            if (make_flag(flag))
            {
                sqlite3_free(query);
                goto main_error;
            }
        }
    }
    else
    {
        printf("No user found, try again later\n");
        goto reg_exit;
    }
    sqlite3_finalize(stmt);
    sqlite3_free(query);

    // Rollback transaction
    rc = sqlite3_exec(db, "ROLLBACK", 0, 0, &err_message);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to rollback transaction: %s\n", err_message);
        sqlite3_free(err_message);
        sqlite3_close(db);
        return 1;
    }

reg_exit:
    // Close database
    sqlite3_close(db);

    return 0;

main_error:
    // Error Occured
    sqlite3_close(db);
    return 1;
}

int get_inputs(char *username, char *password)
{
    printf("Please enter your username: ");
    if (fgets(username, INPUT_SIZE - 1, stdin) == NULL)
    {
        INPUT_ERROR("username");
        return 1;
    }
    username[INPUT_SIZE - 1] = '\0';

    // Check if the SQL template contains "commit"
    if (strcasestr(username, "commit") != NULL)
    {
        fprintf(stderr, "Invalid Username\n");
        return 1;
    }

    printf("Please enter %s's username: ", username);
    if (fgets(password, INPUT_SIZE - 1, stdin) == NULL)
    {
        INPUT_ERROR("password");
        return 1;
    }
    password[INPUT_SIZE - 1] = '\0';

    // Check if the SQL template contains "commit"
    if (strcasestr(password, "commit") != NULL)
    {
        fprintf(stderr, "Invalid Password\n");
        return 1;
    }
    return 0;
}

int make_flag(char *flag_name)
{
    char path[150] = "/root/";

    // Prevent Directory Traversal?
    if (strstr(flag_name, "/") != NULL || strstr(flag_name, "..") != NULL)
    {
        printf("Invalid characters in supplied flag\n");
        return 1;
    }
    sprintf(path, "%s/%s", path, flag_name);

    int fd = open(path, O_CREAT | S_IRUSR | S_IWUSR);
    printf("Flag Added Successfully\n");
    return 0;
}
