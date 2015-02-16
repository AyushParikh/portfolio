/*

This program takes two arguments, the first is a .wav file to open and the second is a .wav file to write
    the audio of the first without the vocal track.

I.e. $ remvocals vocals.wav novocals.wav

*/

#include <stdio.h>
#include <stdlib.h>

#define HEADER_SIZE 11

int main (int argc, char **argv) {
    // Check that the number of inputs match the expectations
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <src filename> <dest filename>\n",argv[0]);
        exit(1);
    }
    FILE *src,*dest;
    short left,right;
    src = fopen(argv[1], "r");
    dest = fopen(argv[2], "w+");
    if ((src == NULL)||(dest == NULL)) {
        fprintf(stderr,"error: file failed to open");
        exit(1);
    }
    
    long l,r;
    int header[HEADER_SIZE];
    // Write the .wav file header over to our new file
    fread(&header,sizeof(int),HEADER_SIZE,src);
    fwrite(&header,sizeof(int),HEADER_SIZE,dest);
    while (((l = fread(&left,sizeof(short),1,src)) != NULL) && ((r = fread(&right,sizeof(short),1,src)) != NULL)) {
        // Take the difference between the 2 channels, leaving only the background audio
        short newbytes = (left - right) / 2;
        fwrite(&newbytes,sizeof(newbytes),1,dest);
        fwrite(&newbytes,sizeof(newbytes),1,dest);
    }
    fclose(src);
    fclose(dest);
    return 0;
}

