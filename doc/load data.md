# JSON

> Q: <br>**Mixed format**
>
> - *dict* including *list*
> - different *keys*
>
> A: <br>**Recursively extrac**t values from a nested dictionary using a list of keys.
>
> **Parameter**: (data, keys: list)
>
> - data, a nested dictionary, top layer is *dict*
>
> **Recursion**
>
> - current layer is *dict*
>   - `return function(data[keys[0]], keys[1:0])`
>     - `keys[0] in data`
>     - `len(key) > 1`
> - current layer is *list*
>   - `return [function(item, keys[1:0]) for item in data]`
>     - **add extra key** at will, e.g. `list`, it will not really be used because in code `keys[1:0]` it will be passed
>
> **Terminate**
>
> - `keys[0] not in data`
>   - `return none` 
> - `len(keys) == 1` 
>   - `return data.get(keys[0])`
>   - if `type(data) == list`, it will be unable to traverse the list
>   - so need to **add extra key** to indicate that this layer is *list*
>
> ```python
> def extract_values(data, keys: list):
>     """
>     Recursively extract values from a nested dictionary using a list of keys.
> 
>     :param data: a nested dictionary
>     :param keys: e.g. ["external_references", "list", "external_id"],
>                  "list" means the type of second layer in data is list
>     :return: value correspond with keys
>     """
>     if len(keys) == 1:
>         return data.get(keys[0])
>     else:
>         if isinstance(data, dict) and keys[0] in data:
>             return extract_values(data[keys[0]], keys[1:])
>         elif isinstance(data, list):
>             result: list = [extract_values(item, keys[1:]) for item in data]
>             return next(item for item in result if item is not None)
>         else:
>             return None
> ```
>
> E: <br>
>
> ```python
> keys: list = ["external_references", "list", "external_id"]
> ```