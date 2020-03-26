# Mistifi

Is a RESTAPI client used for interfacing with Mist (Juniper) API.

## Motivation


# Installation

The module can be pip installed

```
pip install mistifi
```
or using `pip3` if using python3.

The module is imported with
```python
import mistifi
```

# Usage

When creating an instance pass in the `cloud` option to specify a direct instance of a cloud. If not passed in, the default `US` will be used.

## Selecting a cloud
There are currently two cloud options to select from. Either `EU` or `US`, with `US` being the default if not provided with the `cloud` attribute.
They default to
- US = api.mist.com
- EU = api.eu.mist.com
**Ex. 1: Using the default `US` cloud**
```python
>>> mist = MMClient()
```
**Ex. 2: Specifying the `EU` cloud**
```python
>>> mist = MMClient(cloud="EU")
```
Note that using either caps or not for the value will work. In the below example the `US` cloud will be used.
```python
>>> mist = MMClient(cloud="us")
```
## Using a token or username/password

**Ex. 1: Use with a token**

In below example token is used with the US cloud.
```python
>>> mist = MMClient(token="thetoken")
```
An alternative with specifying the EU cloud would be.
```python
>>> mist = MMClient(cloud="EU", token="thetoken")
```

**Usage without the token.**

In this case you are asked for username and password or you can provide one or both or none when creating a new instance.

```python
>>> mist = MMClient(cloud='us')
>>> mist.comms()
```

```python
>>> mist = MMClient(cloud='us', username="theuser@mistifi.com")
>>> mist.comms()
```
Currently 2FA and OAUTH aren't supported.
