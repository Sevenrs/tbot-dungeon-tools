## The .map file specification

.val        = collisions
0000.obj    = main object

### File header
1. [Offset 0x00 to 0x00] - 1 byte for the grid scale. It is always equal to `0x40` (64)
2. [Offset 0x01 to 0x04] - Grid length :: long/4 bytes
3. [Offset 0x05 to 0x08] - Grid height :: long/4 bytes
4. [Offset 0x09 to 0x0A] - Unknown, always `0x01, 0x00`. :: unsigned short/2 bytes

5. [Offset 0x0B to 0x0B] - 1 byte indicating the obj file count.
6. [Offset 0x0C to 0x0C] - 1 byte indicating the val file count.
7. [Offset 0x0D to 0x0D] - 1 byte indicating the flu file count.

8. [Offset 0x0E to 0x0E] - 1 byte indicating the number of objs which are stored in bones
9. [Offset 0x0F to 0x0F] - 1 byte indicating the val file count (again).
10. [Offset 0x10 to 0x10] - 1 byte indicating the flu file count (again).

11. [Offset 0x11 to 0x11] - Unknown data consisting of 1 byte. Either `0x00` or `0x01`.
12. [Offset 0x12 to 0x15] - Number of monster spawns. All maps have 136 spawns allocated, which is the max (aka: `MAX_INDEX`). (`0x88`) :: long/4 bytes

13. [Offset 0x16 to 0x43] - Array of null bytes, always consistent throughout every .map file I have looked at.
14. [Offset 0x44 to 0x47] - Unknown :: long/4 bytes, can be filled with null bytes.
15. [Offset 0x48 to 0x4B] - Length of the JPEG/JFIF file. Always equal to 1651 (`0x73, 0x06, 0x00, 0x00`) :: long/4 bytes

### Image
For some reason every .map file contains a JPEG/JFIF consisting of 1651 bytes. It is always the same in every single file.
It looks to be a black image. Size is 256x256. There's not much else to say about it.

### Files
For every file in the map directory:
1. The file name is appended, for example: `0000.val` and encoded in `utf-8`.
2. Append (`1024 - len(file_name)`) amount of null bytes to the buffer

