/*

This program take two parameters and has two options. The first is a source filename, the second is a destination filename.
    The first option (-d) is a delay in samples for the added echo track, the second (-v) is the factor to divide the echo track by.

I.e. $ addecho -d 5 -v 4 src.wav dest.wav

*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define HEADER_SIZE 11

int main (int argc, char **argv) {
    if ((argc < 3)||(argc > 7)) {
        fprintf(stderr, "Usage: %s [-d delay] [-v volume_scale] <src filename> <dest filename>\n",argv[0]);
        exit(1);
    }


    int arg_check;
    int v = 4;
    int d = 8000;
    while ((arg_check = getopt(argc,argv,"d:v:")) != -1) {
        switch(arg_check){
            case 100: d = strtol(optarg,NULL,10);
            case 118: v = strtol(optarg,NULL,10); break;
            default:
                      fprintf(stderr,"Error: please enter valid options.\n");
                      exit(1);
        }
    }


    int header[HEADER_SIZE];
    FILE *src,*dest;
    src = fopen(argv[argc-2],"r");
    dest = fopen(argv[argc-1],"w+");
    if ((src == NULL)||(dest == NULL)) {
        fprintf(stderr,"error: file failed to open");
        exit(1);
    }
    fread(&header,sizeof(int),HEADER_SIZE,src);
    header[1] = header[1] + (d*2);
    header[10] = header[10] + (d*2);
    fwrite(&header,sizeof(int),HEADER_SIZE,dest);
    
    
    int samplecount = 0;
    int read_check;
    short sample;
    short echo_buffer[d];
    for (int i=0;i<d;i++) {
        if ((read_check = fread(&sample,sizeof(short),1,src))!=NULL) {
            echo_buffer[i] = sample;
            fwrite(&sample,sizeof(sample),1,dest);
            samplecount++;
        }
        else {
            echo_buffer[i] = NULL;
            short pad = 0;
            fwrite(&pad,sizeof(short),1,dest);
        }
    }
    int i=0;
    while ((read_check = fread(&sample,sizeof(short),1,src))!=NULL) {
        short temp_samp = echo_buffer[i%d];
        echo_buffer[i%d] = sample;
        short new_sample = sample + (temp_samp/v);
        fwrite(&new_sample,sizeof(short),1,dest);
        i++;
    }
    for (int m = i%d;m<d;m++) {
        short new_sample = echo_buffer[m]/v;
        if (m < samplecount) {
            fwrite(&new_sample,sizeof(short),1,dest);
        }
    }
    for (int m=0;m<(i%d);m++) {
        short new_sample = echo_buffer[m]/v;
        if (m < samplecount) {
            fwrite(&new_sample,sizeof(short),1,dest);
        }
    }
    fclose(src);
    fclose(dest);
    return 0;
}
