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

The usage workflow intended is:
1. Create an instance with passing in the cloud and authentication options.
2. Initiate communication with the `comms()` method.
3. Use the `resource()` method or 

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

**Ex. 1: Using a token**

In below example a token `thetoken` is used with the US cloud. You can create a user token by following [these instructions](https://www.mist.com/documentation/using-postman/)
```python
>>> mist = MMClient(token="thetoken")
```
An alternative with specifying the EU cloud would be.
```python
>>> mist = MMClient(cloud="EU", token="thetoken")
```

**Usage without the token.**

In this case you are asked for username and password or you can provide one or both or neither when creating a new instance.

```python
>>> mist = MMClient()
```

```python
>>> mist = MMClient(cloud='us', username="theuser@mistifi.com")
```
Currently 2FA and OAUTH aren't supported.

