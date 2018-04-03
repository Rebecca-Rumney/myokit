# Contributing to Myokit

Contributions to Myokit are very welcome! To streamline our work, please have a look at the guidelines below!

We use [GIT](https://en.wikipedia.org/wiki/Git) and [GitHub](https://en.wikipedia.org/wiki/GitHub) to coordinate our work. When making any kind of update, try to follow the procedure below.

### A. Setting up your system

1. If you're planning to contribute to Myokit, don't check out the repo directly, but create a [fork](https://help.github.com/articles/fork-a-repo/) and then [clone](https://help.github.com/articles/cloning-a-repository/) it onto your local system .
2. Install Myokit in development mode, with `$ python setup.py develop`.
3. [Test](#testing) if everything's working, using the test script: `$ python test/unit-main.py`.

If you run into any issues at this stage, please discuss them with us on Github!

### B. Getting started on an issue

4. Before doing any coding, create a GitHub [issue](https://guides.github.com/features/issues/) so that new ideas can be discussed.
5. Now create a [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/) for the issue you're going to work on. Using branches lets us test out new changes without changing the main repository.

You now have everything you need to start making changes!

### C. Writing your code

6. Commit your changes to your branch with useful, descriptive commit messages: Remember these are publically visible and should still make sense a few months ahead in time. While developing, you can keep using the github issue you're working on as a place for discussion. [Refer to your commits](https://stackoverflow.com/questions/8910271/how-can-i-reference-a-commit-in-an-issue-comment-on-github) when discussing specific lines of code.
7. If you want to add a dependency on another library, or re-use code you found somewhere else, have a look at [these guidelines](#dependencies-and-reusing-code).

### D. Finishing touches

8. Please check your code conforms to the [coding style guidelines](#coding-style-guidelines).
9. [Test your code!](#testing)
10. Myokit has online documentation at http://docs.myokit.org/. To make sure any new methods or classes you added show up there, please read the [documentation](#documentation) section.

### E. Merging changes

11. When you feel your code is finished, or at least warrants serious discussion, create a [pull request](https://help.github.com/articles/about-pull-requests/) (PR).
12. Once a PR has been created, it will be reviewed, discussed, and if all goes well it'll be merged into the main source code!

Thanks!





## Installation

Myokit can be installed into your Python system, using

```
$ python setup.py develop
```

This will tell other Python modules where to find Myokit, so that you can use `import myokit` anywhere on your system.






## Coding style guidelines

Myokit is written in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)), with occassional bits of (ansi) [C](https://en.wikipedia.org/wiki/ANSI_C). It uses [CVODE](https://computation.llnl.gov/projects/sundials/cvode) for simulations, and [NumPy](https://en.wikipedia.org/wiki/NumPy) for pre- and post-processing.

For the Python bits, Myokit follows the [PEP8 recommendations](https://www.python.org/dev/peps/pep-0008/) for coding style. These are very common guidelines, and community tools have been developed to check how well projects implement them.

We use [flake8](http://flake8.pycqa.org/en/latest/) to check our PEP8 adherence. To try this on your system, navigate to the Myokit directory in a console and type

```
$ flake8
```

### Naming

Naming is hard. In general, we aim for descriptive class, method, and argument names. Avoid abbreviations when possible without making names overly long.

Class names are CamelCase, and start with an upper case letter, for example `SuperDuperSimulation`. Method and variable names are lower case, and use underscores for word separation, for example `x` or `iteration_count`.

### Python 2 and 3

Myokit is currently only for Python 2, but several issues are open concerning a transition to [code that works in both 2 and 3](http://python-future.org/compatible_idioms.html).






## Dependencies and reusing code

While it's a bad idea to reinvent the wheel, making code that's easy to install and use on different systems gets harder the more dependencies you include. For this reason, we try to limit Myokit's dependencies to the bare necessities. This is a matter of preference / judgement call, so best to discuss these matters on GitHub whenever you feel a new dependency should be added!

Direct inclusion of code from other packages is possible, as long as their license permits it and is compatible with ours, but again should be considered carefully and discussed first. Snippets from blogs and stackoverflow can often be included without attribution, but if they solve a particularly nasty problem (or are very hard to read) it's often a good idea to attribute (and document) them, by making a comment with a link in the source code.

### Matplotlib

Myokit includes plotting methods, _but_, these should never be vital for its functioning, so that users are free to use Myokit with other plotting libraries.

Secondly, Matplotlib should never be imported at the module level, but always inside methods. This means that the `myokit` module can be imported without Matplotlib being installed, and used as long as not Matplotlib reliant methods are called.






## Testing

Myokit uses the [unittest](https://docs.python.org/3.3/library/unittest.html) package for tests.

To run tests, use

```
$ python test/unit-main.py
```

If you have OpenCL installed, use

```
$ python test/unit-full.py
```





## Documentation

Every method and every class should have a [docstring](https://www.python.org/dev/peps/pep-0257/) that describes in plain terms what it does, and what the expected input and output is.

These docstrings can be fairly simple, but can also make use of [reStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html), a markup language designed specifically for writing [technical documentation](https://en.wikipedia.org/wiki/ReStructuredText). For example, you can link to other classes and methods by writing ```:class:`myokit.Model` ``` and  ```:meth:`run()` ```.

In addition, we write a (very) small bit of documentation in separate reStructuredText files in the `doc` directory. Most of what these files do is simply import docstrings from the source code. But they also do things like add tables and indexes. If you've added a new class to a module, search the `doc` directory for the appropriate `.rst` file and add your class.

Using [Sphinx](http://www.sphinx-doc.org/en/stable/) the documentation in `doc` can be converted to HTML, PDF, and other formats. In particular, we use it to generate the documentation on http://docs.myokit.org/

### Building the documentation

To test and debug the documentation, it's best to build it locally. To do this, make sure you have the relevant dependencies installed (see above), navigate to your Myokit directory in a console, and then type:

```
cd doc
make clean
make html
```

Next, open a browser, and navigate to your local Myokit directory (by typing the path, or part of the path into your location bar). Then have a look at `<your myokit path>/doc/build/html/index.html`.

