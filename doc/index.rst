progress-passthrough
====================

Utilities to pass progress information through nested iterators.

Quick Example
-------------

The use case which inspired this is using progress bars like
`tqdm <https://github.com/tqdm/tqdm>`_ on "filtering generators" (think ``(x
for x in l if some_condition(x))``) and wanting the progress to follow the
iteration over the inner (unfiltered) iterable instead of the filtered
iterations.

Consider e.g.:

.. invisible-code-block: python

   # don't waste time on sleeping in doctests:
   from unittest.mock import patch
   sleep_patch = patch("time.sleep").__enter__()

.. code:: python

   from dataclasses import dataclass
   from time import sleep
   from tqdm import tqdm

   @dataclass
   class slow_range:
      """
      Range with simulated delay so progress bar doesn't fill up instantly.
      """
      n: int

      def __iter__(self):
         for x in range(self.n):
            sleep(0.01)
            yield x

      def __len__(self):
         return self.n

   r = slow_range(100)

   filtering_gen = (x for x in r if x % 37 == 0)

   results = list(tqdm(filtering_gen))

This a) doesn't produce a progress bar because the length of the generator
output isn't known and b) even if it did, it would be choppier than it needs to
be because only filtered iterations move the bar, not iterations of the
original source iterable (``r``).

This library allows solving the issue in a generic manner that does not tie the
user down to a specific progress bar:

.. code:: python

   from progress_passthrough.iterator_wrappers import wrap_source

   r = slow_range(100)

   # wrap r in several wrappers that together provide the functionality of this
   # library (see below)
   source_preserving_r = wrap_source(r)

   # construct a generator and wrap it so that the original iterable (r) can
   # still be accessed
   filtering_gen = source_preserving_r.wrap(
       x for x in source_preserving_r if x % 37 == 0
   )

   # attach a callback which updates tqdm on each iteration of r to one of the
   # inner wrappers around it, then iterate
   with tqdm(total=len(filtering_gen.source)) as t:
     filtering_gen.source.callbacks.append(t.update)
     results = list(filtering_gen)

While this all works independently of the specific progress bar library used,
this package comes with a few convenient classes for tqdm specifically
(available after installing the ``tqdm`` extra, see :ref:`Progress bar specific
extras`) that let us not have to worry about setting up the callback:

.. code:: python

   from progress_passthrough.tqdm import TqdmOnSource

   # same setup as above
   r = slow_range(100)
   source_preserving_r = wrap_source(r)
   filtering_gen = source_preserving_r.wrap(
       x for x in source_preserving_r if x % 37 == 0
   )

   # let library set up the source callback (returns instance of tqdm subclass)
   t = TqdmOnSource(filtering_gen)

   # perform iteration
   results = list(t)

.. invisible-code-block: python

   # undo patch
   sleep_patch.__exit__()


Table of contents
-----------------

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   installation
   api/index


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
