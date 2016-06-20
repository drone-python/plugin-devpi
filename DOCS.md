Use the devpi plugin to deploy a Python package to a [devpi](http://doc.devpi.net) server.

**Note: Your setup.py will be ran interpreted Python 3.5 during packaging.**

* `server` - The full path to the root of the devpi server. Make sure to include a port if it's not 80 or 443.
* `index` - The ``<user>/<repo>`` combo designating the index to upload to.
* `username` - The username to login with.
* `password` - A password to login with.
* `package_path` - (Optional) If you want to upload a package in a directory other than the workspace root, pass that in here. Shouldn't normally need to do this.

The following is an example configuration for your .drone.yml:

```yaml
pipeline:
  devpi:
    image: dronepython/plugin-devpi:latest
    server: http://devpi.bigco.com:3141/
    index: root/production
    username: guido
    password: secret
```
