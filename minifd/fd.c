#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <unistd.h>

#define MAX_FILES 16

typedef struct file file_t;

typedef struct fops {
    void (*close)(file_t* f);
    void (*read)(file_t* f, uint32_t size, char* dst_buf);
    void (*write)(file_t* f, uint32_t size, char* src_buf);
    void (*dup)(file_t* f);
} fops_t;

typedef struct file {
    uint8_t refcount;
    uint32_t size;
    char* buf;
    char name[32];
    fops_t fops;
} file_t;


// global table of files
file_t* files[MAX_FILES];




/*
 * Delete fd entry in table and free if refcount 0
 */
int do_close(int fd) {
    if (fd < 0 && fd >+ MAX_FILES) {
        return -1;
    }

    file_t* f = files[fd];
    if (!f) {
        return -1;
    }
    
    f->fops.close(f);
    
    files[fd] = NULL;
    return 0;
}

void c3ctf_file_close(file_t* f) {
    f->refcount -= 1;
    if (f->refcount == 0) {
        free(f->buf);
        free(f);
    }
}

/*
 * Read <size> characters from file and write into <dest_buf>
 */
int do_read(int fd, uint32_t size, char* dst_buf) {
    if (fd < 0 && fd >= MAX_FILES) {
        return -1;
    }

    file_t* f = files[fd];
    if (!f) {
        return -1;
    }

    f->fops.read(f, size, dst_buf);

    return 0;
}

void c3ctf_file_read(file_t* f, uint32_t size, char* dst_buf) {
    if (size > f->size) {
        size = f->size;
    }
    strncpy(dst_buf, f->buf, size);
}


/*
 * Write <size> characters from <src_buf> into file buffer
 */
int do_write(int fd, uint32_t size, char* src_buf) {
    if (fd < 0 && fd >= MAX_FILES) {
        return -1;
    }

    file_t* f = files[fd];
    if (!f) {
        return -1;
    }
    
    f->fops.write(f, size, src_buf);

    return 0;
}


void c3ctf_file_write(file_t* f, uint32_t size, char* src_buf) {
    if (size > f->size) {
        f->buf = realloc(f->buf, size);
    }
    f->size = size;
    strncpy(f->buf, src_buf, size);
}


/*
 * Duplicate file - create new file entry in table
 */
int do_dup(int fd) {
    if (fd < 0 && fd >= MAX_FILES) {
        return -1;
    }

    file_t* f = files[fd];
    if (!f) {
        return -1;
    }
   

    f->fops.dup(f);

    int new_fd = -1;
    for (int i = 0; i < MAX_FILES; ++i) {
        if (files[i] == NULL) {
            new_fd = i;
            break;
        }
    }
    if (new_fd < 0) {
        return -1;
    }
    
    files[new_fd] = f; 
    return new_fd;
}

void c3ctf_file_dup(file_t* f) {
    f->refcount += 1;
}


/*
 * Return index into table (fd)
 */
int create(char* name) {
    int fd = -1;
    for (int i = 0; i < MAX_FILES; ++i) {
        if (files[i] == NULL) {
            fd = i;
            break;
        }
    }
    if (fd < 0) {
        return -1;
    }
    
    file_t* f = calloc(1, sizeof(file_t));
    f->refcount = 1;
    f->size = 0;
    f->buf = NULL;
    strncpy(f->name, name, 31);

    f->fops.close = &c3ctf_file_close;
    f->fops.read = &c3ctf_file_read;
    f->fops.write = &c3ctf_file_write;
    f->fops.dup = &c3ctf_file_dup;
    
    files[fd] = f; 
    return fd;
}


void file_manager() {
    printf( "\n"
            "----------------------\n"
            " Simple File Mananger \n"
            "----------------------\n"
            "\n"
            "This is a simple file manager implementation supporting basic functionality\n"
            "to create, read, and write files.\n"
            "\n"
            "Please note:\n"
            "This is a prototype implementation.\n"  
            "At this point of time, only %d files can be managed at the same time.\n", MAX_FILES);

    printf( "\n"
            "The Simple File Manager supports the following operations.\n"
            "[1] list\n"
            "    Print the file table\n"
            "[2] create <string>\n"
            "    Create a file with name <string>\n"
            "[3] close <fd>\n"
            "    Close the file with file descriptor <fd>\n"
            "[4] dup <fd>\n"
            "    Duplicate a file descriptor <fd>\n"
            "[5] read <fd> <n>\n"
            "    Read <n> bytes from the file with file descriptor <fd>\n"
            "[6] write <fd> <n> <string>\n"
            "    Write <n> bytes to the file with file descriptor <fd>\n"
            "[7] exit\n"
            "    Leave the Simple File Manager\n"
            "\n");

    char* line = NULL;
    size_t linelen;
    while (1) {
        char name[32];
        int fd;
        uint32_t n;
        char* data = NULL;
        
        printf( "\n"
                "Enter the command you want to execute.\n"
                "[1] list\n"
                "[2] create <string>\n"
                "[3] close <fd>\n"
                "[4] dup <fd>\n"
                "[5] read <fd> <n>\n"
                "[6] write <fd> <n> <string>\n"
                "[7] exit\n"
                "\n> ");
        

        if (getline(&line, &linelen, stdin) == -1) {
            break;
        }

        if (strncmp(line, "list", 4) == 0) {
            printf( "-----------------------------------------\n"
                    "| fd |         file name                |\n"
                    "-----------------------------------------\n");
            for (int fd = 0; fd < MAX_FILES; ++fd) {
                file_t* f = files[fd];
                char* name = "";
                if (f) {
                    name = f->name;
                }
                printf("| %2d | %32s |\n", fd, name);
            }
            printf("-----------------------------------------\n");
        } else if (sscanf(line, "create %32s", name) == 1) {
            int fd = create(name);
            if (fd >= 0) {
                printf("Created file with file descriptor: %d\n", fd);
            } else {
                printf("Error: File could not be created\n");
            }
        } else if (sscanf(line, "close %d", &fd) == 1) {
            int ret = do_close(fd);
            if (ret == 0) {
                printf("Closed file with file descriptor: %d\n", fd);
            } else {
                printf("Error: File with fd %d could not be closed\n", fd);
            }
        } else if (sscanf(line, "dup %d", &fd) == 1) {
            int new_fd = do_dup(fd);
            if (new_fd >= 0) {
                printf("Duplicated file %d with new file descriptor: %d\n", fd, new_fd);
            } else {
                printf("Error: File with fd %d could not be duplicated. File table full?\n", fd);
            }
        } else if (sscanf(line, "read %d %d", &fd, &n) == 2) {
            data = calloc(1, n + 1);
            int ret = do_read(fd, n, data);
            if (ret == 0) {
                printf("%s\n", data);
            } else {
                printf("Error: Could not read from file %d\n", fd);
            }
            free(data);
            data = NULL;
        } else if (sscanf(line, "write %d %d %m[^\n]s", &fd, &n, &data) == 3) {
            int ret = do_write(fd, n, data);
            if (ret == 0) {
                printf("Wrote %d bytes to file  %d\n", n, fd);
            } else {
                printf("Error: Could not write to file %d\n", fd);
            }
            free(data);
            data = NULL;
        } else if (strncmp(line, "exit", 4) == 0) {
            break;
        } else {
            printf("Invalid command\n");
        }
    }
    free(line);
}

void spawn_shell() {
    char* args[] = {(char*)"/bin/bash", NULL};
    execve("/bin/bash", args, NULL);
}

int main(int argc, char* argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);

    file_manager();
}
