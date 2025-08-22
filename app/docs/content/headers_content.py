headers_content = (
"""
# Response Headers

## Security Headers

To enhance security, all API responses include the following HTTP headers:

| Header                         | Description                                                                                                 |
|--------------------------------|------------------------------------------------------------------------------------------------------------ |
| `x-content-type-options`       | Set to `nosniff` to prevent browsers from MIME-sniffing responses and reduce XSS risks.                     |
| `strict-transport-security`    | Enforces https connections to protect data integrity and confidentiality.                                   |                                                                                            |
| `permissions-policy`           | Controls which features and APIs the browser can access (e.g., geolocation, camera, microphone).            |
| `cross-origin-resource-policy` | Restricts how resources are shared across origins to prevent data leaks.                                    |
| `referrer-policy`              | Controls how much referrer information is sent with requests.                                               |
| `x-frame-options`              | Prevents your site from being embedded in frames or iframes, mitigating clickjacking attacks.               |
| `x-xss-protection`             | Enables the browser’s built-in XSS filter to block reflected XSS attacks.                                   |
| `x-download-options`           | Instructs Internet Explorer to not execute downloads in the context of the site, reducing drive-by attacks. |
| `origin-agent-cluster`         | Isolates the origin to improve privacy and prevent cross-origin leaks.                                      |
| `cache-control` / `pragma`     | Prevents sensitive data from being cached in the browser or intermediary caches.                            |
| `x-dns-prefetch-control`       | Controls whether the browser is allowed to perform DNS prefetching, reducing privacy risks.                 |

## Rate Limit Headers

Insight Extractor AI Agent API enforces rate limiting to ensure stability and avoid unintended abuse. The following HTTP headers are included in all responses:

| Header                 | Description                                                                              |
|------------------------|------------------------------------------------------------------------------------------|
| `x-ratelimit-limit`    | The maximum number of requests allowed in the current rate limit window.                 |
| `x-ratelimit-remaining`| The number of requests you have left in the current window.                              |
| `x-ratelimit-reset`    | The time at which the current window resets, expressed as a Unix timestamp.              |
| `retry-after`          | The number of seconds to wait before making another request after hitting the rate limit.|

## Logging and Tracing Headers

To aid in debugging, observability, and request correlation across services, the following headers are included:

| Header         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `x-request-id` | A unique identifier assigned to each request. Useful for tracing logs and debugging distributed systems. |

"""
)