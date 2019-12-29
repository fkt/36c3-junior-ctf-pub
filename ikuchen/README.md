# IKuchen

## Public Info

Somehow our cat 🐈 ate all the .py. And some letters, too...
Who needs brackets, anyway?

### Port

5656

### Level

Medium

## Internals

### Info

This is an IPython jail.
The one main thing to find is that IPython treats inputs as functions if they are prepended with a slash.
From there, it is straight forward: encode with "%c", then open flag.txt and print it.

### Flag

36c3{IPython_jails_are_EASY_2_secu__cthulhu}