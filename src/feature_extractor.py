"""
feature_extractor.py
---------------------
Converts a raw URL string into a set of numeric features that a
machine learning model can use to classify it as phishing or legitimate.

Version 2: adds subdomain count, entropy, suspicious keywords,
digit count, and path depth on top of the original 6 core features.
"""

import re
import math
from collections import Counter

import tldextract


def has_ip_address(url: str) -> int:
    """
    Returns 1 if the URL contains a raw IPv4 address instead of a domain name.
    Phishing sites often use IPs directly to avoid registering a domain.
    """
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    return 1 if re.search(ip_pattern, url) else 0


def has_https(url: str) -> int:
    """
    Returns 1 if the URL starts with https://.
    """
    return 1 if url.strip().lower().startswith("https://") else 0


def count_special_chars(url: str) -> int:
    """
    Counts occurrences of characters commonly used to obscure or
    manipulate URLs: @ % = & ?
    """
    special_chars = ["@", "%", "=", "&", "?"]
    return sum(url.count(ch) for ch in special_chars)


def count_subdomains(url: str) -> int:
    """
    Counts the number of subdomains using tldextract.
    'www' is excluded since it's a standard prefix and not a
    security signal — counting it penalizes normal URLs unfairly.
    """
    extracted = tldextract.extract(url)
    if not extracted.subdomain:
        return 0
    # Remove 'www' from subdomain parts before counting
    parts = [p for p in extracted.subdomain.split(".") if p.lower() != "www"]
    return len(parts)


def calculate_entropy(url: str) -> float:
    """
    Calculates Shannon entropy of the URL string - a measure of how
    'random' or unpredictable the characters are. Phishing URLs often
    have higher entropy due to randomized tokens/hashes used to evade
    detection or blocklists.
    """
    if len(url) == 0:
        return 0.0

    char_counts = Counter(url)
    length = len(url)
    entropy = 0.0
    for count in char_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return round(entropy, 3)


def has_suspicious_words(url: str) -> int:
    """
    Returns 1 if the URL contains common phishing bait words often used
    to trick users (e.g. mimicking login/verification pages).
    """
    suspicious_words = [
        "login", "verify", "secure", "account", "update",
        "banking", "confirm", "signin", "password", "auth",
    ]
    url_lower = url.lower()
    return 1 if any(word in url_lower for word in suspicious_words) else 0


def count_digits(url: str) -> int:
    """
    Counts numeric characters in the URL. Phishing URLs often contain
    long random numeric strings (e.g. in tracking IDs or obfuscation).
    """
    return sum(ch.isdigit() for ch in url)


def path_depth(url: str) -> int:
    """
    Counts the number of path segments after the domain.
    Strips the protocol (http:// or https://) first so those slashes
    don't get counted as path depth.
    """
    # Remove protocol prefix so :// doesn't pollute the count
    clean = re.sub(r"https?://", "", url)
    return clean.count("/")


def extract_features(url: str) -> dict:
    """
    Takes a raw URL string and returns a dictionary of numeric features.
    """
    url = str(url)  # guard against non-string input (e.g. NaN)

    features = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "has_ip": has_ip_address(url),
        "has_https": has_https(url),
        "num_special_chars": count_special_chars(url),
        "num_subdomains": count_subdomains(url),
        "url_entropy": calculate_entropy(url),
        "has_suspicious_words": has_suspicious_words(url),
        "num_digits": count_digits(url),
        "path_depth": path_depth(url),
    }
    return features


# Quick manual test when running this file directly
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.php?user=admin&pass=1234",
        "nobell.it/70ffb52d079109dca5664cce6f317373782/login.SkyPe.com/en/cgi-bin/verification/login/index.php",
        "https://secure-login.verify-account.example.co.uk/update/12345",
    ]

    for u in test_urls:
        print(u)
        print(extract_features(u))
        print()