# Magicaltavern API Documentation

This document will guide you through the Magicaltavern APIs' Usage, available request routes and
authentication methods.

## Authentication

Some API routes and request methods are protected. This means, that to use them, you will
have to provide an API key in your request.

### Properly authenticating

Provide your API key as an attribute named `token` in the request header.

### Checking your token

You can check the validity of your token by trying to authenticate under the route `/api/v2.0/auth`.
You will receive a `200 - OK` response if you authenticated correctly.

## Routes

### Campaigns

|Route                      |Method |Description    |Protected  |
|---                        |---    |---            |---        |
|/api/v2.0/campaigns        |GET    | Returns all stored campaigns, formatted as .json. The `key` in the `key`-`value`-pair is the campaigns' unique ID. | Yes |
|/api/v2.0/campaigns/\<id>  |GET    | Returns the campaign which's `key` matches the supplied `id`, formatted as .json. | Yes |
