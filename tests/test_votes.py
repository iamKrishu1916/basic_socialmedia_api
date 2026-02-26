import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_onpost(authorized_client, test_posts):
    res = authorized_client.post("/vote", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twiceonpost(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_del_votenotexist(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_postnotexist(authorized_client, test_posts):
    res = authorized_client.post("/vote", json={"post_id": 80, "dir": 1})
    assert res.status_code == 404


def test_vote_unauth_user(client, test_user, test_posts):
    res = client.post("/vote", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
