from turtle import title
import pytest
from app import schemas


def test_allposts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    posts_list = list(post_map)

    assert res.status_code == 200


def test_unauthorized_user_get_allposts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostOut(**res.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("awesome 2ndnew title", "awesome 2ndnew content", False),
        ("awesome 3rdnew title", "awesome 3rdnew content", True),
    ],
)
def test_createpost(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_unathorized_createpost(client, test_user, test_posts):
    res = client.post("/posts", json={"title": "jsdfja", "content": "safd"})
    assert res.status_code == 401


def test_unathorized_deletepost(client, test_user, test_posts):
    res = client.delete("/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_authorized_deletepost(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_postnotexist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{80}")

    res.status_code == 404


def test_del_otheruserspost(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_otheruserspost(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unathorized_updatepost(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_update_postnotexist(authorized_client, test_user, test_posts):
    res = authorized_client.put(f"/posts/{80}")

    res.status_code == 404
