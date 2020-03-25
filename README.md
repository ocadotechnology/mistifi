# Mistifi

Is a RESTAPI client used for interfacing with Mist (Juniper) API.

## Motivation


# Installation

The module can be pip installed

```shell
$ pip install mistifi
```
or using `pip3` if using python3.

# Usage examples

**Use with a token**

```python
>>> mist = MMClient(token="thetoken")
>>> mist.comms()
```
**Usage without the token.**

In this case you are asked for username and password or you can provide one or both when creating a new instance.

```python
>>> mist = MMClient(username="theuser")
>>> mist.comms()
```
Currently 2FA and OAUTH aren't supported.
