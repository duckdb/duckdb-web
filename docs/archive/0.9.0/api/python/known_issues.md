---
layout: docu
title: Known Python Issues
---

Unfortunately there are some issues that are either beyond our control or are very elusive / hard to track down.  
Below is a list of these issues that you might have to be aware of, depending on your workflow.  

## Numpy Import Multithreading

When making use of multi threading and fetching results either directly as Numpy arrays or indirectly through a Pandas DataFrame, it might be necessary to ensure that `numpy.core.multiarray` is imported.  
If this module has not been imported from the main thread, and a different thread during execution attempts to import it this causes either a deadlock or a crash.  

To avoid this, it's recommended to `import numpy.core.multiarray` before starting up threads.