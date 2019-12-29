#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

void before(void) __attribute__ ((constructor));
void after(void) __attribute__ ((destructor));

char whoop[] = "junior-totally_the_flag_or_maybe_not";
char arg[]   = "                                    ";
char who[] = \
"\x00\x1e" \
"\x00\x1a" \
"\x00\x00" \
"\x00""6" \
"\x00""\n" \
"\x00\x10" \
"\x00""T" \
"\x00\x00" \
"\x00\x01" \
"\x00""3" \
"\x00\x17" \
"\x00\x1c" \
"\x00\x00" \
"\x00""\t" \
"\x00\x14" \
"\x00\x1e" \
"\x00""9" \
"\x00""4" \
"\x00""*" \
"\x00\x05" \
"\x00\x04" \
"\x00\x04" \
"\x00""\t" \
"\x00""=" \
"\x00\x03" \
"\x00\x17" \
"\x00""<" \
"\x00\x05" \
"\x00"">" \
"\x00\x14" \
"\x00\x03" \
"\x00\x03" \
"\x00""6" \
"\x00\x0f" \
"\x00""N" \
"\x00""U";

void before(void)
{
    for(int i = 0; i < 36; i++) {
      whoop[i] = whoop[35-i];
    }
}

void after(void)
{
  for(int i = 0; i < 36; i++) {
    whoop[i] ^= arg[i];
  }

  int cor = 1;
  for(int i = 0; i < 36; i++) {
    if(whoop[i] != who[2*i+1])
      cor = 0;
  }
  sleep(10);
  printf("aber es ist nur noch eine sache von sekunden!\n");
  if (cor)
    printf("correct!\n");
}

int main(int argc, char **argv)
{
  for(int i = 0; i < 36; i++) {
    whoop[i + 64] = argv[1][i];
    // nops
    whoop[i] = (100 + (whoop[i] % 256) + 156) % 128;
    int div = 32;
    div += 1;
    div *= 1;
    whoop[i] = whoop[i] ^ ((uint32_t)whoop[i]) << (div / 7) << 29;
    // end nops
  }
  if(whoop == "this_should_totally_be_a_hering_on_a_kuchenblech")
    printf("correct!\n");
  else
    printf("wrong!\n");
  return 0;
}


