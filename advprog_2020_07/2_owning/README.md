# Owning The Abstractions

A key idea of data abstraction is that interfaces are often more
important than implementation. As long as applications use the
interface, the internal implementation can change without breaking the
rest of the code.

This project twists this idea in a slightly different direction. As
programmers, we're often at the mercy of what libraries and frameworks
provide.  It is tempting to write code that directly interacts with a
library.  However, in doing so, you introduce a hard-dependency into
your application--that is, your application becomes inseparable from
the libraries on which it depends.

Instead of directly depending on libraries, a different approach is to
create your own abstractions.  In essence, you think hard about how
you would ideally want some aspect of your program to work, and then
you create abstractions that mirror that.  Afterwards, you build a
concrete implementation using existing libraries and frameworks.

It's subtle, but this approach gives you ownership of an abstraction.
In turn, ownership gives you power. You can port your application
to new platforms, choose different libraries, and change your mind
later.

For this project, we're going to briefly explore this idea.
To start, go to the file `report.py`.   Then work on the
exercises in `ex1.py`-`ex4.py`.

## Making Custom Containers

A parts of this project involves making custom containers that are
"list-like" or "dict-like." This is commonly done by implementing
classes with one or more of the following magic methods:

```
a[index]            # a.__getitem__(index)
a[index] = value    # a.__setitem__(index, value)
del a[index]        # a.__delitem__(index)

len(a)              # a.__len__()
x in a              # a.__contains__(x)

for x in a:         # i = a.__iter__(), i.__next__()
    ...
```

It might also be necessary to redefine object attribute access:

```
a.attr              # a.__getattribute__("attr")
a.attr = value      # a.__setattr__("attr", value)
del a.attr          # a.__delattr__("attr")
```


