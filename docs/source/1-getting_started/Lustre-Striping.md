.. highlight:: rst

Lustre Striping
===============

As a rough guideline, the only valid use case for Lustre striping is on very large files of O(300 GiB) and above, and even then, only when combined with i/o intensive workloads.

This is an especially niche case because excessively large files are always unwieldy (take a long time to load; are hard to cache) and should be avoided, regardless of striping.

Pros:
-----

- Having a >O(300 GiB) read-intensive file striped across multiple OSS's means more OSS ram can be used to cache it, leading to much higher performance (ie. it's read from ram cache instead of disk) when being read from 100's of jobs at once. (Note that striping indexes must be 10 or more apart (for /fred) to be on different OSS's; just different OSTs is not enough).
- Striping on vast O(TiB) files helps keep OST disk space more even.
- Ideally a large >O(10 Gib) striped file will read or write quicker than an unstriped file, and this works in ideal benchmarks, but not often in reality because of many of the factors listed below.

Cons (even on large files):
---------------------------

- Excessive (too many files, or too many users, or too small files) use of 'lfs setstripe' results in i/o amplification to Lustre servers (ie. all OSTs in the file need to be contacted and to perform i/o, not just one) and these streams interfere with other i/o, leading to poorer i/o for everyone, including especially the codes using striped files. Disks are slow at seeking and 10x more i/o streams means >10x slower i/o per stream from the OST as a while.
- A striped file will be limited by the speed of the slowest of its OSTs. Individual OSTs are often busy, leading to erratic and often much slower than ideal performance for striped files. Striping looks good on idle systems or in benchmarks, but not on a busy machine in the real world.
- The more striped files there are the busier and slower all the OSTs are. (See first point).
- OST inodes increase with striping - 4 stripes = 4x as many OST inodes. Filesystems have run out of inodes before. To be avoided. This happened with ldiskfs/ext4 on g2. Unlikely to happen with ZFS.
- Widely striped small O(< 1 GiB) files turn into tiny files. i/o speeds to tiny files is always poor. (See above re: seeking)
- Probability of files being lost if an OST dies is increased proportionally to striping. ie. 4 stripes = 4x more likely to lose the file in the (extremely unlikely) case of a total OST loss.
