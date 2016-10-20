# Read the Docs Docker image

This image includes tools for building Read the Docs documentation for PHP projects.


## Usage

Run the following commands in order to build the documentation:

``` bash
$ docker run --rm -it -v "$PWD":/doc webplates/readthedocs
$ # You are now in the docker image
$ make html
$ make spelling
```

Alternatively you can run the commands directly from the host without entering the container shell:

``` bash
$ docker run --rm -t -v "$PWD":/doc webplates/readthedocs make html
$ docker run --rm -t -v "$PWD":/doc webplates/readthedocs make spelling
```

There are also simple shortcuts for the two commands above:

``` bash
$ docker run --rm -t -v "$PWD":/doc webplates/readthedocs build
$ docker run --rm -t -v "$PWD":/doc webplates/readthedocs check
```

Last, but not least there is a watch command to watch for changes:

``` bash
$ docker run --rm -t -v "$PWD":/doc webplates/readthedocs watch
```

## Shell support

Typing the above commands is not really convenient. With a simple alias you can
simplify the executed commands:

``` bash
alias doc='docker run --rm -t -v "$PWD":/doc webplates/readthedocs'
```

(Put this in your shell startup script: `~/.bashrc`, `~/.zshrc`, etc)


Then the commands again:

``` bash
$ doc build
$ doc check
$ doc watch
```


## Note about permissions

Unless configured otherwise Docker containers run processes with `root` user.
Furthermore the `root` user inside containers is also not "mapped" to any other user
on host machines by default, although [it is possible](https://docs.docker.com/engine/security/security/).

These facts usually end up in permission issues on the host machine.
In order to mitigate this problem this container comes with a UID/GID hack and
[su-exec](https://github.com/ncopa/su-exec).

In short: the user running in the container gets the UID from the HOST computer.

In most cases it should work fine, but it could cause some issues when the
host UID is already taken in the container.
