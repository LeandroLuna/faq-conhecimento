# Cloudfront

## Cloudfront Functions

### Forçar usuário e senha (Autenticação Basic) ao acessar o site

```js
function handler(event) {
    var user = "nome-do-usuario-aqui";
    var pass = "senha-aqui";
    function encodeToBase64(str) {
        var chars =      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
        for (
            // initialize result and counter
            var block, charCode, idx = 0, map = chars, output = "";
            // if the next str index does not exist:
            //   change the mapping table to "="
            //   check if d has no fractional digits
            str.charAt(idx | 0) || ((map = "="), idx % 1);
            // "8 - idx % 1 * 8" generates the sequence 2, 4, 6, 8
            output += map.charAt(63 & (block >> (8 - (idx % 1) * 8)))
        ) {
            charCode = str.charCodeAt((idx += 3 / 4));
            if (charCode > 0xff) {
                throw new InvalidCharacterError("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range."      );
            }
            block = (block << 8) | charCode;
        }
        return output;
    }
    var requiredBasicAuth = "Basic " + encodeToBase64(`${user}:${pass}`);
    var match = false;
    if (event.request.headers.authorization) {
        if (event.request.headers.authorization.value === requiredBasicAuth) {
            match = true;
        }
    }
    if (!match) {
        return {
            statusCode: 401,
            statusDescription: "Unauthorized",
            headers: {
                "www-authenticate": { value: "Basic" },
            },
        };
    }

    return event.request;
}
```

### Redirects no CloudFront

```js
function handler(event) {
    var request = event.request;
    var uri = request.uri;
    if ( uri.includes('/url/para/redirecionar') ) {
        var response = {
            statusCode: 301,
            headers: {
                "location": { "value": '/nova/url/aqui' }
            }
        }

        return response;
    }

    return request;
}
```

### Forçar o index.html no CloudFront

```js
function handler(event) {
    var request = event.request;
    var uri = request.uri;

    // Check whether the URI is missing a file name.
    if (uri.endsWith('/')) {
        request.uri += 'index.html';
    }
    // Check whether the URI is missing a file extension.
    else if (!uri.includes('.')) {
        request.uri += '/index.html';
    }

    return request;
}
```