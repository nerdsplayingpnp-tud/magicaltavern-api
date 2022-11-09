# Magicaltavern API Documentation

This document will guide you through the Magicaltavern APIs' Usage, available request routes and
authentication methods.

## Authentication

Some API routes and request methods are protected. This means, that to use them, you will
have to provide an API key in your request.

### Properly authenticating

Provide your API key as an attribute named `token` in the requests' header.

### Checking your token

You can check the validity of your token by trying to authenticate under the route `/api/v2.0/auth`.
You will receive a `200 - OK` response if you authenticated correctly.

## Routes

### Campaigns

| Route                     | Method | Description                                                                                                                                                                                        | Protected |
|---------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| /api/v2.0/campaigns       | GET    | Returns all stored campaigns, formatted as .json. The `key` in the `key`-`value`-pair is the campaigns' unique ID.                                                                                 | Yes       |
| /api/v2.0/campaigns       | POST   | Adds a new campaign entry to the database. Data has to be in json-format and located in the request body. The following data needs to be supplied: [Adding a new Campaign](#adding-a-new-campaign) |           |
| /api/v2.0/campaigns/\<id> | GET    | Returns the campaign which's `key` matches the supplied `id`, formatted as .json.                                                                                                                  | Yes       |

## PUTting and POSTing Data

### Adding a new Campaign

Adding a new campaign can be done by using the Route defined in [Routes > Campaigns](#campaigns). You can include the following data in the request body:

```json
{
    "name": String,
    "description": String,
    "players_min": int,
    "players_max": int,
    "complexity": int range 0-2,
    "place": String,
    "time": String,
    "content_warnings": String,
    "ruleset": int ForeignKey("ruleset.id"),
    "campaign_length": int range 0-2,
    "language": int range 0-2,
    "character_creation": String,
    "briefing": String,
    "notes": String,
    "image_url": optional String
}
```

#### Explaining Campaign parameters

Most of the parameters, such as name, description, notes etc. should be pretty self-explanatory. However, some parameters require some more explanation. If a parameter isn't specified as "optional", it must be present and have a value in the request body.

**complexity**  
An integer value, ranging from 0-2.

- 0: Easy
- 1: Medium
- 2: Hard

**ruleset**  
A foreign key, which in this case is the primary key of the `ruleset` Table.

**campaign_length**  
An integer value, ranging from 0-2

- 0: Short
- 1: Medium
- 2: Long

**language**  
An integer value, ranging from 0-2

- 0: English
- 1: German
- 2: German and English

**image_url**  
The image URL has to be a direct link to an image.
