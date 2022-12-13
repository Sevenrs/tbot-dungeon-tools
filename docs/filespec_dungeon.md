# The dungeon.bin file specification

The dungeon file starts with the amount of dungeon scripts at the 12th byte, followed by the dungeon script names 
which are at most 260 bytes. Those script names end with ".dun".

After that, the length in bytes is defined per script. I still need to investigate this part, but I believe
it is the data length for each script in the dungeon file.

Every script is formatted like this:

29 B9 only on the first iteration
(29 B9/FF FF) FF FF FE FF FF FF (length) FF FF

1. The amount of spawn points. This means the amount of enemies that are defined in the script, ending with 0x0D, 0x0A
2. For every spawn point, we have the spawn index followed by the monster number. The index is separated with the value with byte 0x09 and the iteration ends with 0x0D, 0x0A, 0x09

3. After that, the amount of "blocks" is defined. Blocks are sections of the map. This is ended with 0x0D, 0x0A.
4. [info 01] Per block a left top right and bottom is defined as block rect, each value separated by 0x09 and ended with 0x0D, 0x0A
5. [info 02] Array of enemies that appear in this block, separated by 0x09 and ended with 0x0D, 0x0A. Maximum of 13 values.
6. [info 03] Array of enemies that respawn forever, separated by 0x09 and ended with 0x0D, 0x0A. Maximum of 13 values.
7. [info 04] Clear condition spawn list, separated by 0x09 and ended with 0x0D, 0x0A. Maximum of 13 values. This contains all the enemies that need to be killed in order to progress.
8. [info 05] "VIP", separated by 0x09 and ended with 0x0D, 0x0A. Maximum of 13 values. This contains a list of enemies that can be killed. If one of those enemies are killed, the block is finished automatically.
9. [info 06] Exceptional spawn array. Enemies in this array do not die when the block is cleared, separated by 0x09 and ended with 0x0D, 0x0A. Maximum of 13 values.
10. [info 07] Yellow text. Ended with 0x0D, 0x0A
11. [info 08] Countdown. Amount of seconds the player has before the level is lost. Ended with 0x0D, 0x0A

The last block ends with 0D 0A FF FF FF FF

- I am 100% sure that the enemy spawning locations are defined in the .map file itself