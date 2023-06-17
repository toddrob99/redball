from .requestor import Requestor, HttpType


class Lemmy:
    def __enter__(self):
        """Handle the context manager open."""
        return self

    def __exit__(self, *_args):
        """Handle the context manager close."""

    def __init__(self, instance, username, password):
        self.instance = instance
        self.username = username

        # Login, get token, and set as header for future
        self._req = Requestor({})
        self.auth_token = self.login(username, password)
        self._req.headers.update({"Authorization": "Bearer " + self.auth_token})
        # print(self._req.headers.get("Authorization"))

    def login(self, username, password):
        url = self.instance + "/api/v3/user/login"
        res_data = self._req.request(
            HttpType.POST, url, {"username_or_email": username, "password": password}
        )
        return res_data["jwt"]

    def getCommunity(self, name):
        url = self.instance + "/api/v3/community"
        res = self._req.request(HttpType.GET, url, {"name": name})

        self.community = res["community_view"]["community"]
        return self.community

    def listPosts(self, sort=None):
        url = self.instance + "/api/v3/post/list"
        res = self._req.request(
            HttpType.GET,
            url,
            {"sort": sort or "New", "community_id": self.community["id"]},
        )

        return res["posts"]

    def getPost(self, id):
        url = self.instance + "/api/v3/post"
        res = self._req.request(
            HttpType.GET,
            url,
            {"id": id},
        )

        return res["post_view"]

    def submitPost(self, title=None, body=None, url=None):
        api_url = self.instance + "/api/v3/post"
        res = self._req.request(
            HttpType.POST,
            api_url,
            {
                "auth": self.auth_token,
                "community_id": self.community["id"],
                "name": title,
                "body": body,
                "url": url,
            },
        )

        return res["post_view"]

    def editPost(self, post_id, title=None, body=None, url=None):
        api_url = self.instance + "/api/v3/post"
        data = {
            "auth": self.auth_token,
            "post_id": post_id,
        }
        if title:
            data["name"] = title
        if body:
            data["body"] = body
        if url:
            data["url"] = url

        res = self._req.request(HttpType.PUT, api_url, data)

        return res["post_view"]

    def submitComment(self, post_id, content, language_id=None, parent_id=None):
        api_url = self.instance + "/api/v3/comment"

        data = {
            "auth": self.auth_token,
            "content": content,
            "post_id": post_id,
        }

        if language_id:
            data["language_id"] = language_id
        if parent_id:
            data["parent_id"] = parent_id

        res = self._req.request(
            HttpType.POST,
            api_url,
            data,
        )

        return res["comment_view"]
