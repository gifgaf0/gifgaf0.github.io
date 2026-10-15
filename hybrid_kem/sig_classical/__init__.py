"""Classical EdDSA signature legs (RFC 8032)."""

from .eddsa import Ed448Leg, Ed25519Leg

__all__ = ["Ed25519Leg", "Ed448Leg"]
