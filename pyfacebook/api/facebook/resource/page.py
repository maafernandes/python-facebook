"""
    Apis for page.
"""
from typing import Dict, List, Optional, Union, Tuple

import pyfacebook.utils.constant as const
from pyfacebook.api.facebook.resource.base import BaseResource
from pyfacebook.exceptions import LibraryError
from pyfacebook.models.page import Page
from pyfacebook.models.post import Post
from pyfacebook.utils.params_utils import enf_comma_separated


class FacebookPage(BaseResource):
    def get_info(
        self,
        page_id: Optional[str] = None,
        username: Optional[str] = None,
        fields: Optional[Union[str, list, tuple]] = None,
        return_json=False,
    ) -> Union[Page, dict]:
        """
        Get information about a Facebook Page.

        :param page_id: ID for the page.
        :param username: Username for the page.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for page.
            Or return json data. Default is false.
        :return: Page information.
        """
        if page_id:
            target = page_id
        elif username:
            target = username
        else:
            raise LibraryError(
                {"message": "Specify at least one of page_id or username"}
            )

        if fields is None:
            fields = const.PAGE_PUBLIC_FIELDS

        data = self.client.get_object(
            object_id=target,
            fields=enf_comma_separated(field="fields", value=fields),
        )
        if return_json:
            return data
        else:
            return Page.new_from_json_dict(data=data)

    def get_batch(
        self,
        ids: Optional[Union[str, list, tuple]],
        fields: Optional[Union[str, list, tuple]] = None,
        return_json: bool = False,
    ) -> Union[Dict[str, Page], dict]:
        """
        Get batch pages information by ids.

        :param ids: IDs for the pages.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param return_json: Set to false will return a dataclass for page.
            Or return json data. Default is false.
        :return: Pages information.
        """

        ids = enf_comma_separated(field="ids", value=ids)

        if fields is None:
            fields = const.PAGE_PUBLIC_FIELDS

        data = self.client.get_objects(
            ids=ids, fields=enf_comma_separated(field="fields", value=fields)
        )
        if return_json:
            return data
        else:
            return {
                page_id: Page.new_from_json_dict(item) for page_id, item in data.items()
            }

    def get_feed(
        self,
        page_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        source: Optional[str] = "feed",
        return_json: bool = False,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get feed of a Facebook Page including posts and links published by this Page, or by visitors to this Page.

        :param page_id: ID for page to get feeds.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param source: Resource type. Valid values are feed/posts/tagged/published_posts.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """

        if fields is None:
            fields = const.POST_PUBLIC_FIELDS + const.POST_CONNECTIONS_SUMMERY_FIELDS

        feeds, paging = self.client.get_full_connections(
            object_id=page_id,
            connection=source,
            count=count,
            limit=limit,
            fields=enf_comma_separated(field="fields", value=fields),
            since=since,
            until=until,
        )
        if return_json:
            return feeds, paging
        else:
            return [Post.new_from_json_dict(fd) for fd in feeds], paging

    def get_posts(
        self,
        page_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get the page's own posts.

        :param page_id: ID for page to get posts.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """
        return self.get_feed(
            page_id=page_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            source="posts",
            return_json=return_json,
        )

    def get_published_posts(
        self,
        page_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get all published posts by this page.

        :param page_id: ID for page to get published posts.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """
        return self.get_feed(
            page_id=page_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            source="published_posts",
            return_json=return_json,
        )

    def get_tagged_posts(
        self,
        page_id: str,
        fields: Optional[Union[str, list, dict]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        return_json: bool = False,
    ) -> Tuple[List[Union[Post, dict]], dict]:
        """
        Get posts which tagged the target page.

        :param page_id: ID for page to get tagged posts.
        :param fields: Comma-separated id string for data fields which you want.
            You can also pass this with an id list, tuple.
        :param since: A Unix timestamp or strtotime data value that points to the start of data.
        :param until: A Unix timestamp or strtotime data value that points to the end of data.
        :param count: The total count for you to get data.
        :param limit: Each request retrieve objects count.
            It should no more than 100. Default is None will use api default limit.
        :param return_json: Set to false will return a dataclass for post.
            Or return json data. Default is false.
        :return: Posts information and paging
        """
        return self.get_feed(
            page_id=page_id,
            fields=fields,
            since=since,
            until=until,
            count=count,
            limit=limit,
            source="tagged",
            return_json=return_json,
        )
