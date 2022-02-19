# Contributing guide

Cogreqs doesn't try to fix Python packaging. Instead it tries to patch up the leaking bucket that is Python packaging with a thousand pieces of tape.

That is to say, if you want to contribute a piece of tape (please do!) it doesn't have to be perfect. A simple one-sentence GitHub issue is enough -- quantity trumps quality!

## Local development

To build cogreqs in development mode locally, run

```
$ make dev
```

This will install cogreqs symlinked to your cogreqs working directory.

## Local testing

To test the package, run

```
$ make test
```

## Submit a PR

Please run [black](https://github.com/psf/black) on the repo before opening a PR.

```
$ black .
```

Then open a PR, and explain what your change does in the description.

## Release a new version

If you're a maintainer of cogreqs, this is how yourelease a new PyPI version:

1. Bump the `version` in setup.py
2. Commit the version bump to the `main` branch
3. Put a new tag on the main branch that matches the version, with a `v` prefix. For example, if the new version is `version="0.1.7"`, the tag becomes `v0.1.7`
4. Push the tag to GitHub

This will automatically build and release a new PyPI version
