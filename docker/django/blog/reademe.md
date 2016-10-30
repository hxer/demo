## docker for blog with django

use Dockerfile to auto build

code from [https://github.com/hxer/exercise/tree/master/django/blog][1]

[1]: https://github.com/hxer/exercise/tree/master/django/blog


* build

```
docker build -t django:blog .
```

* run

```
docker run -d -p 8000:8000 --name blog django:blog
```

* visit

firefox> ip:8000
