#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <ctype.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>

#include "lmdb.h"

#define LINE_SIZE       10240

int main(int    argc, char  *argv[])
{
    int     size;
    char    string[LINE_SIZE+1];
    char    s_key[LINE_SIZE+1];
    char    s_value[LINE_SIZE+1];
    char*   token;
    char*   save;
    int     cnt_line;

    int         rc;
    MDB_env*    env;
    MDB_txn*    txn;
    MDB_cursor* mc;
    MDB_dbi     dbi;
    MDB_val     key, data;
    char*       envname;
    int         envflags=0;
    char*       subname;
    char*       prog = argv[0];
    size_t      map_size = (SIZE_MAX / (1024*1024*1024) / 4)*6; // 4giga * 6

    struct timeval tv1, tv2;

    if(argc != 3) {
        fprintf(stderr,"%s <envname> <subname>\n",prog);
        exit(1);
    }
    
    envflags = MDB_NOSUBDIR | MDB_NOLOCK;
    envname = argv[1];
    rc = mdb_env_create(&env);
    if(rc) {
        fprintf(stderr, "mdb_env_create failed, error %d %s\n", rc, mdb_strerror(rc));
        return EXIT_FAILURE;
    }
    mdb_env_set_maxdbs(env, 2);
    mdb_env_set_mapsize(env, map_size);
    rc = mdb_env_open(env, envname, envflags, 0664);
    if(rc) {
        fprintf(stderr, "mdb_env_open failed, error %d %s\n", rc, mdb_strerror(rc));
        goto env_close;
    }
    rc = mdb_txn_begin(env, NULL, 0, &txn);
    if(rc) {
        fprintf(stderr, "mdb_txn_begin failed, error %d %s\n", rc, mdb_strerror(rc));
        goto env_close;
    }
    subname = argv[2];
    rc = mdb_open(txn, subname, MDB_CREATE, &dbi);
    if (rc) {
        fprintf(stderr, "mdb_open failed, error %d %s\n", rc, mdb_strerror(rc));
        goto txn_abort;
    }
    rc = mdb_cursor_open(txn, dbi, &mc);
    if (rc) {
        fprintf(stderr, "mdb_cursor_open failed, error %d %s\n", rc, mdb_strerror(rc));
        goto txn_abort;
    }

    gettimeofday(&tv1, NULL);
    
    cnt_line = 0;
    while(fgets(string, LINE_SIZE, stdin) != NULL) {
        size = strlen(string);
        if(string[size-1] == '\n'){
            string[size-1] = '\0';
            --size;
        }
        if(size > 1 && string[size-1] == '\r'){
            string[size-1] = '\0';
            --size;
        }
        if(string[0] == '\0')
            continue;

        if(cnt_line % 10000 == 0)
            fprintf(stderr,"[linecount]\t%d\n",cnt_line);

        /*
        token = strtok_r(string, "\t", &save);
        if(token != NULL) {
            strcpy(s_key, token);
            token = strtok_r(NULL, "\t", &save);
            if(token != NULL) {
                strcpy(s_value, token);
            } else continue;
        } else continue;
        */
        token = strtok_r(string, "\t", &save);
        if(token != NULL) {
            strcpy(s_key, token);
        } else continue;
        
        key.mv_data = s_key;
        key.mv_size = strlen(s_key) + 1;

        rc = mdb_get(txn, dbi, &key, &data);
        if(!rc) {
            fprintf(stdout, "%s\t%s\n", s_key, (char*)data.mv_data);
        }

        cnt_line++;
    }
    gettimeofday(&tv2, NULL);
    fprintf(stderr, "<-end > : t2.sec = %d t2.usec = %d\n",(int)tv2.tv_sec,(int)tv2.tv_usec);
    fprintf(stderr, "<+time> : sec = %d usec = %d\n",(int)(tv2.tv_sec-tv1.tv_sec),(int)(tv2.tv_usec-tv1.tv_usec));

    rc = mdb_txn_commit(txn);
    if(rc) {
        fprintf(stderr, "%s: txn_commit fail: %s\n", prog, mdb_strerror(rc));
        goto env_close;
    }
    mdb_dbi_close(env, dbi);

txn_abort:
    mdb_txn_abort(txn);
env_close:
    mdb_env_close(env);

    return rc ? EXIT_FAILURE : EXIT_SUCCESS;

}
