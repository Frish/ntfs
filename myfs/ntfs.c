#include <tcutil.h>
#include <tcadb.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

typedef struct {
  char *name;
  char *key_time;
} TCDDB;

TCADB *openadb(const char *dbname){
    TCADB *adb = tcadbnew();
    if(!tcadbopen(adb, dbname)) {
        fprintf(stderr, "open error: %s\n", dbname);
    }
    return adb;
}
int closeadb(TCADB *adb){
    if(!tcadbclose(adb)){
        fprintf(stderr, "close error:");
        return 0;
    }
    tcadbdel(adb);
    return 1;
}

bool create_folder(const char *name){
    struct stat sbuf;
    if(stat(name, &sbuf) == 0){
        if(!S_ISDIR(sbuf.st_mode)) return false;
    } else {
        if(mkdir(name, 0755) != 0) return false;
    }
    return true;
}

/* キーからファイルパスを作るユーティリティ */
static char *makepath(TCDDB *ddb, const void *kbuf, int ksiz){
  char *uenc = (char *)tcmemdup(kbuf, ksiz);
  char *delims = "_";
  int i;
  TCLIST *keys = tcstrsplit(uenc,delims);
  if(tclistnum(keys)!=3){
      fprintf(stderr, "keys is not 3 is %d\n", tclistnum(keys));
      return 0;
  }
  char *hash_folder = tclistval2(keys, 0);
  char *path = tcsprintf("%s/%s",ddb->name, hash_folder);
  if(!create_folder(path))return false;
  char *hash_db = tclistval2(keys, 1);
  ddb->key_time = tcurldecode(tclistval2(keys, 2),&i);
  char *allpath = tcsprintf("%s/%s.tch#mode=wc",path,hash_db);
  tcfree(uenc);
  tcfree(keys);
  return allpath;
}

/* コンストラクタの実装 */
static TCDDB *tcddbnew(void){
  TCDDB *ddb = tcmalloc(sizeof(*ddb));
  ddb->name = NULL;
  return ddb;
}

/* デストラクタの実装 */
static void tcddbdel(TCDDB *ddb){
  tcfree(ddb);
}

/* openメソッドの実装 */
static bool tcddbopen(TCDDB *ddb, const char *name){
  if(!create_folder(name)) return false;
  ddb->name = tcstrdup(name);
  return true;
}

/* closeメソッドの実装 */
static bool tcddbclose(TCDDB *ddb){
  tcfree(ddb->name);
  return true;
}

/* putメソッドの実装 */
static bool tcddbput(TCDDB *ddb, const void *kbuf, int ksiz, const void *vbuf, int vsiz){
  bool err = false;
  char *path = makepath(ddb, kbuf, ksiz);
  if(!path)return err;
  char *value = (char *)tcmemdup(vbuf,vsiz);
  TCADB *adb = openadb(path);
  tcadbput2(adb, ddb->key_time, value);
  closeadb(adb);
  tcfree(path);
  return !err;
}

/* getメソッドの実装 */
static void *tcddbget(TCDDB *ddb, const void *kbuf, int ksiz, int *sp){
  void *vbuf;
  char *path = makepath(ddb, kbuf, ksiz);
  if(!path)return 0;
  TCADB *adb = openadb(path);
  int new_kiz = strlen(ddb->key_time);
  vbuf = tcadbget(adb,tcmemdup(ddb->key_time,new_kiz),new_kiz,sp);
  closeadb(adb);
  tcfree(path);
  return vbuf;
}

/* ライブラリを初期化して、実装をオーバーライドする */
bool initialize(ADBSKEL *skel){
  skel->opq = tcddbnew();
  skel->del = (void (*)(void *))tcddbdel;
  skel->open = (bool (*)(void *, const char *))tcddbopen;
  skel->close = (bool (*)(void *))tcddbclose;
  skel->put = (bool (*)(void *, const void *, int, const void *, int))tcddbput;
  skel->get = (void *(*)(void *, const void *, int, int *))tcddbget;
  return true;
}