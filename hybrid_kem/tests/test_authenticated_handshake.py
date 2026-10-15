"""Tests for the authenticated key-exchange handshake."""

from __future__ import annotations

import pytest

from hybrid_kem.protocols.authenticated_handshake import (
    AuthenticationError,
    Identity,
    Initiator,
    PeerIdentity,
    ProtocolError,
    Responder,
)

KEM_PROFILES = ["xwing", "mlkem1024+x25519"]
SIG_PROFILES = ["id-MLDSA65-Ed25519-SHA512", "id-MLDSA87-Ed448-SHAKE256"]


def _server(sig="id-MLDSA65-Ed25519-SHA512"):
    return Identity.generate("server.example", sig_profile=sig)


# ---- responder-only authentication -----------------------------------------


@pytest.mark.parametrize("kem", KEM_PROFILES)
def test_responder_auth_agree(kem):
    server = _server()
    resp = Responder(kem, identity=server)
    init = Initiator(kem, peer=server.public)

    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    key_i, m3 = init.finish(st_i, m2)

    assert m3 is None                       # no initiator auth in this mode
    assert key_i == resp.session_key(st_r)
    assert len(key_i) == 32


@pytest.mark.parametrize("sig", SIG_PROFILES)
def test_responder_auth_across_sig_profiles(sig):
    server = _server(sig)
    resp = Responder("xwing", identity=server)
    init = Initiator("xwing", peer=server.public)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    key_i, _ = init.finish(st_i, m2)
    assert key_i == resp.session_key(st_r)


# ---- mutual authentication --------------------------------------------------


def test_mutual_auth_agree():
    server, client = _server(), Identity.generate("client.example")
    resp = Responder("xwing", identity=server, require_peer=client.public)
    init = Initiator("xwing", peer=server.public, identity=client)

    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    key_i, m3 = init.finish(st_i, m2)
    assert m3 is not None
    key_r = resp.confirm(st_r, m3)
    assert key_i == key_r and len(key_i) == 32


def test_mutual_rejects_wrong_initiator():
    server, client, imposter = _server(), Identity.generate("c"), Identity.generate("x")
    resp = Responder("xwing", identity=server, require_peer=client.public)
    # imposter runs the initiator but is not the required peer
    init = Initiator("xwing", peer=server.public, identity=imposter)
    st_i, m1 = init.start()
    with pytest.raises(AuthenticationError):
        resp.respond(m1)  # responder pins the required initiator identity


def test_mutual_rejects_forged_msg3():
    server, client = _server(), Identity.generate("client")
    resp = Responder("xwing", identity=server, require_peer=client.public)
    init = Initiator("xwing", peer=server.public, identity=client)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    _key, m3 = init.finish(st_i, m2)
    bad = bytearray(m3)
    bad[-1] ^= 0x01
    with pytest.raises(AuthenticationError):
        resp.confirm(st_r, bytes(bad))


# ---- attacks on the responder's authentication -----------------------------


def test_tampered_ciphertext_fails_auth():
    server = _server()
    resp = Responder("xwing", identity=server)
    init = Initiator("xwing", peer=server.public)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    # flip a byte: the transcript hash changes, so sig_R no longer matches.
    bad = bytearray(m2)
    bad[-1] ^= 0x01
    with pytest.raises(AuthenticationError):
        init.finish(st_i, bytes(bad))


def test_wrong_server_key_rejected():
    server, other = _server(), _server()
    resp = Responder("xwing", identity=server)
    # the initiator pins a different server key than the one answering
    init = Initiator("xwing", peer=other.public)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    with pytest.raises(AuthenticationError):
        init.finish(st_i, m2)


def test_forged_responder_signature_rejected():
    server, attacker = _server(), _server()
    # attacker answers but the initiator expects the real server; attacker signs
    # with its own key, which the initiator does not trust.
    resp = Responder("xwing", identity=attacker)
    init = Initiator("xwing", peer=server.public)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    with pytest.raises(AuthenticationError):
        init.finish(st_i, m2)


# ---- suite binding and freshness -------------------------------------------


def test_suite_downgrade_rejected():
    server = _server()
    resp = Responder("xwing", identity=server)
    init = Initiator("mlkem1024+x25519", peer=server.public)  # different KEM
    st_i, m1 = init.start()
    with pytest.raises(ProtocolError):
        resp.respond(m1)


def test_independent_handshakes_differ():
    server = _server()
    resp = Responder("xwing", identity=server)
    init = Initiator("xwing", peer=server.public)
    keys = []
    for _ in range(2):
        st_i, m1 = init.start()
        st_r, m2 = resp.respond(m1)
        k, _ = init.finish(st_i, m2)
        keys.append(k)
    assert keys[0] != keys[1]


def test_peer_identity_from_pinned_bytes():
    server = _server()
    pinned = PeerIdentity(server.public.name, server.public.verification_key,
                          server.public.sig_profile)
    resp = Responder("xwing", identity=server)
    init = Initiator("xwing", peer=pinned)
    st_i, m1 = init.start()
    st_r, m2 = resp.respond(m1)
    k, _ = init.finish(st_i, m2)
    assert k == resp.session_key(st_r)
